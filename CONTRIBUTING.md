# Contributing to The Aleatoric Engine

Thank you for your interest in contributing to The Aleatoric Engine!

---

## Getting Started

### Prerequisites

- Python 3.9+
- Git

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/aleatoric.git
cd aleatoric

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

---

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Follow the code style guidelines below.

### 3. Document Changes

Update relevant documentation:
- `README.md` for user-facing changes
- `CHANGELOG.md` for all changes
- Docstrings for new functions/classes

### 4. Commit

```bash
git add .
git commit -m "feat: add new feature"
```

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix  
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring
- `perf:` Performance improvement

### 5. Submit Pull Request

- Push to your fork
- Create PR with clear description
- Link related issues

---

## Code Style

### Python

Follow PEP 8 with these specifics:

```python
# Imports
import standard_library
import third_party
from aleatoric.module import Class

# Line length: 100 characters max

# Type hints
def function(param: int) -> str:
    """Docstring in Google style."""
    return str(param)

# Dataclasses for configuration
@dataclass
class Config:
    param1: float
    param2: int = 10  # Default

# Constants
CONSTANT_NAME = "value"
```

### Documentation

```python
def function(param1: float, param2: str) -> dict:
    """
    Brief description.
    
    Longer description with more details about the function's
    behavior and usage.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is negative
        
    Example:
        >>> result = function(1.5, "test")
        >>> print(result)
        {'key': 'value'}
    """
    ...
```

---

## Testing Guidelines

### Unit Tests

```python
def test_feature():
    """Test specific feature behavior."""
    # Arrange
    config = SimulationManifest(param=value)
    
    # Act
    result = function(config)
    
    # Assert
    assert result == expected
```

### Test Coverage

- Aim for >80% coverage
- Test both success and failure cases
- Test edge cases

---

## Adding New Features

### New Exchange Model

```python
# 1. Create module: src/aleatoric/venues/exchange_name.py
class ExchangeNameFundingModel:
    def calculate_funding_rate(self, spot, mark):
        # Exchange-specific formula
        ...
    
    def generate_perp_price(self, spot, funding):
        # Exchange-specific pricing
        ...

# 2. Export in venues/__init__.py
from .exchange_name import ExchangeNameFundingModel

__all__ = [..., 'ExchangeNameFundingModel']

# 3. Add preset in presets.py
class ExchangeNamePreset:
    @staticmethod
    def futures_btc(seed=None):
        return SimulationManifest(...)

# 4. Register preset
PRESETS["exchange_futures_btc"] = ExchangeNamePreset.futures_btc

# 5. Add tests
def test_exchange_funding():
    model = ExchangeNameFundingModel()
    rate = model.calculate_funding_rate(50000, 50100)
    assert rate > 0

# 6. Add documentation
# Update docs/FUNDING_MODELS.md with new exchange
```

### New Feature

1. Implement in appropriate module
2. Add configuration parameters to `SimulationManifest`
3. Write unit tests
4. Update docstrings
5. Add example to `examples/`
6. Update `CHANGELOG.md`

---

## Documentation

### When to Update

- **README.md**: User-facing features, installation, quick start
- **FUNDING_MODELS.md**: Exchange-specific mechanics
- **CHANGELOG.md**: All changes (following semantic versioning)
- **Examples**: New features or use cases

### Documentation Style

- Clear, concise language
- Code examples for all features
- Visual aids (tables, diagrams) where helpful
- Keep up-to-date with code

---

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create git tag: `git tag v0.2.0`
4. Push tag: `git push origin v0.2.0`
5. Build: `python -m build`
6. Publish: `twine upload dist/*`

---

## Questions?

- Check existing issues
- Ask in discussions
- Email maintainers

---

Thank you for contributing! 🚀
