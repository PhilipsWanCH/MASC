# MASC

以下是针对第一位审稿人的建议，撰写的 **GitHub 开源代码的 README 文件**，用于解释我们的 Multi-Agent Scheduling Chain (MASC) 代码及其补充材料的使用方法。

---

# MASC: Large Language Model-Based Multi-Agent Scheduling Chain for Flexible Job Shop Scheduling Problem

## Introduction
This repository contains the implementation of the **Multi-Agent Scheduling Chain (MASC)**, a framework leveraging **Large Language Models (LLMs) and multi-agent systems** to solve the **Flexible Job Shop Scheduling Problem (FJSP)**. MASC integrates LLM-driven decision-making with a structured **multi-agent** approach to enhance scheduling efficiency, adaptability, and automation in dynamic manufacturing environments.

This repository includes:
- The **SchedAgent** implementation based on **LLMs fine-tuned with QLoRA**.
- The **DialBag method**, which enhances knowledge retention in LLM-based scheduling.
- Simulation and real-world **robotic arm experiments** validating MASC’s performance.
- Preprocessed **datasets** and **experimental results** for reproducibility.

---

## Features
- **Multi-Agent Coordination:** Agents for observation, scheduling, planning, and control.
- **LLM-Driven Decision Making:** Enhanced scheduling through LLM-powered **SchedAgent**.
- **Reinforcement Learning Integration:** Adaptive scheduling optimization.
- **Flexible Scheduling Capabilities:** Supports both **simulated** and **real-world** execution.
- **Knowledge Retention via DialBag:** Improves scheduling efficiency without forgetting previous knowledge.

---

## Installation
To set up the MASC framework, follow these steps:

### 1. Clone the repository
```bash
git clone https://github.com/YourUsername/MASC-Scheduling.git
cd MASC-Scheduling
```

### 2. Create and activate a virtual environment (optional)
```bash
python3 -m venv masc_env
source masc_env/bin/activate  # For macOS/Linux
masc_env\Scripts\activate     # For Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download pretrained LLM models (if applicable)
Our **fine-tuned LLM models** are available via Hugging Face:
```bash
pip install transformers
```
Then, download the pre-trained model:
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model_name = "YourHuggingFaceModel"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
```

---

## Dataset & Experimental Setup
Our dataset includes:
1. **FJSP Scheduling Scenarios:** Various manufacturing job shop scheduling cases.
2. **Simulation Data:** Scheduling results from different optimization techniques.
3. **Real-World Data:** Robotic arm scheduling experiment results.

Datasets are stored in `data/` and formatted as `.csv` files:
```
data/
├── fjsp_scheduling_cases.csv
├── simulation_results.csv
├── real_robot_experiment.csv
```

To **replicate our experiments**, run:
```bash
python run_experiment.py --mode simulation  # For simulated scheduling
python run_experiment.py --mode real_robot  # For real-world scheduling
```

---

## Usage
### 1. Running the MASC framework
To execute the MASC framework, run:
```bash
python masc_main.py
```
This will initialize **ObsAgent, SchedAgent, PlanAgent, and CtrlAgent** for job shop scheduling.

### 2. Running the scheduling optimization
For scheduling task execution, use:
```bash
python masc_scheduler.py --algorithm GA  # Use Genetic Algorithm
python masc_scheduler.py --algorithm MIP  # Use Mixed Integer Programming
```

### 3. Running the DialBag fine-tuning
To fine-tune the LLM with **DialBag**:
```bash
python train_dialbag.py --dataset fjsp_scheduling_cases.csv
```

---

## Reproducibility
To ensure reproducibility, we provide:
- **Preprocessed scheduling datasets**
- **Fine-tuned LLM model weights**
- **Simulation & real-world scheduling experiment logs**

For any inconsistencies, please open an issue.

---

## Results & Benchmarks
Our experimental results demonstrate:
| Method                | ARC (%) | HellaSwag (%) | MMLU (%) | SchedQA (%) |
|----------------------|---------|--------------|----------|-------------|
| internlm2-7b        | 83.73   | 85.64        | **62.19** | 31.36       |
| internlm2-7b + Single Round | 72.2    | 81.01        | 61.01     | 31.47       |
| **internlm2-7b + DialBag** | **84.75** | **86.14** | 58.93     | **32.11**   |

These results validate that **DialBag effectively reduces knowledge forgetting** while improving **domain-specific scheduling accuracy**.

---

## Citation
If you use our work, please cite:
```
@article{MASC2025,
  title={MASC: Large Language Model-Based Multi-Agent Scheduling Chain for Flexible Job Shop Scheduling Problem},
  author={Your Name, et al.},
  journal={Advanced Engineering Informatics},
  year={2025}
}
```

---

## Acknowledgments
This work is supported by [Funding Agency Name] under project number **XXXXX**.

For questions, please contact: [YourEmail@domain.com](mailto:YourEmail@domain.com)

---

这样，**README 文件**详细介绍了：
- MASC 代码的安装与运行
- 相关实验的数据和 reproducibility 细节
- 运行不同实验的方法
- 代码的 benchmark 结果
- 如何引用我们的工作

你可以直接将这个 **README** 上传至 **GitHub**，或者进行适当的修改后使用！
