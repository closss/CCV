# CCV/SKETCH 修改任务书（NeurIPS 2026 camera-ready / arXiv v1）

Sep 27, 2026 · @anderson

## 总览

本轮任务书交给写作 agent 做第一轮修改，只包含凭论文原文和 rebuttal 就能完成的改动。核心主线是把“两通道条件独立、偶然一致很罕见”的叙事，整体替换为“两通道正相关，但一致性的似然比 > 1 即可提升精度”。

本轮规则：

- **不动数字只标记**：GPS-clean 是 GPS-full 的严格子集，所有基于 1,709 题汇总的数字都将重算。这些数字保持原值，用 `\recheck{}` 包起来；从 rebuttal 新写入的汇总数字同样处理。每个 benchmark 单列的准确率不需要包。
- **宏定义**：在导言区加 `\newcommand{\recheck}[1]{\textcolor{red}{#1}}`，重算结果回来后统一替换。
- **不自行计算**：不要推算、舍入或修正任何汇总数字，也不要补写论文和 rebuttal 里没有的实验细节。
- **本轮不动**：作者与致谢；图片本身（图注文字可以改）；arXiv 打包；以及最后一节列出的待工程核查事项。

优先级定义：**P0** 为 AC 点名或影响主结果口径的问题；**P1** 为 rebuttal 里明确承诺的修改；**P2** 为通读发现的小问题。每条标注来源（AC / R1 / R2 / R3）和投稿版行号。

## P0：必改项

P0-0 是作者自查发现的口径问题，P0-1 到 P0-6 来自 metareview。P0-1 到 P0-3 是同一件事的三个层面（事实、数字、理论），建议一起改。

### P0-0 评测口径：GPS-clean ⊂ GPS-full

- 来源：作者自查。GPS-clean（146）是 MathVista-GPS（208）的严格子集，汇总时被重复计数。
- 位置：Table 1；Table 2；摘要与 L80 的 “four benchmarks”；Sec 4.1–4.3；App C L446–447；App E L456–459；Table E.1 与 Table D.2 图注；checklist 第 7 项
- 改法：
  - 主评测改为 Geometry3K test、GeoQA test、GPS-clean 三个集合；GPS-full 降为参考。
  - Table 1：GPS-full 的 Role 改为“Reference (superset of GPS-clean)”，并加脚注说明包含关系。
  - Table 2：All 列定义改为三个主集合的汇总；GPS 列移到最右并用竖线隔开，表注写明不计入 All。All 列数值保持原样，包 `\recheck{}`。
  - 全文 “four (geometry) benchmarks” 改为 “three benchmarks, with GPS-full reported for reference”。
  - App C 的 heldout/OOD 定义去掉 MathVista-GPS。
  - 所有 1,709 与 27,344 包 `\recheck{}`。

### P0-1 生成顺序与通道耦合

- 来源：AC；R1 Q1、R1 Limitations
- 位置：Eq.(1) 及 L47–55；Sec 2 Closed-loop structure L98–103；Fig 1 图注；摘要 L10–14
- 改法：
  - Eq.(1) 后加一句：单次自回归解码顺序为 \[VGF\] → \[DSL\] → \[Final Answer\]；exec 由外部沙箱解释器在生成后执行。
  - 明确写出：claim 以 DSL 源码为条件，但不以 DSL 输出为条件。附段落顺序统计 `\recheck{27,342/27,344}`。
  - 新增耦合小表：题内均值 φ = `\recheck{0.325}`（`\recheck{766}` 个有效题，⊥ 计为 exec ✗），并列 ρ\_e = `\recheck{0.526}` 作参照。
  - 删除或改写所有“独立收敛 / neural errors relatively independent / fail for different reasons”类表述。
  - Fig 1 图注补一句“execution is performed externally after generation”。图本身下轮再改。

### P0-2 修正 0.225

