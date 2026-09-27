# 写作修订说明（2026-09-27）

本版按 `task/写作task.md` 修改正文、理论、实验解释、附录和 checklist；不重算实验。摘要优先采用本轮消息明确给定的原文，只做 LaTeX 排版转义，并为汇总数字添加 `\recheck{}`。这是待工程核查的工作稿，不是已完成数据重算的 camera-ready 稿。

## 摘要与任务书的冲突

给定摘要保留了 `structurally independent`、`independently converge`、`four geometry benchmarks`、`no ... extra inference` 和未限定几何领域的末句。这些表述与任务书要求以及修订后的正文冲突。已在摘要源码注释和 checklist 第 1 项明确记录；未擅自改写用户指定摘要。提交前需决定是否将这些句子统一为：结构不同但正相关、三个主集合及 GPS-full 参考、仅已有 SKETCH 池上的验证无需额外模型调用，以及限于几何的验证结论。

## 叙事结构与段落作用

| 部分 | 段落作用与修改 |
| --- | --- |
| Introduction | 问题：共享图像导致相关错误；方法：生成顺序及通道耦合；原理：似然比条件；贡献：结构化格式、验证器和适用范围。 |
| SKETCH / Method | 先交代单次生成与外部执行，再定义信号、精度恒等式及似然比命题，最后给出选择算法、回退与成本。 |
| Experiments | 明确三个主集合和参考超集，保留逐集合数值；随后比较方法、模型、候选预算、特征及双向损益。 |
| Limitations / Conclusion | 分别说明生成耦合、教师与 SFT 依赖、格式退化、任务边界和 oracle 余量；结论将跨领域收益列为可证伪假设。 |
| Appendices | 保留 A–I 的实验内容，重写 J 的理论，新增 K 的回退分析、L 的成本、M 的常数敏感性结构和 N 的符号表。 |

## 任务核对

| 任务 | 状态 |
| --- | --- |
| P0-0 评测口径 | 主集合为 Geometry3K、GeoQA、GPS-clean；GPS-full 为超集参考，主表最右以竖线分隔；All/OOD 原值标红。摘要例外见上。 |
| P0-1 / P0-2 通道耦合 | 加入生成顺序、claim 条件依赖、段落顺序统计、φ 小表及 0.736 对 0.617；正文删除 0.225 与弱耦合叙述。 |
| P0-3 理论 | Theorem 1 只保留精度恒等式；新增似然比 iff 命题、精确赔率恒等式及证明；删除分散假设推论；明确 SNR 不保证池级收益。 |
| P0-4 / P0-6 成本与范围 | 正文收窄为已有 SKETCH 池上的验证无额外模型调用；交代教师流程与 LoRA SFT；新增成本表和跨领域预测试。摘要例外见上。 |
| P0-5 双向分析 | 加入两组 win/loss、两个交换表、三类回退及恢复图范围说明；不自行填补或修正冲突计数。 |
| P1 Limitations | 独立五段，覆盖闭源 few-shot 未测试、证明题需 proof checker、格式退化、oracle 与选择边界。 |
| P1 其余常数 | 写明已有定性观察，缺失 accuracy 填 `\recheck{pending}`；未编造网格或端点；证明 +1 bonus 不影响 argmax。 |
| P1 符号、缩写、发布承诺 | 新增符号表；补齐 VGF、DSL、MV、CISC、PRM、GPS-c、s240 等定义；正文写明计划发布的脚本、冻结池、逐题选择、scorer 文件和 audit。 |
| P2 排版与参考文献 | 保留 GeoQA 上 PROVE-style 的最优加粗；括号引用改 `\citep`；修正 bib；清理重复 document 尾部及 checklist 泄漏文本。 |
| Checklist | 修改第 1–4、6、7 项；当前未统一摘要、未完成重算及工程复现核查的项目如实标 No；第 5、8 项保持原文。另将第 10 项成本表述收窄。 |
| 交付映射 | `recheck_locations.md` 列出每处宏的文件、源码行号、原值和上下文。图内旧数字按任务书不改，已在图注说明。 |

## Claim–evidence 核对

