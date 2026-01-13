from __future__ import annotations

import argparse
import os
import sys


import numpy as np
import pandas as pd

from examples.asq import ASQMaker, StratConfig


# --- CONFIGURATION (Drift Protocol / Solana Params) ---
INITIAL_CASH = 10_000.0  # USDC
BASE_PRICE = 100.0  # SOL Price
SIM_STEPS = 10_000  # Approx 1 hour of blocks (400ms per step)
DT_SECONDS = 0.4  # Block time

# Avellaneda-Stoikov Parameters
GAMMA = 0.1  # Risk aversion (Aggressive = 0.01, Conservative = 1.0)
SIGMA_BASE = 0.5  # Annualized Volatility (50%)
K_LIQUIDITY = 1.5  # Order book liquidity parameter (Fill probability decay)

# Oracle Parameters (Pyth)
CONF_THRESHOLD = 0.0015  # 15 bps (If Conf/Price > 0.15%, assume toxic flow)
CONF_MULTIPLIER = 5.0  # How much to widen spreads during high uncertainty


class MarketSimulator:
    def __init__(self, steps, dt, base_price, sigma):
        self.steps = steps
        self.dt = dt

        # 1. Generate Synthetic Price Path (GBM)
        # We add "Jumps" to simulate Oracle dislocations where Confidence would spike
        t = np.linspace(0, steps * dt, steps)
        drift = 0.0

        # Stochastic Volatility component
        vol_process = np.abs(np.random.normal(sigma, sigma * 0.5, steps))

        # Price Generation
        returns = np.random.normal(
            drift * dt, vol_process * np.sqrt(dt / 31536000), steps
        )

        # Add "Toxic Shocks" (Price jumps)
        jumps = np.random.poisson(0.005, steps) * np.random.normal(
            0, 0.02, steps
        )  # 0.5% chance of 2% jump
        returns += jumps

        self.prices = base_price * np.exp(np.cumsum(returns))

        # 2. Generate Oracle Confidence Signal (Correlated with Vol + Jumps)
        # High Vol or Jumps = Wide Confidence Interval
        self.confs = self.prices * (
            0.0005 + (np.abs(jumps) * 10) + (vol_process * 0.001)
        )

    def get_data(self):
        return pd.DataFrame({"price": self.prices, "conf": self.confs})


class Strategy:
    def __init__(self, name, use_oracle_signal=False):
        self.name = name
        self.use_signal = use_oracle_signal
        self.cash = INITIAL_CASH
        self.inventory = 0.0
        self.pnl_history = []
        self.fills_history = []

    def quote(self, current_price, current_conf, current_vol):
        # --- CORE AVELLANEDA LOGIC ---

        # 1. Calculate Reservation Price (r)
        # Shifts "fair value" based on inventory (q).
        # If Long (q>0), r < price (Try to sell). If Short (q<0), r > price (Try to buy).
        reservation_price = current_price - (self.inventory * GAMMA * (current_vol**2))

        # 2. Calculate Optimal Spread (half_spread)
        # Wider if vol is high or risk aversion (gamma) is high
        spread_term = (GAMMA * (current_vol**2)) + (2 / GAMMA) * np.log(
            1 + (GAMMA / K_LIQUIDITY)
        )
        half_spread = spread_term / 2.0

        # Convert to drifting "Oracle Offsets"
        bid_price = reservation_price - half_spread
        ask_price = reservation_price + half_spread

        # --- ORACLE ADVERSE SELECTION SIGNAL ---
        is_toxic = False
        uncertainty_coeff = current_conf / current_price

        if self.use_signal:
            # If Confidence is wide, widen quotes drastically to avoid "Toxic Flow"
            if uncertainty_coeff > CONF_THRESHOLD:
                is_toxic = True
                bid_price -= half_spread * CONF_MULTIPLIER  # Bid lower
                ask_price += half_spread * CONF_MULTIPLIER  # Ask higher

        return bid_price, ask_price, is_toxic

    def update_fill(self, fill_price, quantity):
        cost = fill_price * quantity
        self.cash -= cost
        self.inventory += quantity


