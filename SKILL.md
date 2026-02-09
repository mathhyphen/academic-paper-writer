---
name: academic-paper-writer
version: 1.0.0
description: |
  学术论文写作助手 - 从代码到论文的完整解决方案
  支持代码分析、大纲设计、LaTeX生成、模板下载、审稿反馈
---

# Academic Paper Writer - 学术论文写作助手

## 功能特性

### 1. 代码分析 (Code Analysis)
- 自动检测项目类型（深度学习/系统/软件等）
- 统计代码结构和规模
- 提取关键文件和内容
- 自动生成创新点和关键词

### 2. 论文大纲设计 (Outline Design)
- 根据会议/期刊类型设计结构
- 自动生成各章节框架
- 提供内容要点建议

### 3. LaTeX 模板管理 (Template Management)
- 支持多种会议模板：
  - IEEE Conference
  - ACM Conference
  - AAAI
  - CVPR
  - ICML
  - NeurIPS
- 自动下载和配置模板

### 4. LaTeX 内容生成 (LaTeX Generation)
- 自动生成论文框架
- 分章节管理
- 集成参考文献

### 5. 审稿人模式 (Review Mode)
- 自动检查论文完整性
- 评分系统（1-10分）
- 提供改进建议

## 使用方法

### 完整工作流程

```bash
# 分析项目代码并生成完整论文
python academic_paper_writer.py <项目路径> <模板> <类型>

# 示例
python academic_paper_writer.py "./my_ai_project" ieee conference
```

### 分步骤使用

```python
from academic_paper_writer import AcademicPaperWriter

writer = AcademicPaperWriter()

# 1. 分析代码
analysis = writer.analyze_code("./my_project")

# 2. 设计大纲
outline = writer.design_outline(analysis, "conference")

# 3. 下载模板
template_dir = writer.download_template("ieee")

# 4. 生成 LaTeX
paper_dir = writer.generate_latex(outline, template_dir, output_dir)

# 5. 审稿
review = writer.review_paper(paper_dir)
```

## 支持的模板

| 会议/期刊 | 命令 | 说明 |
|-----------|------|------|
| IEEE Conference | `ieee` | 计算机领域顶级会议 |
| ACM Conference | `acm` | ACM系列会议 |
| AAAI | `aaai` | AI顶会 |
| CVPR | `cvpr` | 计算机视觉顶会 |
| ICML | `icml` | 机器学习顶会 |
| NeurIPS | `neurips` | 神经信息处理顶会 |

## 输出结构

```
papers/
└── paper_20260209_143052/
    ├── main.tex              # 主文件
    ├── sections/             # 章节目录
    │   ├── introduction.tex
    │   ├── method.tex
    │   ├── experiments.tex
    │   ├── discussion.tex
    │   └── conclusion.tex
    ├── references.bib        # 参考文献
    ├── meta.json            # 元数据
    ├── review_comments.json # 审稿意见
    └── workflow_report.json # 完整报告
```

## 依赖

- Python 3.9+
- 标准库：pathlib, json, datetime, urllib

## 作者

AI Academic Assistant
