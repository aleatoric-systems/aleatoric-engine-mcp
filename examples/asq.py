import numpy as np
import math
import logging
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict


# --- CONFIGURATION DATACLASS ---
@dataclass
class StratConfig:
    # Avellaneda Params
    gamma: float = 0.5  # Risk aversion
    k_liquidity: float = 1.5  # Liquidity parameter
    sigma_min: float = 0.40  # Floor for annualized volatility (40%)

    # Oracle / Signal Params
    conf_threshold_bps: int = 15
    conf_multiplier: float = 4.0

    # Stacking Params
    min_spread_bps: int = 5
    grid_levels: int = 5
    level_spacing_bps: int = 10
    max_inventory_units: float = 100.0

    # Time / Volatility Params
    vol_halflife_seconds: int = 300
    dt_seconds: float = 0.4  # Time horizon for the trade (T-t) used in skew calc


class ASQMaker:
    def __init__(self, symbol: str, config: StratConfig):
        self.symbol = symbol
        self.cfg = config

        # State
        self.oracle_price: float = 0.0
        self.oracle_conf: float = 0.0
        self.inventory_q: float = 0.0
        self.last_ts: float = 0.0

        # Initialize Variance (Annualized)
        self.vol_variance = self.cfg.sigma_min**2

        # Calculate alpha for EWMA
        self.alpha = 1.0 - math.exp(-1.0 / self.cfg.vol_halflife_seconds)

        self.is_stale = True
        self.circuit_breaker = False

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"MM-{symbol}")

    def on_tick(self, price: float, conf: float, timestamp: float, inventory: float):
        """
        Ingest live market data and update internal state.
        """
        if price <= 0:
            return

        # 1. Update Volatility (Only if we have a valid previous price)
        if self.oracle_price > 0 and not self.is_stale:
            # Log return
            ret = math.log(price / self.oracle_price)

            # SAFETY CLAMP: Limit single-tick return impact to 5% to prevent
            # volatility explosions from bad data or flash crashes.
            ret = max(min(ret, 0.05), -0.05)

            # Annualize the return for variance tracking
            # We assume the tick represents 'dt' time or 1 second on average for simplicity here
            # Ideally, use actual time delta: delta_t = timestamp - self.last_ts
            seconds_in_year = 31536000

            # Scale squared return to annual variance
            scaled_ret_sq = (ret**2) * seconds_in_year

            # Update EWMA
            self.vol_variance = (1 - self.alpha) * self.vol_variance + (
                self.alpha * scaled_ret_sq
            )

        self.oracle_price = price
        self.oracle_conf = conf
        self.inventory_q = inventory
        self.last_ts = timestamp
        self.is_stale = False

        self._run_safety_checks()

    def _run_safety_checks(self):
        """
        Monitor for Oracle Uncertainty.
        """
        uncertainty_coeff = (self.oracle_conf / self.oracle_price) * 10000

        if uncertainty_coeff > self.cfg.conf_threshold_bps:
            if not self.circuit_breaker:
                self.logger.warning(f"Uncertainty Spike: {uncertainty_coeff:.2f}bps")
            self.circuit_breaker = True
        else:
            self.circuit_breaker = False

    def get_quotes(self) -> Dict:
        """
        Calculate Optimal Quotes.
        """
        if self.is_stale or self.oracle_price == 0:
            return {"status": "STALE"}

        # --- AVELLANEDA CORE CALCS ---

        # 1. Volatility (Annualized)
        sigma = max(math.sqrt(self.vol_variance), self.cfg.sigma_min)

        # 2. Reservation Price Skew (r)
        # Formula: r = s - q * gamma * sigma^2 * (T-t)
        # We must scale the annualized sigma^2 down to the trading horizon (dt)
        dt_years = self.cfg.dt_seconds / 31536000

        # Skew is the distance from Mid to Reservation Price
        reservation_skew_val = (
            -1 * self.inventory_q * self.cfg.gamma * (sigma**2) * dt_years
        )

        # Convert absolute price skew to Basis Points
        skew_bps = (reservation_skew_val / self.oracle_price) * 10000

        # 3. Optimal Half-Spread (delta)
        # Formula: delta = (2/gamma) * ln(1 + gamma/k)
        # Note: We do NOT add sigma^2 here. Spread width is execution risk (gamma/k).
        spread_val = (2.0 / self.cfg.gamma) * math.log(
            1.0 + (self.cfg.gamma / self.cfg.k_liquidity)
        )

        half_spread_bps = (spread_val / 2.0 / self.oracle_price) * 10000
        half_spread_bps = max(half_spread_bps, self.cfg.min_spread_bps)

        # --- SIGNAL ADJUSTMENTS ---
        if self.circuit_breaker:
            half_spread_bps *= self.cfg.conf_multiplier

        # --- GRID GENERATION ---
        bids = []
        asks = []

        # Logic:
        # If Skew is NEGATIVE (Long Inventory): We want to sell.
        #   - Reservation Price is LOWER than Mid.
        #   - Bids move LOWER (Harder to buy).
        #   - Asks move LOWER (Easier to sell).

        for level in range(self.cfg.grid_levels):
            spacing = level * self.cfg.level_spacing_bps

            # Bid Offset Calculation
            # Offset = (Mid - BidPrice)
            # BidPrice = (Mid + Skew) - HalfSpread
            # Offset = HalfSpread - Skew + spacing
            # (Note: Subtracting a negative skew makes the offset larger -> price lower)
            bid_offset_bps = (half_spread_bps - skew_bps) + spacing

            # Ask Offset Calculation
            # Offset = (AskPrice - Mid)
            # AskPrice = (Mid + Skew) + HalfSpread
            # Offset = HalfSpread + Skew + spacing
            # (Note: Adding a negative skew makes the offset smaller -> price lower)
            ask_offset_bps = (half_spread_bps + skew_bps) + spacing

            # Clamp to minimum spread
            bid_offset_bps = max(self.cfg.min_spread_bps, bid_offset_bps)
            ask_offset_bps = max(self.cfg.min_spread_bps, ask_offset_bps)

            # --- HARD INVENTORY LIMITS ---
            # Instead of "penalty box", we simply don't quote that side

            # If Long Max: Stop Bidding
            if self.inventory_q <= self.cfg.max_inventory_units:
                size = 1.0 + (level * 0.5)
                bids.append({"offset_bps": int(bid_offset_bps), "size": size})

            # If Short Max: Stop Asking
            if self.inventory_q >= -self.cfg.max_inventory_units:
                size = 1.0 + (level * 0.5)
                asks.append({"offset_bps": int(ask_offset_bps), "size": size})

        return {
            "status": "ACTIVE",
            "oracle_price": self.oracle_price,
            "sigma_annual": sigma,
            "skew_bps": skew_bps,
            "half_spread_bps": half_spread_bps,
            "bids": bids,
            "asks": asks,
        }


# --- USAGE EXAMPLE ---
if __name__ == "__main__":
    config = StratConfig(gamma=0.5, conf_threshold_bps=10, max_inventory_units=50)

    maker = AvellanedaMarketMaker("SOL-PERP", config)

    print("--- SCENE: Long Inventory (+40 units) ---")
    # We are Long -> We want lower prices to sell.
    # Skew should be NEGATIVE.
    # Bid Offset should INCREASE (Lower Price).
    # Ask Offset should DECREASE (Lower Price).

    maker.on_tick(price=100.0, conf=0.05, timestamp=1000, inventory=40)

    quotes = maker.get_quotes()
    print(f"Skew: {quotes['skew_bps']:.2f} bps (Expect Negative)")
    print(f"Spread: {quotes['half_spread_bps']:.2f} bps")

    if quotes["bids"]:
        print(f"Bid L0 Offset: {quotes['bids'][0]['offset_bps']} bps")
    if quotes["asks"]:
        print(f"Ask L0 Offset: {quotes['asks'][0]['offset_bps']} bps")
