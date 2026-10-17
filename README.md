# sanjiu-core · 三元九维符号体系形式层

**唯一数理底座**：`3⁹=19683` 状态空间 · 平衡三态 `{-1,0,+1}` · 错/综/错综/互/变算子 · 等价类 · 距离 · 校验。

> 设计原则：**形式统一 + 语义自适配**
> - 本包只承载**与语义无关**的数学底座（形式层）。
> - 领域语义（D/R/T、体/用/变、时空因果、阴/和/阳…）由各应用仓通过 **manifest** 自适配，不进入本包。

## 安装

```bash
pip install sanjiu-core
```

## 快速上手

```python
from sanjiu_core import idx_to_g, g_to_idx, F_C, F_Z, F_CZ, F_H, F_B_single

g = idx_to_g(189)            # ( -1,-1,-1,-1, 1, 0,-1,-1,-1 )
idx_to_g(0) == g_to_idx 逆运算
F_C(g)   # 错卦
F_Z(g)   # 综卦
F_H(g)   # 互卦(5维)
F_B_single(g, 5)  # 第5爻动
```

## 核心 API

| 函数 | 说明 |
|---|---|
| `idx_to_g / g_to_idx` | 索引 ↔ 9 维三元向量（三进制，g1 上爻最高位） |
| `F_C / F_Z / F_CZ` | 错 / 综 / 错综（对合算子） |
| `F_H` | 互卦内核投影（9→5 维） |
| `F_B_single / F_B_multi` | 单爻 / 多爻动变 |
| `distance` | 欧氏距离 |
| `build_universe / equivalence_groups` | 全集 19683 + 等价组（5002，Burnside 校验） |
| `validate_manifest / validate_indices` | 语义适配协议校验 + 数据校验 |
| `to_core / from_core` | 任意仓向量 ↔ core 规范（按位权映射） |

## 语义适配（manifest）

每个应用仓在 `sanjiu_core/manifests/` 声明一份 manifest：

```json
{
  "name": "sanjiu-nine",
  "space": 19683,
  "state_alphabet": { "-1": "D承载", "0": "R审定", "+1": "T增益" },
  "idx_convention": "g1_high",
  "bit_weight_map": [0,1,2,3,4,5,6,7,8],
  "domains": ["诗词", "卦典"]
}
```

- `state_alphabet`：把三态映射到本仓语义词（自适配点）
- `bit_weight_map`：把本仓维序映射到 core 规范（解决上中下 / 洛书九宫等维序差异）

## 公理约束

三元九爻公理与算子映射一经锁定，任何变更必须升主版本并显式记录（`docs/VERSIONING.md`）。
