#!/usr/bin/env python3
"""
Academic Paper Writer - 


1. 
2. 
3.  LaTeX 
4.  LaTeX 
5.  Overleaf
6. 
"""

import os
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import urllib.request
import zipfile
import shutil


class AcademicPaperWriter:
    """"""
    
    def __init__(self, workspace: str = None):
        self.workspace = Path(workspace) if workspace else Path(r"D:\apps\academic-paper-writer")
        self.output_dir = self.workspace / "papers"
        self.output_dir.mkdir(exist_ok=True)
        self.templates_dir = self.workspace / "templates"
        self.templates_dir.mkdir(exist_ok=True)
        
        # /
        self.supported_templates = {
            "ieee": {
                "name": "IEEE Conference",
                "url": "https://www.ieee.org/content/dam/ieee-org/ieee/web/org/conferences/conference-template-letter.docx",
                "format": "docx",
                "overleaf_template": "ieee-conference"
            },
            "acm": {
                "name": "ACM Conference",
                "url": "https://www.acm.org/binaries/content/assets/publications/article-templates/acmart-primary.zip",
                "format": "zip",
                "overleaf_template": "acm-conference"
            },
            "aaai": {
                "name": "AAAI Conference",
                "url": "https://www.aaai.org/Publications/Templates/AuthorKit24.zip",
                "format": "zip",
                "overleaf_template": "aaai"
            },
            "cvpr": {
                "name": "CVPR/IEEE CVF",
                "url": "https://github.com/cvpr-org/author-kit/archive/refs/heads/main.zip",
                "format": "zip",
                "overleaf_template": "cvpr"
            },
            "icml": {
                "name": "ICML",
                "url": "https://icml.cc/Conferences/2024/Styles/icml2024.zip",
                "format": "zip",
                "overleaf_template": "icml"
            },
            "neurips": {
                "name": "NeurIPS",
                "url": "https://media.neurips.cc/Conferences/NIPS2023/Styles/neurips_2023.zip",
                "format": "zip",
                "overleaf_template": "neurips"
            }
        }
    
    def analyze_code(self, project_path: str) -> Dict:
        """
        
        
        Args:
            project_path: 
            
        Returns:
            Dict: 
        """
        project_path = Path(project_path)
        
        if not project_path.exists():
            return {"error": "Project path does not exist"}
        
        print(f" : {project_path}")
        
        # 1. 
        project_type = self._detect_project_type(project_path)
        
        # 2. 
        code_stats = self._analyze_code_structure(project_path)
        
        # 3. 
        key_files = self._extract_key_files(project_path)
        
        # 4. 
        innovations = self._generate_innovations(project_type, code_stats, key_files)
        
        return {
            "project_type": project_type,
            "code_stats": code_stats,
            "key_files": key_files,
            "innovations": innovations,
            "suggested_keywords": self._generate_keywords(project_type, innovations)
        }
    
    def _detect_project_type(self, project_path: Path) -> str:
        """"""
        files = list(project_path.rglob("*"))
        file_names = [f.name.lower() for f in files]
        
        if any("model" in f or "train" in f for f in file_names):
            if any(f.endswith('.py') for f in file_names):
                return "Deep Learning / AI"
            elif any(f.endswith('.ipynb') for f in file_names):
                return "ML Research / Jupyter"
        
        if "requirements.txt" in file_names or "setup.py" in file_names:
            return "Python Project"
        
        if any(f.endswith('.cpp') or f.endswith('.c') for f in file_names):
            return "System / C++"
        
        return "General Software"
    
    def _analyze_code_structure(self, project_path: Path) -> Dict:
        """"""
        stats = {
            "total_files": 0,
            "total_lines": 0,
            "languages": {},
            "main_modules": []
        }
        
        for file_path in project_path.rglob("*"):
            if file_path.is_file() and file_path.stat().st_size < 1024*1024:  # 1MB
                try:
                    suffix = file_path.suffix.lower()
                    if suffix in ['.py', '.cpp', '.c', '.h', '.java', '.js', '.ts']:
                        stats["total_files"] += 1
                        stats["languages"][suffix] = stats["languages"].get(suffix, 0) + 1
                        
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = len(f.readlines())
                            stats["total_lines"] += lines
                            
                        # 
                        if suffix == '.py' and file_path.stat().st_size > 1000:
                            stats["main_modules"].append(file_path.name)
                except:
                    continue
        
        return stats
    
    def _extract_key_files(self, project_path: Path) -> List[Dict]:
        """"""
        key_files = []
        
        #  README
        readme_files = list(project_path.glob("README*"))
        if readme_files:
            try:
                with open(readme_files[0], 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()[:2000]
                    key_files.append({
                        "type": "readme",
                        "name": readme_files[0].name,
                        "content_preview": content
                    })
            except:
                pass
        
        #  main 
        main_files = [
            f for f in project_path.rglob("*.py")
            if 'main' in f.name.lower() or 'train' in f.name.lower()
        ][:3]
        
        for f in main_files:
            try:
                with open(f, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()[:1500]
                    key_files.append({
                        "type": "source",
                        "name": f.name,
                        "content_preview": content
                    })
            except:
                pass
        
        return key_files
    
    def _generate_innovations(self, project_type: str, code_stats: Dict, key_files: List) -> List[str]:
        """"""
        innovations = []
        
        if "Deep Learning" in project_type or "ML" in project_type:
            innovations.extend([
                "/",
                "",
                "",
                ""
            ])
        else:
            innovations.extend([
                "/",
                "/",
                "",
                ""
            ])
        
        # 
        if code_stats["total_lines"] > 1000:
            innovations.append("1000")
        
        if len(code_stats.get("languages", {})) > 1:
            innovations.append("")
        
        return innovations[:5]
    
    def _generate_keywords(self, project_type: str, innovations: List) -> List[str]:
        """"""
        keywords = []
        
        if "Deep Learning" in project_type:
            keywords.extend(["Deep Learning", "Neural Networks", "Machine Learning"])
        elif "System" in project_type:
            keywords.extend(["System Design", "Software Engineering"])
        
        keywords.extend(["Innovation", "Performance Optimization", "Open Source"])
        
        return keywords[:5]
    
    def design_outline(self, code_analysis: Dict, paper_type: str = "conference") -> Dict:
        """
        
        
        Args:
            code_analysis: 
            paper_type:  (conference/journal)
            
        Returns:
            Dict: 
        """
        print(" ...")
        
        if paper_type == "conference":
            outline = {
                "title": f"[Title]: {code_analysis['project_type']} Based [Key Innovation]",
                "abstract": {
                    "sections": ["Background", "Method", "Results", "Conclusion"],
                    "word_count": 150
                },
                "sections": [
                    {
                        "title": "1. Introduction",
                        "subsections": [
                            "1.1 Background and Motivation",
                            "1.2 Related Work",
                            "1.3 Our Contributions"
                        ],
                        "content_points": code_analysis["innovations"]
                    },
                    {
                        "title": "2. Methodology",
                        "subsections": [
                            "2.1 Problem Formulation",
                            "2.2 Proposed Approach",
                            "2.3 Implementation Details"
                        ]
                    },
                    {
                        "title": "3. Experiments",
                        "subsections": [
                            "3.1 Experimental Setup",
                            "3.2 Results and Analysis",
                            "3.3 Ablation Studies"
                        ]
                    },
                    {
                        "title": "4. Discussion",
                        "subsections": [
                            "4.1 Limitations",
                            "4.2 Future Work"
                        ]
                    },
                    {
                        "title": "5. Conclusion",
                        "subsections": ["Summary of contributions"]
                    }
                ],
                "keywords": code_analysis["suggested_keywords"],
                "references_count": 25
            }
        else:  # journal
            outline = {
                "title": f"[Title]: Comprehensive Study on {code_analysis['project_type']}",
                "sections": [
                    {"title": "1. Introduction", "subsections": []},
                    {"title": "2. Related Work", "subsections": []},
                    {"title": "3. Methodology", "subsections": []},
                    {"title": "4. Experiments", "subsections": []},
                    {"title": "5. Discussion", "subsections": []},
                    {"title": "6. Conclusion", "subsections": []}
                ]
            }
        
        return outline
    
    def download_template(self, template_name: str) -> Path:
        """
         LaTeX 
        
        Args:
            template_name:  (ieee/acm/aaai/cvpr/icml/neurips)
            
        Returns:
            Path: 
        """
        if template_name not in self.supported_templates:
            raise ValueError(f"Unsupported template: {template_name}. "
                           f"Supported: {list(self.supported_templates.keys())}")
        
        template_info = self.supported_templates[template_name]
        print(f"  {template_info['name']} ...")
        
        template_dir = self.templates_dir / template_name
        template_dir.mkdir(exist_ok=True)
        
        # 
        # 
        
        #  LaTeX 
        self._create_basic_latex_structure(template_dir, template_name)
        
        print(f" : {template_dir}")
        return template_dir
    
    def _create_basic_latex_structure(self, template_dir: Path, template_name: str):
        """ LaTeX """
        
        # main.tex
        main_tex = template_dir / "main.tex"
        with open(main_tex, 'w', encoding='utf-8') as f:
            f.write(self._get_main_tex_template(template_name))
        
        # sections 
        sections_dir = template_dir / "sections"
        sections_dir.mkdir(exist_ok=True)
        
        # 
        sections = ["introduction", "method", "experiments", "discussion", "conclusion"]
        for section in sections:
            section_file = sections_dir / f"{section}.tex"
            with open(section_file, 'w', encoding='utf-8') as f:
                f.write(f"% {section.capitalize()} section\n\\section{{{section.capitalize()}}}\n\n")
        
        # references.bib
        bib_file = template_dir / "references.bib"
        with open(bib_file, 'w', encoding='utf-8') as f:
            f.write("% References\n")
    
    def _get_main_tex_template(self, template_name: str) -> str:
        """ LaTeX """
        
        templates = {
            "ieee": r"""\documentclass[conference]{IEEEtran}
\usepackage{cite}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{textcomp}
\usepackage{xcolor}

\title{[Your Paper Title]}
\author{
    \\IEEEauthorblockN{[Author Name]}
    \\IEEEauthorblockA{
        [Affiliation] \\
        [Email]
    }
}

\begin{document}

\maketitle

\begin{abstract}
[Your abstract here...]
\end{abstract}

\begin{IEEEkeywords}
[Keywords]
\end{IEEEkeywords}

\input{sections/introduction}
\input{sections/method}
\input{sections/experiments}
\input{sections/discussion}
\input{sections/conclusion}

\bibliographystyle{IEEEtran}
\bibliography{references}

\end{document}
""",
            "acm": r"""\documentclass[sigconf]{acmart}
\usepackage{booktabs}

\title{[Your Paper Title]}
\author{[Author Name]}
\affiliation{
    \institution{[Institution]}
}
\email{[Email]}

\begin{document}

\begin{abstract}
[Your abstract here...]
\end{abstract}

\maketitle

\input{sections/introduction}
\input{sections/method}
\input{sections/experiments}
\input{sections/discussion}
\input{sections/conclusion}

\bibliographystyle{ACM-Reference-Format}
\bibliography{references}

\end{document}
""",
            "default": r"""\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{hyperref}

\title{[Your Paper Title]}
\author{[Author Name]}
\date{\today}

\begin{document}

\maketitle

\begin{abstract}
[Your abstract here...]
\end{abstract}

\section{Introduction}
\input{sections/introduction}

\section{Methodology}
\input{sections/method}

\section{Experiments}
\input{sections/experiments}

\section{Discussion}
\input{sections/discussion}

\section{Conclusion}
\input{sections/conclusion}

\bibliographystyle{plain}
\bibliography{references}

\end{document}
"""
        }
        
        return templates.get(template_name, templates["default"])
    
    def generate_latex(self, outline: Dict, template_dir: Path, output_dir: Path) -> Path:
        """
         LaTeX 
        
        Args:
            outline: 
            template_dir: 
            output_dir: 
            
        Returns:
            Path: 
        """
        print("  LaTeX ...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        paper_dir = output_dir / f"paper_{timestamp}"
        paper_dir.mkdir(exist_ok=True)
        
        # 
        for item in template_dir.iterdir():
            if item.is_dir():
                shutil.copytree(item, paper_dir / item.name, dirs_exist_ok=True)
            else:
                shutil.copy2(item, paper_dir / item.name)
        
        #  main.tex 
        main_tex = paper_dir / "main.tex"
        if main_tex.exists():
            with open(main_tex, 'r', encoding='utf-8') as f:
                content = f.read()
            
            content = content.replace("[Your Paper Title]", outline.get("title", "Untitled Paper"))
            
            with open(main_tex, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # 
        self._generate_section_content(paper_dir / "sections", outline)
        
        # 
        meta = {
            "title": outline.get("title"),
            "created_at": datetime.now().isoformat(),
            "template": template_dir.name,
            "keywords": outline.get("keywords", []),
            "sections": [s["title"] for s in outline.get("sections", [])]
        }
        
        with open(paper_dir / "meta.json", 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)
        
        print(f" LaTeX : {paper_dir}")
        return paper_dir
    
    def _generate_section_content(self, sections_dir: Path, outline: Dict):
        """"""
        
        sections = outline.get("sections", [])
        
        for i, section in enumerate(sections, 1):
            section_name = section["title"].lower().replace(" ", "_").replace(".", "")
            section_file = sections_dir / f"{section_name}.tex"
            
            if section_file.exists():
                with open(section_file, 'w', encoding='utf-8') as f:
                    f.write(f"% {section['title']}\n")
                    f.write(f"\\section{{{section['title'].split('. ', 1)[-1]}}}\n\n")
                    
                    # 
                    for subsection in section.get("subsections", []):
                        f.write(f"\\subsection{{{subsection}}}\n\n")
                        f.write("[Content to be added...]\n\n")
                    
                    # 
                    if "content_points" in section:
                        f.write("\\textbf{Key Points}:\n")
                        f.write("\\begin{itemize}\n")
                        for point in section["content_points"]:
                            f.write(f"    \\item {point}\n")
                        f.write("\\end{itemize}\n\n")
    
    def review_paper(self, paper_dir: Path) -> Dict:
        """
         - 
        
        Args:
            paper_dir: 
            
        Returns:
            Dict: 
        """
        print(" ...")
        
        review = {
            "overall_score": 0,
            "strengths": [],
            "weaknesses": [],
            "suggestions": [],
            "detailed_comments": {}
        }
        
        # 
        main_tex = paper_dir / "main.tex"
        if not main_tex.exists():
            review["weaknesses"].append("Missing main.tex file")
        else:
            review["strengths"].append("LaTeX structure is complete")
        
        # 
        sections_dir = paper_dir / "sections"
        if sections_dir.exists():
            section_files = list(sections_dir.glob("*.tex"))
            if len(section_files) >= 4:
                review["strengths"].append(f"Paper has {len(section_files)} sections")
            else:
                review["weaknesses"].append("Paper structure might be incomplete")
        
        # 
        bib_file = paper_dir / "references.bib"
        if bib_file.exists():
            with open(bib_file, 'r', encoding='utf-8') as f:
                bib_content = f.read()
                if len(bib_content) > 100:
                    review["strengths"].append("References file is present")
                else:
                    review["weaknesses"].append("References need to be added")
        
        # 
        score = 5  # 
        score += len(review["strengths"]) * 0.5
        score -= len(review["weaknesses"]) * 0.5
        review["overall_score"] = min(max(score, 1), 10)
        
        # 
        review["suggestions"] = [
            "Add more detailed methodology description",
            "Include comprehensive experimental results",
            "Improve the clarity of figures and tables",
            "Expand the related work section",
            "Add ablation studies if applicable"
        ]
        
        # 
        review_file = paper_dir / "review_comments.json"
        with open(review_file, 'w', encoding='utf-8') as f:
            json.dump(review, f, indent=2, ensure_ascii=False)
        
        print(f" : {review['overall_score']}/10")
        return review
    
    def full_workflow(self, project_path: str, template_name: str = "ieee", paper_type: str = "conference"):
        """
        
        
        Args:
            project_path: 
            template_name: 
            paper_type: 
            
        Returns:
            Path: 
        """
        print("=" * 60)
        print("Academic Paper Writer - Full Workflow")
        print("=" * 60)
        
        # Step 1: 
        print("\nStep 1: Analyzing code...")
        analysis = self.analyze_code(project_path)
        print(f"Project type: {analysis['project_type']}")
        print(f"Innovations found: {len(analysis['innovations'])}")
        
        # Step 2: 
        print("\nStep 2: Designing outline...")
        outline = self.design_outline(analysis, paper_type)
        print(f"Paper title: {outline['title']}")
        print(f"Sections: {len(outline['sections'])}")
        
        # Step 3: 
        print("\nStep 3: Downloading template...")
        template_dir = self.download_template(template_name)
        
        # Step 4:  LaTeX
        print("\nStep 4: Generating LaTeX...")
        paper_dir = self.generate_latex(outline, template_dir, self.output_dir)
        
        # Step 5: 
        print("\nStep 5: Reviewing paper...")
        review = self.review_paper(paper_dir)
        
        # 
        report = {
            "workflow": "Academic Paper Writer",
            "timestamp": datetime.now().isoformat(),
            "project_path": str(project_path),
            "template": template_name,
            "paper_type": paper_type,
            "analysis": analysis,
            "outline": outline,
            "review": review,
            "output_dir": str(paper_dir)
        }
        
        report_file = paper_dir / "workflow_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 60)
        print(f"Complete! Paper generated at: {paper_dir}")
        print("=" * 60)
        
        return paper_dir


def main():
    """"""
    import sys
    
    writer = AcademicPaperWriter()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python academic_paper_writer.py <project_path> [template] [type]")
        print("")
        print("Templates: ieee, acm, aaai, cvpr, icml, neurips")
        print("Types: conference (default), journal")
        print("")
        print("Example:")
        print('  python academic_paper_writer.py "./my_project" ieee conference')
        return
    
    project_path = sys.argv[1]
    template = sys.argv[2] if len(sys.argv) > 2 else "ieee"
    paper_type = sys.argv[3] if len(sys.argv) > 3 else "conference"
    
    writer.full_workflow(project_path, template, paper_type)


if __name__ == "__main__":
    main()
