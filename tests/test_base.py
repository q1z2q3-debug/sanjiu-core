# -*- coding: utf-8 -*-
"""sanjiu-core 单元测试：公理锁定样例 + 对合 + 索引可逆 + 等价组 Burnside。"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sanjiu_core import (
    idx_to_g, g_to_idx, F_C, F_Z, F_CZ, F_H, F_B_single, F_B_multi,
    equivalence_groups, burnside_expected, unit_test, N,
)
from sanjiu_core.validate import validate_manifest, validate_indices, to_core, from_core


def test_operators_locked():
    assert unit_test(), "锁定样例算子测试未通过"


def test_idempotent():
    G0 = (1, 0, -1, 1, 0, -1, 0, 1, -1)
    assert F_C(F_C(G0)) == G0
    assert F_Z(F_Z(G0)) == G0
    assert F_CZ(F_CZ(G0)) == G0


def test_index_bij():
    for i in range(0, N, 997):
        assert g_to_idx(idx_to_g(i)) == i


def test_equivalence_burnside():
    reps, groups = equivalence_groups()
    assert len(groups) == burnside_expected() == 5002


def test_multi_move():
    G = (+1, +1, 0, -1, +1, 0, -1, -1, 0)
    assert F_B_multi(G, [1, 5]) == F_B_single(F_B_single(G, 1), 5)


def test_manifest():
    import json
    p = os.path.join(os.path.dirname(__file__), "..", "sanjiu_core", "manifests", "sanjiu_nine.json")
    m = json.load(open(p, encoding="utf-8"))
    assert validate_manifest(m)
    assert validate_indices(list(range(19683)))


def test_roundtrip_weights():
    # 恒等位权时互转为原样
    v = (1, 0, -1, 1, 0, -1, 0, 1, -1)
    m = {"bit_weight_map": [0, 1, 2, 3, 4, 5, 6, 7, 8]}
    assert to_core(v, m) == v and from_core(v, m) == v


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"  [✓] {name}")
    print("sanjiu-core 单元测试全部通过")
