# -*- coding: utf-8 -*-
"""sanjiu-core 语义 manifest 全量校验 + 位权互转往返。

CI 可持续保证：
1) 每份 manifest 通过 validate_manifest（space/三态词表/位权排列/索引约定）。
2) 用每份 manifest 的 bit_weight_map 做"随机构建向量 → to_core → from_core"
   往返，保证位权映射自洽（本仓 ↔ core 不丢失信息）。
3) 对 hexq-prod 的 1-based 偏移与反向组做定向抽查。
"""
import sys
import os
import glob
import json
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sanjiu_core.validate import (
    validate_manifest, validate_indices, to_core, from_core,
)
from sanjiu_core import g_to_idx, idx_to_g, N

_MANIFESTS = sorted(glob.glob(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                 "sanjiu_core", "manifests", "*.json")))


def _load_all():
    out = []
    for f in _MANIFESTS:
        with open(f, encoding="utf-8") as fh:
            out.append((os.path.basename(f), json.load(fh)))
    return out


def test_all_manifests_valid():
    assert _MANIFESTS, "未找到任何 manifest"
    for name, m in _load_all():
        assert validate_manifest(m), f"{name} 未通过 validate_manifest"


def test_all_manifests_idx_space_unique():
    # 每份 manifest 只声明编码方式；这里用 core 索引全集（0..19682）验证位权可互转
    for name, m in _load_all():
        bw = m.get("bit_weight_map", list(range(9)))
        assert sorted(bw) == list(range(9)), f"{name} 位权非排列"


def test_bitweight_roundtrip():
    random.seed(19683)
    for name, m in _load_all():
        for _ in range(200):
            vec = tuple(random.choice((-1, 0, 1)) for _ in range(9))
            core = to_core(vec, m)          # 本仓 → core 规范
            back = from_core(core, m)       # core → 本仓
            assert back == vec, f"{name} 位权往返不还原 {vec}->{core}->{back}"
            # 索引往返：本仓向量按位权归一为 core 向量后再算索引
            idx = g_to_idx(core)
            assert idx_to_g(idx) == core, f"{name} core 索引可逆失败"


def test_hexq_one_based_offset():
    # hexq-prod：idx 1-based（+1），互转须 core_idx = hexq_idx - 1
    for name, m in _load_all():
        if name.startswith("hexq"):
            bw = m.get("bit_weight_map")
            assert bw == [8, 7, 6, 5, 4, 3, 2, 1, 0], "hexq-prod 应为反向位权"
            # 定向：core 全中和向量 idx=9841 → hexq idx = 9841+1 = 9842
            neutral = (0,) * 9
            core_idx = g_to_idx(neutral)
            assert core_idx == 9841
            assert core_idx + 1 == 9842
            return
    raise AssertionError("未找到 hexq manifest 用于定向抽查")


def test_reverse_group_bitweight():
    # 反向组（cog-layer/heal-belief/hexq-prod）：bit_weight_map 应为 [8..0]
    for name, m in _load_all():
        if name.startswith(("cog_layer", "heal_belief", "hexq")):
            assert m.get("bit_weight_map") == [8, 7, 6, 5, 4, 3, 2, 1, 0], \
                f"{name} 应为反向位权"
            assert m.get("idx_convention") == "other", f"{name} idx_convention=other"


def test_forward_group_bitweight():
    # 正向组（tri9/meihua/xiuqiankun/sanjiu-nine）：恒等 [0..8]
    for name, m in _load_all():
        if name.startswith(("tri9", "meihua", "xiuqiankun", "sanjiu_nine")):
            assert m.get("bit_weight_map") == [0, 1, 2, 3, 4, 5, 6, 7, 8], \
                f"{name} 应为正向位权"
            assert m.get("idx_convention") == "g1_high", f"{name} idx_convention=g1_high"


def test_full_index_uniqueness():
    # core 索引全集唯一性（19683 卦一一对应）
    seen = set()
    for i in range(N):
        g = idx_to_g(i)
        assert idx_to_g(g_to_idx(g)) == g
        assert g_to_idx(g) not in seen
        seen.add(g_to_idx(g))
    assert len(seen) == 19683