- 来源：AC；R1 Q2（R1 称这是最重要的一条）
- 位置：L63–74（Principle 段 + 0.225 句）
- 改法：
  - 替换为全池值 P(exec ✓ | claim ✓) = `\recheck{0.736}`，对比 p\_e = `\recheck{0.617}`，明说两通道正相关。
  - 删掉 “only weakly coupled” 和 0.225。
  - Principle 段的 “independently converge” 和 “for any k bounded by N\_eff” 没有证明支撑，改写为似然比条件的直观版本。

### P0-3 用似然比条件替换条件独立假设

- 来源：AC；R1 Q2 与理论批评；AC final justification（“theory does not guarantee pool-level gains”）
- 位置：Sec 3.2 L126–148；Fig 2 图注；App J.1–J.4；checklist 第 3 项
- 改法：
  - Theorem 1 只保留恒等式 p\_κ = t\_κ/(t\_κ + f\_κ)；删掉 L132–134 的潜变量条件独立与均匀分散部分。
  - 新增命题（0 < p\_e < 1）：p\_κ > p\_e 当且仅当 P(agree | exec ✓) > P(agree | exec ✗)。App J 补三行证明，并附下表。
  - Theorem 2 明确定位为近似，并写明“精度条件不蕴含池级投票增益”。
  - L135–138 “f\_κ is rare” 删除。用 Gemma 做反例：`\recheck{40.2%}` 的 κ 候选是假一致，但保留精度仍从 `\recheck{33.4%}` 升到 `\recheck{59.8%}`。
  - Corollary 1（L572–575）依赖均匀分散假设，删除或降为 remark。
  - L584–585 “most κ=1 candidates correspond to true agreement” 补上 Gemma 的假一致率。
  - Fig 2 图注 “false agreement is dispersed” 改为不依赖分散假设的说法。
  - 增加“预测试”用法：部署前在带标签的候选池上测该比值，接近 1 则 κ 过滤几乎无收益。

下表全部数字写入论文时包 `\recheck{}`：

| 指标 | Qwen3.5-9B | Gemma4-E4B |
| --- | --- | --- |
| P(agree \| exec ✓) | 0.802 | 0.646 |
| P(agree \| exec ✗) | 0.192 | 0.218 |
| 比值 | 4.18× | 2.96× |
| 题内 Mantel–Haenszel（排除 ⊥） | 3.22× | 2.09× |
| CCV 相对 Claim MV | +10.41 pp | +7.84 pp |

可选加强（我的建议，rebuttal 未承诺）：把该命题写成赔率恒等式，它给出的是精确预测而不只是方向。按现有数字，Qwen 与 Gemma 的预测值都与表 D.1 吻合。写作 agent 只写公式和证明，验证用的代入数字等重算后再填。

```latex
\frac{p_\kappa}{1-p_\kappa} = \frac{p_e}{1-p_e} \cdot \frac{P(\kappa=1 \mid \text{exec}\,\checkmark)}{P(\kappa=1 \mid \text{exec}\,\times)}
```

### P0-4 收窄 “no additional inference”

- 来源：AC；R1 Q4；R2 W1
- 位置：摘要 L16；贡献 L78–80；Sec 3.3 Complexity L172；结论 L279 “training-free”；Table E.1 图注
- 改法：
  - 统一表述为：“在已有 SKETCH 候选池上验证无需额外模型调用”。明写生成器需要 LoRA SFT 和教师重格式化流程。
  - 明说 CCV 不是任意候选池上的 drop-in verifier。“training-free” 改为 “training-free verifier”。
  - 加成本对比（见下表），正文一句，完整表放附录。与池大小相关的数字包 `\recheck{}`。

