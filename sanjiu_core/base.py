# -*- coding: utf-8 -*-
"""sanjiu-core · 三元九维符号体系形式层。

只承载"与语义无关"的数学底座（形式层）：
  3^9=19683 状态空间 · 平衡三态 {-1,0,+1} · 错/综/错综/互/变算子 · 等价类 · 距离。

领域语义（D/R/T、体用变、时空因果、阴阳…）不在本包，由各应用仓以 manifest 自适配。
公理一经锁定不可修改；任何变更须升主版本并显式记录（见 docs/VERSIONING.md）。

索引约定（本包唯一规范）：g1 上爻为最高位，Σ(vᵢ·3^(8-i)) → 0..19682。
"""
from __future__ import annotations

import math

N = 3 ** 9                 # 19683 卦总数
D = 9                      # 维度（爻数）


# ---------------- 索引 ↔ 卦向量 互转 ----------------
def idx_to_g(idx: int) -> tuple:
    """0..19682 → 9 维三元向量 (g1..g9)，gi∈{-1,0,+1}，g1 上爻为最高位。"""
    out = [0] * D
    v = idx
    for i in range(D - 1, -1, -1):
        out[i] = v % 3 - 1
        v //= 3
    return tuple(out)


def g_to_idx(g) -> int:
    """9 维三元向量 → 0..19682（三进制，g1 最高位）。"""
    idx = 0
    for x in g:
        idx = idx * 3 + (x + 1)
    return idx


# ---------------- 算子（公理2~6，纯形式，与语义无关） ----------------
def F_C(g) -> tuple:
    """错卦（对偶）：逐爻独立取反 +1<->-1，0 不变。F_C(F_C(g))=g。"""
    return tuple(-x for x in g)


def F_Z(g) -> tuple:
    """综卦（反转）：序列反转 [g1..g9]->[g9..g1]。F_Z(F_Z(g))=g。"""
    return g[::-1]


def F_CZ(g) -> tuple:
    """错综复合：先综后错。F_CZ(g)=F_C(F_Z(g))。"""
    return F_C(F_Z(g))


def F_H(g) -> tuple:
    """互卦（内核投影）：剔除 g1,g9，取中心连续 5 爻 [g3,g4,g5,g6,g7] → 5 维。"""
    return g[2:7]


def F_B_single(g, pos: int) -> tuple:
    """单爻动（变卦）：F_B(+1)=0, F_B(-1)=0, F_B(0)=+1。pos: 1..9。"""
    i = pos - 1
    v = g[i]
    nv = 0 if v != 0 else 1
    return g[:i] + (nv,) + g[i + 1:]


def F_B_multi(g, positions) -> tuple:
    """多爻动：各动爻独立计算。"""
    out = list(g)
    for pos in positions:
        i = pos - 1
        out[i] = 0 if out[i] != 0 else 1
    return tuple(out)


# ---------------- 空间距离 ----------------
def distance(gA, gB) -> float:
    """欧氏距离 D = sqrt(Σ(aᵢ-bᵢ)²)。"""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(gA, gB)))


# ---------------- 全集 / 等价类 ----------------
def build_universe():
    """全集 19683 卦 + 逐卦批量错/综/错综/互卦 + 算子固定点计数（Burnside 校验用）。"""
    full = [idx_to_g(i) for i in range(N)]
    return {
        "full": full,
        "fc": [F_C(g) for g in full],
        "fz": [F_Z(g) for g in full],
        "fcz": [F_CZ(g) for g in full],
        "fh": [F_H(g) for g in full],
        "fix": {
            "e": N,
            "F_C": sum(1 for g in full if F_C(g) == g),
            "F_Z": sum(1 for g in full if F_Z(g) == g),
            "F_CZ": sum(1 for g in full if F_CZ(g) == g),
        },
    }


def equivalence_groups():
    """对每卦构造 {G, F_C(G), F_Z(G), F_CZ(G)} 去重，统计独立等价组。"""
    seen = set()
    groups = []
    reps = []
    for i in range(N):
        g = idx_to_g(i)
        grp = frozenset({g, F_C(g), F_Z(g), F_CZ(g)})
        if grp not in seen:
            seen.add(grp)
            groups.append(sorted(grp))
            reps.append(g)
    return reps, groups


def burnside_expected() -> int:
    """等价组数理论值（Burnside）：(|G| + |F_C 固定| + |F_Z 固定| + |F_CZ 固定|) / 4。"""
    u = build_universe()
    f = u["fix"]
    return (f["e"] + f["F_C"] + f["F_Z"] + f["F_CZ"]) // 4


# ---------------- 单元测试（锁定样例，禁止改公理） ----------------
def unit_test() -> bool:
    G = (+1, +1, 0, -1, +1, 0, -1, -1, 0)
    cases = {
        "F_C(G)": (F_C(G), (-1, -1, 0, +1, -1, 0, +1, +1, 0)),
        "F_Z(G)": (F_Z(G), (0, -1, -1, 0, +1, -1, 0, +1, +1)),
        "F_CZ(G)": (F_CZ(G), (0, +1, +1, 0, -1, +1, 0, -1, -1)),
        "F_H(G)": (F_H(G), (0, -1, +1, 0, -1)),
        "第5爻动": (F_B_single(G, 5), (+1, +1, 0, -1, 0, 0, -1, -1, 0)),
    }
    ok = True
    for name, (got, exp) in cases.items():
        if got != exp:
            ok = False
    # 对合性质
    G0 = (1, 0, -1, 1, 0, -1, 0, 1, -1)
    ok = ok and F_C(F_C(G0)) == G0 and F_Z(F_Z(G0)) == G0 and F_CZ(F_CZ(G0)) == G0
    # 索引可逆（抽样）
    for i in range(0, N, 997):
        if g_to_idx(idx_to_g(i)) != i:
            ok = False
            break
    return ok
