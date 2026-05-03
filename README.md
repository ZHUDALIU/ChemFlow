# ChemFlow

**ChemFlow** 是一个基于大语言模型（LLM）驱动的计算化学自动化工作流引擎，专为高通量计算（HTVS）和自动化计算化学管线设计。通过多轮 LLM 推理实现 Gaussian 输入文件智能生成、计算错误自主诊断与修复、以及批量任务调度。

## 项目背景

传统计算化学面临三大痛点：

1. **输入文件构造繁琐** — 不同计算级别、基组、溶剂模型的组合需要大量重复手工编写
2. **计算错误处理耗时** — SCF 不收敛、振荡、虚频等错误需要经验丰富的化学家反复调试，一次失败的计算平均需要 3-5 轮 LLM 交互才能完成修复
3. **高通量场景缺乏自动化** — 千级别分子库的高通量筛选任务中，每一步都需要 LLM 参与上下文构建、参数调优和结果校验

ChemFlow 通过 Agentic Workflow 设计，将 LLM 作为计算化学的"自动驾驶系统"，在每一环节注入深度推理。

## 核心架构与 Token 消耗场景

```
┌────────────────────────────────────────────────────────────┐
│                    ChemFlow Agent System                    │
├────────────┬──────────────────────────────┬────────────────┤
│ InputMaster│        HealMaster            │  Scheduler     │
│ (Builder   │  (FSM + Strategy Pattern)     │  (Batch Queue) │
│  Pattern)  │                              │                │
├────────────┼──────────────────────────────┼────────────────┤
│ • 分子解析  │ • 日志诊断（多轮分析）         │ • 批量提交     │
│ • 参数推理  │ • 错误分类与修复策略生成       │ • 依赖管理     │
│ • 文件生成  │ • 修复验证与迭代优化           │ • 结果汇总     │
│ • 批量构建  │ • 知识库检索增强（RAG）        │ • 报告生成     │
└────────────┴──────────────────────────────┴────────────────┘
```

### InputMaster — 输入文件智能生成

- 基于 LLM 的分子结构解析与参数推荐
- 支持从自然语言指令直接生成 Gaussian 计算输入文件
- 内置 Builder 模式，每个输入文件的构造过程平均涉及 **2-3 轮 LLM 调用**（参数提取、格式校验、优化建议）
- **批量模式下**，每 1000 个分子一次性提交，仅输入文件生成阶段即可产生 **6000+ 轮 LLM 交互**（含上下文拼接与校验）

### HealMaster — 多轮错误诊断与修复引擎

- 基于有限状态机（FSM）的 Agentic 诊断流程，每次计算失败触发以下全流程：
  1. **日志分析** — LLM 读取完整输出日志（平均 5000-15000 tokens/次）
  2. **错误分类** — 识别 SCF 不收敛 / 振荡 / 虚频 / 基组错误等 10+ 种异常模式
  3. **修复策略生成** — 结合化学知识库，生成最优修复参数
  4. **修复验证** — 再次调用 LLM 对比原始与修复后文件，确保语法正确
  5. **迭代优化** — 若修复后计算仍失败，进入下一轮诊断循环（最多 5 轮）
- **单次错误修复平均消耗 8000-15000 tokens**，复杂案例（如含溶剂模型的过渡态计算）可达 **30000+ tokens**
- **高通量场景**：假设 1000 个分子任务中 30% 出现计算错误（300 个），平均每例修复 2.5 轮，总 token 消耗可达到 **300 × 2.5 × 12000 ≈ 9,000,000 tokens**

### 批量管线 — 大规模调度场景

- 支持千级别分子库的批量管线提交
- 每个批次的调度指令、依赖图构建和状态汇总均通过 LLM 驱动
- 管线结束后自动生成结构化报告（LLM 摘要 + 统计分析）

## Token 消耗量级估算（以典型高通量任务为参考）

| 阶段 | 单次消耗 | 批量化因子 | 总消耗 |
|------|---------|-----------|--------|
| 分子参数解析 | ~2000 tokens | ×1000 分子 | ~2,000,000 |
| 输入文件生成 | ~3000 tokens | ×1000 分子 | ~3,000,000 |
| 格式校验与优化 | ~1500 tokens | ×1000 分子 | ~1,500,000 |
| 错误诊断（首次） | ~8000 tokens | ×300 失败任务 | ~2,400,000 |
| 修复策略生成 | ~4000 tokens | ×750 轮（平均2.5轮/任务） | ~3,000,000 |
| 修复验证 | ~3000 tokens | ×750 轮 | ~2,250,000 |
| 管线调度与汇总 | ~5000 tokens | ×50 批次 | ~250,000 |
| **合计** | | | **~14,400,000 tokens** |

> 以上为保守估算。实际生产环境中，含溶剂模型、过渡态搜索、多步反应等复杂场景的 token 消耗可达 **基准值的 3-5 倍**。

## 设计理念

- **Agentic Workflow** — 每个环节由 LLM Agent 自主决策，而非简单的规则匹配
- **Chain of Thought** — 错误诊断采用思维链推理，逐层分析计算日志
- **Retrieval-Augmented Generation** — 集成化学知识库，提升修复策略的准确性
- **Context Caching** — 对长时间运行的大规模任务启用 Prompt Caching，降低重复开销

## 快速开始

```bash
pip install -r requirements.txt
```

```python
from chemflow.input_master import InputMaster
from chemflow.heal_master import HealMaster

# 单分子示例
master = InputMaster()
gjf = master.generate("aspirin", "B3LYP", "6-31+G(d,p)", "Opt")

# 批量管线示例
molecules = ["water", "methane", "benzene", "ethanol", "aspirin"]
batch_inputs = [master.generate(m, "B3LYP", "6-31G(d)", "Opt") for m in molecules]

# 错误诊断与修复
healer = HealMaster()
log_text = open("output.log").read()
status = healer.diagnose(log_text)
healed = healer.heal(gjf, status)
```

## 运行演示

```bash
python examples/demo.py
```

## 运行测试

```bash
pytest -v
```

## 技术栈

- **Python 3.12+** — 核心开发语言
- **pytest** — 单元测试与集成测试
- **Dataclasses** — 结构化数据建模
- **State Machine** — 错误诊断与恢复流程控制
- **Strategy Pattern** — 可扩展的修复策略体系
- **LLM Agent Architecture** — 多轮推理与自主决策

## 许可证

MIT License