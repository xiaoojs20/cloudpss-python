# CloudPSS Python SDK 自动化仿真项目

本项目集成了 CloudPSS Python SDK，旨在对特定的风电集电系统模型进行自动化仿真、参数扫描及报告生成。

## 项目结构

- `run_simulation.py`: 基础仿真脚本，支持获取模型、运行仿真及自动绘制波形图。
- `extract_jibei.py`: 从 CloudPSS 平台提取“方案-冀北”的所有参数，并生成 `jibei_parameters.md`。
- `jibei_baseline.py`: 针对“方案-冀北”配置运行的基准仿真脚本。
- `power_sweep.py`: **核心功能脚本**。针对风电出力（P_WT2WF 与 P_WF_Other）进行 11 次步进扫描（0% - 100% 额定容量），并生成对比分析图像。
- `report/`: 包含 LaTeX 报告源码及编译生成的 PDF 报告。
- `figures/`: 存放仿真生成的波形图及参数扫描趋势图。

## 快速开始

### 1. 环境准备

确保已安装 Python 3.8+ 及相关依赖库：

```bash
pip install cloudpss matplotlib plotly
```

如需编译 PDF 报告，建议安装 [Tectonic](https://tectonic-typesetting.github.io/):

```bash
brew install tectonic
```

### 2. 配置 Token

在脚本中替换您的 CloudPSS SDK Token：

```python
TOKEN = "您的_CLOUDPSS_TOKEN"
```

### 3. 运行仿真

运行完整的风电出力参数扫描：

```bash
python3 power_sweep.py
```

## 关键参数说明 (方案-冀北)

| 参数 ID | 说明 | 扫描范围 |
| --- | --- | --- |
| `P_WT2WF` | 风电机组出力 (MW) | 0 - 100 |
| `P_WF_Other` | 其他风电场出力 (MW) | 0 - 900 |
| `Freq_WT` | 风机运行频率 (Hz) | 固定 (20Hz) |

## 注意事项

- **实时状态轮询**: 在某些网络环境下，SDK 的 `runner.status()` 可能因 Websocket 连接中断而发生长时间挂起。本项目脚本已集成了超时处理和容错逻辑。
- **图像保存**: 所有仿真生成的图像均会自动存放在 `figures/` 目录下，命名规则为 `sweep_{step}_plot_{index}.png`。

---
```