| 项目 | 成本 |
| --- | --- |
| CCV 聚合 | 单 CPU 核 2–4 ms/题；全池 `\recheck{4–7 s}` |
| DSL 执行（与 Exec MV / EAV / PROVE 共享） | 全部 `\recheck{27,344}` 候选 < 10 s |
| SKETCH 候选长度 | 均值约 86 tokens |
| LoRA SFT（一次性） | 约 3.5 GPU·h 至评估 checkpoint；全程约 10.6 |
| URSA-RM weighted MV | 每候选一次 RM 前向 |
| CISC | 每候选一次自评 |

### P0-5 CCV 把正确答案改错的分析

- 来源：AC；R2 W2
- 位置：Sec 4.6 与 Fig D.1 图注
- 改法（以下所有计数包 `\recheck{}`）：
  - Sec 4.6 改为双向报告：相对 Claim MV 为 237 赢 / 59 输（4.02:1），相对 EAV 为 121 / 39（3.10:1）。
  - 写明各 benchmark 净增益均为正：相对 Claim MV 从 +8.22 pp（GeoQA）到 +13.70 pp（GPS-clean）。
  - 加两个 2×2 交换表（Claim MV：1,147 / 237 / 59 / 266；EAV：1,263 / 121 / 39 / 286），空间不够就放附录。
  - 加三类回退分类：(i) 假 κ 一致，26/59 vs Claim MV、30/39 vs EAV，错误 κ 组很小（中位数 3 / 2）。(ii) 回退分支错误执行共识，33 例，全部无候选执行出正确答案，15 例为 16/16 一致。(iii) 阈值效应，仅相对 EAV，7 例。
  - Fig D.1 图注补一句，说明该图只展示恢复方向，回退见新表。

### P0-6 收窄几何以外的 claim

- 来源：AC；R1 Q3；R3 W2
- 位置：结论 L283–285；摘要末句 L18–20；checklist 第 1 项
- 改法：
  - 结论中“其他领域也可受益”明确标为假设。
  - 给出可证伪的下一步：在 chart/table QA、physics diagrams、code generation 的带标签候选池上先测似然比。
  - 摘要 “confirming that structural diversity is the core verification resource” 限定为 “in geometry”。

## P1：rebuttal 承诺兑现清单

除 P0 已覆盖的内容外，本轮可完成的承诺有 6 项，工作量最大的是新 Limitations 节。基线实现附录和完整算力记账需要仓库信息，已移到最后一节。

| 承诺内容 | 来源 | 放在哪里 | 素材 / 要点 |
| --- | --- | --- | --- |
| 独立的 Limitations 节，逐项分析而非一笔带过 | R1、R3 | 结论前新增一节 | 五项：单次生成 vs 独立性理想化（φ 包 `\recheck{}`）；SKETCH-SFT 与教师流程依赖；格式退化会缩小 κ 池并触发回退而非静默出错；仅几何验证与可测迁移条件；Exec✗Claim✗ 恢复率低及 oracle 余量分解（8.3%、93.27%、91.75% 均包 `\recheck{}`） |
| 闭源模型与开放式证明题的边界 | R3 Q1、Q2 | Limitations 节 | 闭源模型可能靠 few-shot 产出 SKETCH，但未测试，不声称；证明题需把数值一致改为 proof checker 判决层一致，属于扩展而非调参 |
| 其余常数的敏感性扫描 | R1 Q5 | App C / App H 旁新表 | 先写文字和表格结构，数字包 `\recheck{}`。要点：绝对容差与聚类容差跨 4 个数量级不变；选项映射容差默认 0.02 并非局部最优；claim 权重在 \[0, 2\] 内波动很小；+1 bonus 在 κ 池内为公共常数，不影响 argmax（最后一条是证明，不需重算） |
| 符号表 | R2 W3 | 新附录 | κ、t\_κ、f\_κ、p\_e、p\_κ、ρ\_e、ρ\_κ、K\_κ、τ\_exec、φ 等 |
| 缩写首次出现即定义 | R1、R2 W3 | 全文 | EAV = Execution-Answer Voting（首次出现在 Sec 4.2）；s240 = 冻结的 Qwen rollout 池（首次出现在 L203）；VGF、DSL、MV、CISC、PRM、GPS-c 一并检查 |
| 开源承诺与 checklist 修正 | R1、R3 | 正文一句 + checklist 第 4、6 项 | 文字写明将发布评测与聚合脚本、冻结候选池与逐题选择、外部 scorer 文件、audit 脚本，不放链接；第 4 项 “Appendices ??”；第 6 项 MathVerse 改 MathVista |

