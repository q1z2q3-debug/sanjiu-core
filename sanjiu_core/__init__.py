# -*- coding: utf-8 -*-
"""sanjiu-core：三元九维符号体系形式层。"""
from .base import (
    N, D,
    idx_to_g, g_to_idx,
    F_C, F_Z, F_CZ, F_H, F_B_single, F_B_multi,
    distance, build_universe, equivalence_groups, burnside_expected, unit_test,
)
from .validate import validate_manifest, validate_indices, to_core, from_core

__version__ = "0.1.0"
__all__ = [
    "N", "D",
    "idx_to_g", "g_to_idx",
    "F_C", "F_Z", "F_CZ", "F_H", "F_B_single", "F_B_multi",
    "distance", "build_universe", "equivalence_groups", "burnside_expected", "unit_test",
    "validate_manifest", "validate_indices", "to_core", "from_core",
]
