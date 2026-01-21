"""
SAGCO OS Core Module
====================

The core module contains the fundamental SAGCO kernel implementation.
"""

from .sagco import (
    SAGCOKernel,
    ConsciousnessState,
    QuantumState,
    MemoryLayer,
    ProcessingEngine,
)

__version__ = "0.1.0"

__all__ = [
    "SAGCOKernel",
    "ConsciousnessState",
    "QuantumState",
    "MemoryLayer",
    "ProcessingEngine",
]