| Claim | Evidence | Status |
| --- | --- | --- |
| 一致过滤提高精度，当且仅当正确执行的一致概率更高 | Proposition 1、Appendix J 三行证明及赔率恒等式 | supported（精确条件，不依赖独立性） |
| 两通道存在正相关 | 新耦合表及 0.736 对 0.617；数值均标红 | needs recomputation |
| Qwen / Gemma 的一致过滤改善候选精度 | Appendix J 似然比表、Gemma 40.2% 假一致反例、原诊断表 | needs recomputation；不推导池级保证 |
| 三主集合上的 CCV 收益 | 主表保留逐集合准确率；All/OOD 与模型汇总标红 | 单集合原值保留；汇总 needs recomputation |
| CCV 也会把正确答案改错 | 两个交换表及回退分类 | needs recomputation / count reconciliation |
| 验证阶段无额外模型调用 | 算法仅聚合已有 claim 和外部执行结果；成本表区分教师、SFT、执行与外部 scorer | supported within stated scope；完整成本台账待工程核查 |
| 可推广到几何以外 | 尚无实验，仅提出先测似然比再测选择收益 | hypothesis；未当作已证实结果 |

## 五维自审与待核查

| 维度 | 结论 |
| --- | --- |
| 贡献 | 保留 SKETCH 格式与 CCV 的可检验贡献；未将精度命题表述成池级胜出定理。 |
| 写作清晰度 | 正文术语和因果链已统一；指定摘要仍需作者决定是否同步。 |
| 实验强度 | 逐集合值未动；所有受重叠影响的汇总、置信区间与显著性结果均待重算。 |
| 评测完整性 | 补充了回退和成本；敏感性数值、基线实现、checkpoint 等按任务书留给工程轮。 |
| 方法合理性 | 标明生成耦合、错误一致、错误回退、选择无法创造正确候选等边界；SNR 比值条件补充 `p_e > 1/2` 限制，Gemma 需比较带符号的 SNR。 |

原恢复流图的 `123/139` 与交换表相对 EAV 的 `121` wins 尚未对齐，原 `355` 条失败分析也需与交换表统一；任务书提供的 EAV 回退分类尚非穷尽分解。均原样保留并标注，未补造残余类别。`80.05%` 负对照、两处 `400` 集合、超参/checkpoint、完整算力及许可仍按任务书留待工程核查。

原图文件、作者匿名占位、样式选项及 arXiv 打包未修改。新增材料使主文延伸至第 10 页；最终版需在确定投稿篇幅要求后单独压缩，不在本轮通过改样式压页数。

## 参考文献核验来源

Cobbe 的标题和 arXiv 字段依据[原论文](https://arxiv.org/abs/2110.14168)修正；Lightman 的 ICLR 2024 年份及作者拼写依据[正式论文](https://proceedings.iclr.cc/paper_files/paper/2024/file/aca97732e30bcf1303bc22ac3924fd16-Paper-Conference.pdf)修正。Self-consistency 改用 [ICLR 2023](https://research.google/pubs/self-consistency-improves-chain-of-thought-reasoning-in-language-models/)；MathVista 改用 [ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/file/663bce02a0050c4a11f1eb8a7f1429d3-Paper-Conference.pdf)。

GenRM、GeoX、MAVIS 分别采用正式 [GenRM ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/214308a2d5e3f83ef9ad2739e1cbc46d-Abstract-Conference.html)、[GeoX ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/2722a0ccf6acfe3d144fdbb0dedd80b5-Abstract-Conference.html)、[MAVIS ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/db36dcad6baee298a34ffca324b84b09-Abstract-Conference.html)元数据；URSA 的不完整 arXiv 字段依据[原论文](https://arxiv.org/abs/2501.04686)修复。保留所有引用键，未声称其余预印本不存在正式版本。

## 验证记录

最终 Tectonic 编译通过（29 页）；23 个引用键均存在，包含 checklist 与输入图文件的交叉引用检查通过。PDF 无未解析引用、替换字符或泄漏的 LaTeX 环境文本；日志无 overfull box 或缺字。静态核对确认主表所有原数值、匿名作者、checklist 第 5/8 项和图文件未改。共生成 291 处 recheck 映射。保留宏包编码注释及少量 underfull 排版警告；页面渲染已逐页检查，并调整了代码示例跨页和符号表页首位置。
