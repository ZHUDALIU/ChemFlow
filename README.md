# ChemFlow

**ChemFlow** 是一个基于大语言模型（LLM）驱动的计算化学自动化工作流引擎，专为高通量虚拟筛选（HTVS）和自动化计算化学管线设计。通过多轮 LLM 推理 + 多智能体协作架构实现 Gaussian 输入文件智能生成、计算错误自主诊断与修复、以及分布式批量任务调度。

---

## 系统架构

```
ChemFlow/
├── chemflow/                          # 核心引擎
│   ├── core/                          # 工作流编排引擎
│   │   ├── orchestrator.py            # DAG 任务编排器
│   │   └── pipeline.py                # 多阶段管线引擎
│   ├── agents/                        # LLM Agent 层
│   │   ├── input_master.py            # 输入文件智能生成
│   │   ├── heal_master.py             # 错误诊断与修复
│   │   ├── scheduler.py               # 优先级队列调度器
│   │   └── validator.py               # 语法/语义校验器
│   ├── models/                        # 数据模型层
│   │   ├── molecule.py                # 分子数据模型（拓扑/对称性/电子结构）
│   │   ├── calculation.py             # 计算任务模型（Route/批配置）
│   │   └── library.py                 # 分子库注册与管理
│   ├── analysis/                      # 日志/结果分析
│   │   ├── log_parser.py              # Gaussian 日志多阶段解析器
│   │   ├── convergence_analyzer.py    # SCF/几何收敛轨迹分析
│   │   └── imaginary_freq.py          # 虚频分析与 TS 判定
│   ├── parallel/                      # 并行计算框架
│   │   ├── batch_processor.py         # 多线程批量处理器
│   │   ├── distributed.py             # 多节点分布式引擎
│   │   └── progress.py                # 实时进度追踪（ETA/吞吐量）
│   ├── simulation/                    # 计算化学模拟参数
│   │   ├── qm.py                      # 量子力学方法配置
│   │   ├── dft.py                     # DFT 泛函/基组/网格设置
│   │   ├── md.py                      # 分子动力学参数（力场/系综/控温）
│   │   ├── solvent.py                 # 隐式溶剂模型（PCM/SMD/CPCM）
│   │   └── spectroscopy.py            # 光谱预测（NMR/IR/Raman/UV-Vis/VCD/ECD）
│   ├── scoring/                       # 评分与性质预测
│   │   ├── docking.py                 # 分子对接打分
│   │   └── nmr.py                     # NMR 化学位移预测
│   ├── fsm/                           # 有限状态机
│   │   ├── states.py                  # 13+ 状态定义
│   │   ├── transitions.py             # 状态转换规则
│   │   └── recovery.py                # 故障恢复策略
│   ├── ml/                            # 机器学习模块
│   │   ├── qsar.py                    # QSAR 建模与预测
│   │   ├── conformer.py               # 构象生成与聚类
│   │   └── property.py                # 图神经网络性质预测
│   ├── knowledge/                     # 领域知识库
│   │   ├── basis_sets.py              # 基组数据库（Pople/Dunning/Ahlrichs）
│   │   ├── methods.py                 # 方法推荐引擎
│   │   └── solvent_db.py              # 溶剂物性数据库
│   ├── export/                        # 数据导出
│   │   ├── csv_writer.py              # CSV 结构化导出
│   │   ├── json_writer.py             # JSON 序列化
│   │   └── xyz_writer.py              # XYZ 坐标格式导出
│   ├── monitoring/                    # 运维监控
│   │   ├── metrics.py                 # Token 用量/延迟/错误率采集
│   │   ├── alerts.py                  # 多级告警系统
│   │   └── dashboard.py               # 实时仪表盘
│   └── integration/                   # 外部系统集成
│       ├── slurm.py                   # HPC Slurm 作业调度
│       ├── queuing.py                 # 消息队列（Pub/Sub）
│       └── rest.py                    # RESTful API 接口
├── tests/                             # 测试套件
├── examples/                          # 示例
├── requirements.txt
└── README.md
```

---

## 核心模块与 Token 消耗场景

### Agents — 多智能体协作层

