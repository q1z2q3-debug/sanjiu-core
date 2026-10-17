# -*- coding: utf-8 -*-
"""语义适配协议（manifest 校验）与互转。

「形式统一 + 语义自适配」的落点：
- sanjiu-core 提供唯一形式底座（索引、算子、校验）。
- 每个应用仓声明一份 manifest：三元词表（-1/0/+1 → 本仓语义）、
  九维位权映射（本仓第 i 维 ↔ core 第 j 维）、索引约定、领域清单。
- validate_manifest 保证 manifest 合法；validate_indices 保证数据落在 0..19682 且唯一。
- to_core / from_core 按位权映射把任意仓的卦向量/索引互转到 core 规范。
"""
from __future__ import annotations

# core 规范位权（g1 上爻最高位）：第 j 维对应 g[j]，bit_weight_map 给出
# 本仓向量元素顺序到 core 维序的映射（默认恒等 = 本仓即 g1..g9 上→下）。


def validate_manifest(m: dict) -> bool:
    """校验一份语义 manifest。合法返回 True，否则抛 ValueError。"""
    if m.get("space") != 19683:
        raise ValueError("manifest.space 必须为 19683")
    alpha = m.get("state_alphabet")
    if not isinstance(alpha, dict) or set(alpha.keys()) != {"-1", "0", "+1"}:
        raise ValueError("state_alphabet 必须恰好覆盖三态键 -1/0/+1（值为本仓语义词）")
    bw = m.get("bit_weight_map", list(range(9)))
    if sorted(bw) != list(range(9)) or len(bw) != 9:
        raise ValueError("bit_weight_map 必须是 0..8 的一个排列（长度 9）")
    if m.get("idx_convention") not in (None, "g1_high", "other"):
        raise ValueError("idx_convention 取值 g1_high / other")
    return True


def validate_indices(indices) -> bool:
    """数据校验：全部落在 0..19682 且唯一（任一仓 19683 空间索引需与 core 一致）。"""
    if isinstance(indices, dict):
        indices = list(indices.keys())
    return (all(isinstance(i, int) and 0 <= i <= 19682 for i in indices)
            and len(set(indices)) == len(indices))


def to_core(vec_or_idx, manifest=None):
    """按 manifest 的位权映射，把"本仓顺序"的 9 维向量转到 core 规范向量。
    未给 manifest 时视为已是 core 规范（g1..g9 上→下）。"""
    if manifest is None:
        return vec_or_idx
    bw = manifest.get("bit_weight_map", list(range(9)))
    # 本仓 vec[i] 应放到 core 的第 bw[i] 位
    if isinstance(vec_or_idx, (tuple, list)) and len(vec_or_idx) == 9:
        out = [0] * 9
        for i, j in enumerate(bw):
            out[j] = vec_or_idx[i]
        return tuple(out)
    return vec_or_idx  # 非向量输入原样返回


def from_core(vec, manifest=None):
    """core 规范向量 → 本仓顺序。"""
    if manifest is None:
        return vec
    bw = manifest.get("bit_weight_map", list(range(9)))
    if isinstance(vec, (tuple, list)) and len(vec) == 9:
        return tuple(vec[j] for j in bw)
    return vec
