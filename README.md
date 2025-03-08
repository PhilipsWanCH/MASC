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
- **Flexible Scheduling Capabilities:** Supports both **simulated** and **real-world** execution.
- **Knowledge Retention via DialBag:** Improves scheduling efficiency without forgetting previous knowledge.

---

## Requirements
- **Python >= 3.8**
- **PyTorch >= 1.12.0 (2.0.0 and above are recommended)**
- **Transformers >= 4.38**

---

## Datasets and Benchmarks

**ARC** (AI2 Reasoning Challenge) [1]: A dataset for testing machine reasoning abilities.

**HellaSwag** [2]: A dataset designed to evaluate commonsense reasoning in language models.

**MMLU **(Massive Multitask Language Understanding) [3]: A dataset covering various knowledge domains for evaluating LLM generalization.

**SchedQA**: A dataset specifically generated using the gen_ReAct_data script to evaluate scheduling-related question-answering performance.

[1] P. Clark, I. Cowhey, et al., “Think you have solved question answering? Try ARC, the AI2 reasoning challenge,” 2018, arXiv:1803.05457.

[2] R. Zellers, A. Holtzman, et al., “HellaSwag: Can a Machine Really Finish Your Sentence?,” in Proc. 57th Annu. Meet. Assoc. Comput. Linguistics, pp. 4791-4800, July 2019, Florence, Italy.

[3] D. Hendrycks, C. Burns, et al., “Measuring Massive Multitask Language Understanding,” in Proc. Int. Conf. Learn. Representations (ICLR), 2021.

---

## Experiment & Results
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
  author={Zelong Wang,Chenhui Wan,Jie Liu,Xi Zhang,Haifeng Wang,Youmin Hu,Zhongxu Hu.},
  journal={Advanced Engineering Informatics},
  year={2025}
}
```

---

## Acknowledgments
This work was supported in part by the National Key Research and Development Program of China (No. 2023YFD2100905), National Natural Science Foundation of China (No. 52205104).