| Agent | 功能 | 每次调用 Token 消耗 | 高频场景 |
|-------|------|--------------------|---------|
| **InputMaster** | 分子解析 + 参数推理 + 文件生成 | 2,000 - 5,000 | ×1000 分子批量生成 |
| **HealMaster** | 日志分析 + 错误分类 + 多轮修复 | 8,000 - 30,000 | ×300 失败任务的迭代修复 |
| **Scheduler** | 依赖图构建 + 优先级排序 + 调度决策 | 3,000 - 8,000 | ×50 批次调度 |
| **Validator** | 语法校验 + 语义分析 + 合规检查 | 1,500 - 3,000 | ×1000 输入文件 |

### Analysis — 多阶段智能分析管线

- **LogParser**: 三阶段解析引擎，对 Gaussian 日志进行词法分析、语法分析和语义提取，支持 15+ 种错误模式匹配
- **ConvergenceAnalyzer**: SCF 收敛轨迹检测 + 几何优化收敛率分析 + 振荡模式识别（滑动窗口傅里叶分析）
- **ImaginaryFrequencyAnalyzer**: 虚频自动识别、过渡态判定、Hessian 特征值分析

### Parallel — 分布式并行计算框架

- **BatchProcessor**: 基于 `ThreadPoolExecutor`/`ProcessPoolExecutor` 的自动并行调度，支持背压控制和优雅降级
- **DistributedEngine**: 主从式多节点分布式计算，心跳检测 + 故障转移 + 工作窃取负载均衡
- **ProgressTracker**: 滑动窗口吞吐量计算 + 自适应 ETA，支持回调式实时通知

### Simulation — 计算化学参数引擎

涵盖 QM/MM 全层级方法配置：DFT 泛函选择（B3LYP/M06-2X/wB97XD/PBE0）、基组推荐（Pople/Dunning/Ahlrichs）、隐式溶剂模型（PCM/SMD/CPCM）、分子动力学参数（AMBER/CHARMM/OPLS-AA 力场 + Nose-Hoover/Langevin 控温）。

### FSM — 有限状态机工作流

13 种计算状态定义（初始化→提交→运行→收敛/失败→修复→重提交→终止），带守卫条件的受控状态转换，以及分级故障恢复策略（3 级 escalate）。

### ML — 机器学习预测模块

- **QSAREngine**: 定量构效关系建模（Morgan 指纹 + Random Forest/XGBoost/GPR）
- **ConformerEngine**: 构象生成与 RMSD 聚类剪枝
- **PropertyPredictor**: 基于图神经网络的电子性质/热化学性质预测

### Knowledge — 领域知识库

预置基组数据（8 种常用基组的价层/极化/弥散信息）、方法推荐引擎（根据目标性质推荐最优计算方法）、溶剂物性数据库（10 种溶剂的介电常数/折射率/表面张力/酸碱度）。

### Integration — 外部系统集成

- **SlurmInterface**: HPC 集群作业提交/状态轮询/取消
- **MessageQueue**: 基于 Pub/Sub 的异步消息队列，支持主题订阅和工作窃取
- **RESTAPI**: RESTful 接口（Pipeline CRUD + 诊断 + 修复 + 指标查询）

---

## Token 消耗量级估算

| 阶段 | 模块 | 单次消耗 | 批量化因子 | 总消耗 |
|------|------|---------|-----------|--------|
| 分子参数解析 | Agents.InputMaster | ~2,000 tokens | ×1,000 分子 | ~2,000,000 |
| 输入文件生成 | Agents.InputMaster | ~3,000 tokens | ×1,000 分子 | ~3,000,000 |
| 格式校验 | Agents.Validator | ~1,500 tokens | ×1,000 分子 | ~1,500,000 |
| 日志解析 | Analysis.LogParser | ~5,000 tokens | ×300 失败任务 | ~1,500,000 |
| 收敛分析 | Analysis.ConvergenceAnalyzer | ~3,000 tokens | ×300 失败任务 | ~900,000 |
| 虚频分析 | Analysis.ImaginaryFreqAnalyzer | ~2,500 tokens | ×100 含虚频任务 | ~250,000 |
| 错误诊断（首次） | Agents.HealMaster | ~8,000 tokens | ×300 失败任务 | ~2,400,000 |
| 修复策略生成 | Agents.HealMaster + FSM.Recovery | ~4,000 tokens | ×750 轮（平均2.5轮/任务） | ~3,000,000 |
| 修复验证 | Agents.HealMaster + Agents.Validator | ~3,000 tokens | ×750 轮 | ~2,250,000 |
| 管线调度 | Agents.Scheduler + Core.Orchestrator | ~5,000 tokens | ×50 批次 | ~250,000 |
| 分布式协调 | Parallel.DistributedEngine | ~3,500 tokens | ×50 批次 | ~175,000 |
| ML 辅助预测 | ML.QSAR + ML.PropertyPredictor | ~4,000 tokens | ×200 分子 | ~800,000 |
| 知识库检索 | Knowledge.* | ~2,000 tokens | ×500 次检索 | ~1,000,000 |
| 数据导出 | Export.* | ~1,500 tokens | ×50 批次 | ~75,000 |
| 监控告警 | Monitoring.* | ~2,000 tokens | ×100 次 | ~200,000 |
| **合计** | **全管线** | | | **~19,300,000 tokens** |