## P2：通读发现的其他问题

都是不依赖重算的小改。

| 问题 | 位置 | 建议 |
| --- | --- | --- |
| GeoQA 上 PROVE-style（82.10）高于 CCV（81.83） | Table 2 | 加粗按列取最优。正文如有“CCV 在所有 benchmark 上最好”之类的隐含表述，需要改 |
| 引用格式全文用了叙述式，如 “difficult Gao et al. \[2023\]” | 全文 | 括号式引用改用 \\citep |
| 参考文献格式错误 | Cobbe et al.（URL 混入正文）；Lightman et al.（ICLR 2024 误写为 2023） | 整体过一遍 bib，优先用正式发表版本 |
| checklist 末尾漏出 LaTeX 残留 “endenumerate” | L938 | 修复环境闭合 |
| checklist 第 2、3 项与修改后的正文不再一致 | checklist | 第 2 项指向新 Limitations 节；第 3 项改写为似然比命题。第 5、8 项本轮不动 |

## 本轮不做

写作 agent 本轮不要动以下内容。最后一项由 CCV/SKETCH 工程核查清单（camera-ready 前） 交给工程 agent 核查，结果回来后再开下一轮。

- **作者与致谢**：作者顺序待定，保持匿名占位。
- **图片本身**：Fig 1、Fig 2、Fig 3 的重绘及图中嵌入的数字。图注文字按 P0 修改。
- **arXiv 打包**：样式选项、代码链接、源码清理、元数据。
- **待工程核查后补**：所有 `\recheck{}` 数字的新值；训练超参与 checkpoint 选择；VGF 负对照 80.05% 的来源；两处 “400” 集合的说明；基线实现附录；完整算力记账与 checklist 第 8 项；代码发布与 checklist 第 5 项；数据与模型许可。

## 执行顺序与完成检查表

先定口径和理论，再改叙事。摘要、引言、结论的措辞都依赖 Sec 3.2 的新表述，反过来改会返工。

- [ ] 1\. 导言区加 `\recheck` 宏
- [ ] 2\. 评测口径：Table 1 / Table 2 结构、“four benchmarks”、heldout 定义，汇总数字全部包 `\recheck{}`（P0-0）
- [ ] 3\. 重写 Sec 3.2 与 App J：恒等式 + 似然比命题 + Theorem 2 定位（P0-3）
- [ ] 4\. 改引言与 Sec 2：生成顺序、耦合表、替换 0.225、改写 Principle（P0-1、P0-2）
- [ ] 5\. 改摘要、贡献、Sec 3.3、结论的 “no additional inference” 和跨领域措辞（P0-4、P0-6）
- [ ] 6\. Sec 4.6 改为双向分析，新增 Limitations 节（P0-5、P1）
- [ ] 7\. 附录：成本表、常数敏感性表（结构 + `\recheck{}`）、符号表（P0-4、P1）
- [ ] 8\. 图注文字：Fig 1、Fig 2、Fig D.1
- [ ] 9\. 全文一遍：缩写、\\citep、bib、Table 2 加粗、endenumerate（P1、P2）
- [ ] 10\. 在 tex 源码中搜索残留旧表述：independent、rare、weakly、no additional inference、training-free、0.225、uniform、dispersed、four benchmarks，逐处确认
- [ ] 11\. 更新 checklist 第 1–4、6、7 项
- [ ] 12\. 交付时附一份所有 `\recheck{}` 的位置清单（行号与原值），用于和工程 agent 的映射表对齐
