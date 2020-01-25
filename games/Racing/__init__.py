#!/usr/bin/env python3
print("loaded", __name__)

__all__ = [
	"constants",
	"helpers",
	"core",
]

from .core import Racing
from .core import example
