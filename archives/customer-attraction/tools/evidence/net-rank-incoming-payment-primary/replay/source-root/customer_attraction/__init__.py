"""Exact pure SPEs of the sequential, unit-player customer-attraction game.

This model is separate from the atomic, two-stage facility games in the sibling
packages. Integer customer multiplicities mean distinct identical unit clones.
"""

from .model import CustomerType, Instance, big_theme_lower_bound
from .exact import ExactSPESolver, SolverStats
from .certificate import (
    CertificateVerification,
    DeviationViolation,
    StrategyCertificate,
    verify_certificate,
)

__all__ = [
    "CustomerType", "Instance", "big_theme_lower_bound", "ExactSPESolver",
    "SolverStats", "StrategyCertificate", "CertificateVerification",
    "DeviationViolation", "verify_certificate",
]
