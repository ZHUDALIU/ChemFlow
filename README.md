# ChemFlow

ChemFlow 是一个利用大语言模型（LLM）自动化 Gaussian 输入文件生成和计算错误修复的计算化学辅助工具。

## 核心特性

- **InputMaster** — 基于 Builder 模式和状态机设计，支持高通量计算场景的 Gaussian 输入文件（.gjf）自动构造
- **HealMaster** — 智能检测 Gaussian 计算日志中的常见错误（SCF 不收敛、振荡、虚频等），自动修复输入文件并重提交
- **内置分子库** — 预置水、甲烷、苯、阿司匹林、乙醇等常见分子坐标，开箱即用

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

```python
from chemflow.input_master import InputMaster
from chemflow.heal_master import HealMaster

# 生成输入文件
master = InputMaster()
gjf = master.generate("aspirin", "B3LYP", "6-31+G(d,p)", "Opt")

# 诊断与修复
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