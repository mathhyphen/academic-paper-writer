# Academic Paper Writer - 学术论文写作助手

**English** | [中文](#中文文档)

## Overview

A complete academic paper writing solution that transforms your code into a professional research paper.

## Features

- 🔍 **Code Analysis**: Automatically analyze project code and extract innovations
- 📝 **Outline Design**: Generate paper structure based on conference/journal requirements
- 📄 **LaTeX Generation**: Auto-generate LaTeX content and structure
- 🎨 **Template Management**: Support IEEE, ACM, AAAI, CVPR, ICML, NeurIPS templates
- 🔍 **Review Mode**: Automated paper quality check and feedback

## Quick Start

### Installation

```bash
git clone https://github.com/yourusername/academic-paper-writer.git
cd academic-paper-writer
```

### Usage

```bash
# Full workflow
python academic_paper_writer.py "./your_project" ieee conference

# Parameters:
#   - Project path: Path to your code
#   - Template: ieee/acm/aaai/cvpr/icml/neurips
#   - Type: conference or journal
```

## Workflow

```
Code Project → Analysis → Outline Design → Template Download → LaTeX Generation → Review
```

## Supported Templates

- **IEEE Conference**: Computer science top conferences
- **ACM Conference**: ACM series conferences
- **AAAI**: AI top conference
- **CVPR**: Computer vision top conference
- **ICML**: Machine learning top conference
- **NeurIPS**: Neural information processing conference

## Output

```
papers/
└── paper_YYYYMMDD_HHMMSS/
    ├── main.tex
    ├── sections/
    ├── references.bib
    └── review_comments.json
```

## Example

```bash
# Analyze a deep learning project
python academic_paper_writer.py "./my_cnn_project" cvpr conference

# Output:
# ✅ Project type: Deep Learning / AI
# ✅ Innovations found: 4
# ✅ Paper generated: papers/paper_20260209_143052/
# ✅ Review score: 7.5/10
```

---

## 中文文档

### 简介

学术论文写作助手 - 从代码到论文的完整解决方案。

### 核心功能

1. **代码分析**
   - 自动检测项目类型
   - 提取创新点
   - 生成关键词

2. **大纲设计**
   - 根据会议要求设计结构
   - 自动生成章节框架
   - 提供写作建议

3. **LaTeX 模板**
   - 支持多种顶级会议模板
   - 自动下载和配置
   - 符合会议规范

4. **审稿模式**
   - 自动检查完整性
   - 评分系统
   - 改进建议

### 使用方法

```bash
# 完整工作流程
python academic_paper_writer.py "./你的项目" ieee conference

# 示例：分析深度学习项目，生成CVPR格式论文
python academic_paper_writer.py "./my_dl_project" cvpr conference
```

### 支持的模板

| 会议 | 命令 | 领域 |
|------|------|------|
| IEEE | `ieee` | 计算机综合 |
| ACM | `acm` | 计算机综合 |
| AAAI | `aaai` | 人工智能 |
| CVPR | `cvpr` | 计算机视觉 |
| ICML | `icml` | 机器学习 |
| NeurIPS | `neurips` | 神经信息 |

### 输出示例

```
论文目录/
├── main.tex              # 主文件
├── sections/             # 章节
│   ├── introduction.tex  # 引言
│   ├── method.tex        # 方法
│   ├── experiments.tex   # 实验
│   ├── discussion.tex    # 讨论
│   └── conclusion.tex    # 结论
├── references.bib        # 参考文献
└── review_comments.json  # 审稿意见
```

### 使用场景

1. **毕业设计**
   - 快速生成论文框架
   - 符合学校格式要求

2. **会议投稿**
   - 使用标准会议模板
   - 自动生成结构

3. **开源项目**
   - 为项目生成学术论文
   - 提升项目影响力

## License

MIT License