def run_simulation():
    # Setup Environment
    sim = MarketSimulator(SIM_STEPS, DT_SECONDS, BASE_PRICE, SIGMA_BASE)
    data = sim.get_data()

    # Initialize Strategies
    naive_mm = Strategy("Naive Avellaneda", use_oracle_signal=False)
    smart_mm = Strategy("Oracle-Aware MM", use_oracle_signal=True)

    strategies = [naive_mm, smart_mm]

    print(
        f"Running Simulation: {SIM_STEPS} blocks ({SIM_STEPS * DT_SECONDS / 60:.1f} mins)..."
    )

    # Main Loop
    for t in range(len(data)):
        price = data["price"].iloc[t]
        conf = data["conf"].iloc[t]

        # Estimate instantaneous volatility (simple rolling window proxy for simulation)
        # In production, use high-freq estimator
        if t < 10:
            continue
        vol_proxy = (
            data["price"].iloc[t - 10 : t].std()
            / price
            * np.sqrt(31536000 * DT_SECONDS)
        )
        if np.isnan(vol_proxy) or vol_proxy == 0:
            vol_proxy = SIGMA_BASE

        for strat in strategies:
            # 1. Get Quotes
            bid, ask, is_toxic = strat.quote(price, conf, vol_proxy)

            # 2. Match Engine Simulation (Stochastic Fill)
            # Probability of fill decreases as distance from mid-price increases
            dist_bid = price - bid
            dist_ask = ask - price

            prob_bid = np.exp(-K_LIQUIDITY * dist_bid)
            prob_ask = np.exp(-K_LIQUIDITY * dist_ask)

            # Random "Market Arrival" check
            if np.random.random() < prob_bid:
                strat.update_fill(bid, 1.0)  # Buy 1 unit

            if np.random.random() < prob_ask:
                strat.update_fill(ask, -1.0)  # Sell 1 unit

            # 3. Mark to Market PnL
            nav = strat.cash + (strat.inventory * price)
            strat.pnl_history.append(nav)

    # --- RESULTS ANALYSIS ---
    print("\n" + "=" * 40)
    print(f"{'METRIC':<20} | {'NAIVE MM':<15} | {'ORACLE MM (YOU)':<15}")
    print("=" * 40)

    results = {}
    for strat in strategies:
        pnl_series = pd.Series(strat.pnl_history)
        total_ret = pnl_series.iloc[-1] - INITIAL_CASH
        max_dd = (pnl_series - pnl_series.cummax()).min()
        vol = pnl_series.diff().std()
        sharpe = (
            (pnl_series.diff().mean() / vol) * np.sqrt(365 * 24 * 60 * 60 / DT_SECONDS)
            if vol > 0
            else 0
        )

        results[strat.name] = {"Ret": total_ret, "DD": max_dd, "Sharpe": sharpe}

    n_res = results["Naive Avellaneda"]
    s_res = results["Oracle-Aware MM"]

    print(f"{'Total Return ($)':<20} | {n_res['Ret']:>15.2f} | {s_res['Ret']:>15.2f}")
    print(f"{'Max Drawdown ($)':<20} | {n_res['DD']:>15.2f} | {s_res['DD']:>15.2f}")
    print(f"{'Sharpe Ratio':<20} | {n_res['Sharpe']:>15.2f} | {s_res['Sharpe']:>15.2f}")
    print("=" * 40)

    # Interpretation
    diff = s_res["Ret"] - n_res["Ret"]
    print(f"\nVALIDATION VERDICT: Oracle Filter generated ${diff:.2f} excess return.")
    if diff > 0:
        print(
            "SUCCESS: Avoiding high-uncertainty zones reduced adverse selection losses."
        )
    else:
        print("FAIL: Parameters too conservative; missed profitable volume.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate simulation config")
    parser.add_argument("--config-file", help="Path to JSON config file")
    parser.add_argument("--show-schema", action="store_true", help="Print JSON Schema")
    parser.add_argument("--symbol", default="BTC", help="Symbol (default: BTC)")
    parser.add_argument("--seed", type=int, default=42, help="Seed (default: 42)")
    args = parser.parse_args()

    api_key = os.getenv("ALEATORIC_API_KEY")
    if not api_key:
        print("Error: Set ALEATORIC_API_KEY environment variable", file=sys.stderr)
        return 1

    headers = {"X-API-Key": api_key}

    with httpx.Client(timeout=30) as client:
        if args.show_schema:
            resp = client.get(f"{BASE_URL}/mcp/config/schema", headers=headers)
            resp.raise_for_status()
            print(json.dumps(resp.json(), indent=2))
            return 0

        if args.config_file:
            with open(args.config_file) as f:
                config = json.load(f)
        else:
            config = {
                "symbol": args.symbol,
                "seed": args.seed,
                "tick_size": 0.01,
                "lot_size": 0.001,
                "initial_mid": 50000.0,
                "initial_spread_bps": 1.0,
                "book_depth": 10,
                "volatility": 0.02,
                "drift": 0.0,
                "mean_reversion": 0.1,
            }

        print(f"Validating: symbol={config.get('symbol')}, seed={config.get('seed')}")

        resp = client.post(
            f"{BASE_URL}/mcp/config/validate",
            json={"config": config},
            headers=headers,
        )
        resp.raise_for_status()
        result = resp.json()

        if result.get("valid"):
            print(f"Valid! Hash: {result.get('hash')}")
            print(json.dumps(result.get("config", {}), indent=2))
        else:
            print(f"Invalid: {result.get('errors', [])}")
            return 1

    return 0