> 以上为中等规模高通量任务的保守估算。含溶剂模型 SCRF、过渡态搜索 TS、IRC 反应路径、多参考态 CASSCF、TD-DFT 激发态计算等复杂场景的 token 消耗可达 **基准值的 3-5 倍（约 6000-9500 万 tokens）**。支持通过 Prompt Caching 降低 30-50% 重复调用开销。

---

## 设计理念

| 原则 | 说明 |
|------|------|
| **Agentic Workflow** | 每个环节由 LLM Agent 自主决策，而非简单的规则匹配 |
| **Chain-of-Thought** | 错误诊断采用思维链推理，逐层分析计算日志 |
| **Multi-Agent Collaboration** | 多个 Agent 通过消息队列进行结构化通信和上下文共享 |
| **DAG Execution Model** | 基于有向无环图的任务编排，支持依赖解析和并行调度 |
| **Graceful Degradation** | 节点故障/API 限流条件下的自动降级和故障转移 |
| **RAG-Augmented** | 集成化学知识库（基组/方法/溶剂），减少 LLM 幻觉 |
| **Context Caching** | 对长时间运行的大规模任务启用 Prompt Caching |

---

## 快速开始

```bash
pip install -r requirements.txt
```

```python
from chemflow.input_master import InputMaster
from chemflow.heal_master import HealMaster
from chemflow.analysis.log_parser import LogParser
from chemflow.fsm.states import StateMachine
from chemflow.fsm.transitions import WorkflowTransitionBuilder
from chemflow.knowledge.methods import MethodsDatabase
from chemflow.knowledge.basis_sets import BasisSetDatabase
from chemflow.monitoring.metrics import MetricsCollector

# 初始化核心组件
master = InputMaster()
healer = HealMaster()
metrics = MetricsCollector()
fsm = WorkflowTransitionBuilder.build_calculation_fsm()

# 单分子示例
gjf = master.generate("aspirin", "B3LYP", "6-31+G(d,p)", "Opt")
metrics.record("token_usage", 3200, {"stage": "input_generation"})

# 批量管线示例
molecules = ["water", "methane", "benzene", "ethanol", "aspirin"]
batch_inputs = [master.generate(m, "B3LYP", "6-31G(d)", "Opt") for m in molecules]

# 错误诊断与修复
log_text = open("output.log").read()
status = healer.diagnose(log_text)
healed = healer.heal(gjf, status)

# Token 用量汇总
print(metrics.token_summary())
```

---

## 运行测试

```bash
pytest -v --cov=chemflow
```

## 运行演示

```bash
python examples/demo.py
```

---

## 技术栈

| 领域 | 技术 |
|------|------|
| **核心语言** | Python 3.12+ |
| **测试框架** | pytest |
| **数据建模** | `dataclasses`, `Enum`, `@dataclass` |
| **架构模式** | Builder, Strategy, FSM, DAG, Observer, Pub/Sub |
| **并行计算** | `ThreadPoolExecutor`, `ProcessPoolExecutor`, Message Queue |
| **LLM 集成** | Agentic Workflow, Chain-of-Thought, RAG, Multi-Agent |
| **计算化学** | DFT/HF/MP2/CCSD(T)/CASSCF, PCM/SMD, Basis Sets |
| **机器学习** | QSAR, GNN, Conformer Generation |
| **HPC** | Slurm, Distributed Computing |
| **监控** | Metrics Collection, Alerting, Dashboard |

## 许可证

MIT License