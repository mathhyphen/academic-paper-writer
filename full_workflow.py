#!/usr/bin/env python3
"""
完整的学术论文工作流：生成论文 + 自动同步到 Overleaf (全自动版本)

支持两种模式：
1. 全自动模式：使用 Playwright 自动登录 Overleaf 创建项目
2. 半自动模式：用户手动提供 git URL

环境变量：
- OVERLEAF_EMAIL: Overleaf 邮箱
- OVERLEAF_PASSWORD: Overleaf 密码
- 或者直接在命令行参数提供
"""

import sys
import os
sys.path.insert(0, r'D:\apps\academic-paper-writer')

from academic_paper_writer import AcademicPaperWriter
from overleaf_auto import OverleafGitSync, OverleafAutoManager


def full_workflow_auto(
    project_path: str,
    template: str = "ieee",
    paper_type: str = "conference",
    overleaf_project_name: str = None,
    auto_create: bool = False,
    email: str = None,
    password: str = None
):
    """
    完整工作流：代码 → 论文 → Overleaf
    
    Args:
        project_path: 代码项目路径
        template: LaTeX 模板 (ieee/acm/aaai/cvpr/icml/neurips)
        paper_type: 论文类型 (conference/journal)
        overleaf_project_name: Overleaf 项目名称
        auto_create: 是否自动创建 Overleaf 项目 (需要 Playwright + 账号)
        email: Overleaf 邮箱 (可选，优先使用环境变量)
        password: Overleaf 密码 (可选，优先使用环境变量)
    """
    
    # Step 1: 生成论文
    print("="*60)
    print("Step 1: Generating Paper from Code")
    print("="*60)
    
    writer = AcademicPaperWriter()
    paper_dir = writer.full_workflow(project_path, template, paper_type)
    
    # Step 2: 同步到 Overleaf
    print("\n" + "="*60)
    print("Step 2: Syncing to Overleaf")
    print("="*60)
    
    project_name = overleaf_project_name or paper_dir.name
    
    # 尝试全自动模式
    if auto_create:
        print(f"[Auto Mode] Creating Overleaf project: {project_name}")
        
        auto_manager = OverleafAutoManager(email, password)
        result = auto_manager.sync_to_overleaf(paper_dir, project_name)
        
        if result["success"]:
            print(f"[OK] Auto-created and synced!")
            return {
                "paper_dir": str(paper_dir),
                "overleaf_configured": True,
                "auto_created": True,
                "sync_success": True,
                "project_name": project_name,
                "git_url": result.get("git_url"),
                "view_url": result.get("view_url")
            }
        else:
            print(f"[Auto Failed] {result.get('error')}")
            print(f"[Fallback] Switching to manual mode...")
    
    # 半自动模式
    sync = OverleafGitSync()
    
    if project_name not in sync.projects:
        print(f"\n[Manual Setup Required]")
        print(f"Project '{project_name}' not configured yet.")
        print(f"\nPlease choose:")
        print(f"\nOption 1 - Manual (Recommended):")
        print(f"  1. Go to https://www.overleaf.com/project/new")
        print(f"  2. Create blank project: {project_name}")
        print(f"  3. Menu → Git → Copy git URL")
        print(f"  4. Run: python overleaf_auto.py add {project_name} <git_url>")
        print(f"\nOption 2 - Auto (Needs credentials):")
        print(f"  Set OVERLEAF_EMAIL and OVERLEAF_PASSWORD env vars")
        print(f"  Then run with --auto flag")
        
        return {
            "paper_dir": str(paper_dir),
            "overleaf_configured": False,
            "next_step": f"python overleaf_auto.py add {project_name} <git_url>"
        }
    
    # 已配置，直接同步
    success = sync.sync(paper_dir, project_name)
    
    return {
        "paper_dir": str(paper_dir),
        "overleaf_configured": True,
        "auto_created": False,
        "sync_success": success,
        "project_name": project_name
    }


def main():
    """命令行入口"""
    args = sys.argv[1:]
    
    if not args or args[0] in ['-h', '--help']:
        print("Full Workflow: Code → Paper → Overleaf")
        print("")
        print("Usage:")
        print("  python full_workflow.py <project_path> [options]")
        print("")
        print("Options:")
        print("  --template <name>     LaTeX template (ieee/acm/aaai/cvpr/icml/neurips)")
        print("  --type <type>         Paper type (conference/journal)")
        print("  --name <name>         Overleaf project name")
        print("  --auto                Auto-create Overleaf project (needs credentials)")
        print("  --email <email>       Overleaf email (or set OVERLEAF_EMAIL env)")
        print("  --password <pass>     Overleaf password (or set OVERLEAF_PASSWORD env)")
        print("")
        print("Examples:")
        print('  # Basic: generate paper only')
        print('  python full_workflow.py ./my-project')
        print("")
        print('  # Full: generate + sync to existing Overleaf project')
        print('  python full_workflow.py ./my-project --name my-paper')
        print("")
        print('  # Auto: generate + auto-create Overleaf project')
        print('  python full_workflow.py ./my-project --auto --name my-paper')
        print("")
        print("Environment Variables:")
        print("  OVERLEAF_EMAIL, OVERLEAF_PASSWORD (for --auto mode)")
        return
    
    # 解析参数
    project_path = args[0]
    
    # 默认值
    template = "ieee"
    paper_type = "conference"
    overleaf_name = None
    auto_create = False
    email = None
    password = None
    
    # 解析选项
    i = 1
    while i < len(args):
        if args[i] == '--template' and i + 1 < len(args):
            template = args[i + 1]
            i += 2
        elif args[i] == '--type' and i + 1 < len(args):
            paper_type = args[i + 1]
            i += 2
        elif args[i] == '--name' and i + 1 < len(args):
            overleaf_name = args[i + 1]
            i += 2
        elif args[i] == '--auto':
            auto_create = True
            i += 1
        elif args[i] == '--email' and i + 1 < len(args):
            email = args[i + 1]
            i += 2
        elif args[i] == '--password' and i + 1 < len(args):
            password = args[i + 1]
            i += 2
        else:
            i += 1
    
    # 执行工作流
    result = full_workflow_auto(
        project_path=project_path,
        template=template,
        paper_type=paper_type,
        overleaf_project_name=overleaf_name,
        auto_create=auto_create,
        email=email,
        password=password
    )
    
    print("\n" + "="*60)
    print("Workflow Complete!")
    print("="*60)
    for key, value in result.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
