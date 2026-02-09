#!/usr/bin/env python3
"""
Overleaf 自动化助手
由于 Overleaf 没有公开 API，使用浏览器自动化创建项目
"""

import os
import re
import time
import subprocess
from pathlib import Path
from urllib.parse import urlparse

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


class OverleafAutoManager:
    """Overleaf 自动化管理器"""
    
    def __init__(self, email: str = None, password: str = None):
        self.email = email or os.getenv("OVERLEAF_EMAIL")
        self.password = password or os.getenv("OVERLEAF_PASSWORD")
        self.git_urls = {}  # 缓存 git URL
        
    def create_project(self, project_name: str, template: str = "blank") -> dict:
        """
        自动创建 Overleaf 项目
        
        由于 Overleaf 没有公开 API，使用浏览器自动化
        
        Args:
            project_name: 项目名称
            template: 模板类型 (blank/cvpr/ieee等)
            
        Returns:
            dict: 包含 project_url, git_url
        """
        if not PLAYWRIGHT_AVAILABLE:
            return {
                "success": False,
                "error": "Playwright not installed. Run: pip install playwright && playwright install chromium",
                "manual_url": "https://www.overleaf.com/project/new"
            }
        
        if not self.email or not self.password:
            return {
                "success": False,
                "error": "Need Overleaf credentials. Set OVERLEAF_EMAIL and OVERLEAF_PASSWORD env vars",
                "manual_url": "https://www.overleaf.com/project/new"
            }
        
        print(f"[Auto] Creating Overleaf project: {project_name}")
        print(f"[Auto] This may take 10-20 seconds...")
        
        try:
            with sync_playwright() as p:
                # 启动浏览器 (无头模式)
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(viewport={"width": 1280, "height": 720})
                page = context.new_page()
                
                # 1. 登录
                print("[Auto] Logging in to Overleaf...")
                page.goto("https://www.overleaf.com/login", wait_until="networkidle")
                
                # 填写登录表单
                page.fill("input[name='email']", self.email)
                page.fill("input[name='password']", self.password)
                page.click("button[type='submit']")
                
                # 等待登录完成 (跳转到 dashboard)
                page.wait_for_url("**/project", wait_until="networkidle")
                print("[Auto] Login successful")
                
                # 2. 创建新项目
                print("[Auto] Creating new project...")
                page.goto("https://www.overleaf.com/project/new", wait_until="networkidle")
                
                # 3. 选择 Blank Project (通过链接文本)
                # 等待页面加载
                page.wait_for_selector("text=Blank Project", timeout=10000)
                
                # 点击 Blank Project
                blank_btn = page.locator("text=Blank Project").first
                blank_btn.click()
                
                # 4. 填写项目名称
                page.wait_for_selector("input[placeholder*='Project Name']", timeout=10000)
                page.fill("input[placeholder*='Project Name']", project_name)
                
                # 点击 Create 按钮
                page.click("button:has-text('Create'):not([disabled])")
                
                # 5. 等待项目编辑器加载
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(3000)  # 额外等待
                
                project_url = page.url
                print(f"[Auto] Project created: {project_url}")
                
                # 6. 获取 Git URL
                print("[Auto] Getting Git URL...")
                
                # 点击 Menu 按钮
                page.click("button[aria-label*='Menu']")
                page.wait_for_timeout(1000)
                
                # 点击 Git 选项
                git_link = page.locator("text=Git").first
                git_link.click()
                
                # 等待 Git 对话框
                page.wait_for_selector("text=Git Integration", timeout=10000)
                
                # 获取 git URL
                git_input = page.locator("input[value*='git.overleaf.com']").first
                git_url = git_input.get_attribute("value")
                
                browser.close()
                
                # 缓存结果
                self.git_urls[project_name] = git_url
                
                print(f"[Auto] Got Git URL: {git_url[:50]}...")
                
                return {
                    "success": True,
                    "project_name": project_name,
                    "project_url": project_url,
                    "git_url": git_url
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "manual_url": "https://www.overleaf.com/project/new"
            }
    
    def sync_to_overleaf(self, local_path: str, project_name: str = None) -> dict:
        """
        同步本地 LaTeX 项目到 Overleaf
        
        Args:
            local_path: 本地项目路径
            project_name: Overleaf 项目名称（可选，默认使用文件夹名）
            
        Returns:
            dict: 操作结果
        """
        local_path = Path(local_path)
        project_name = project_name or local_path.name
        
        print(f"[Sync] Syncing {local_path} to Overleaf project: {project_name}")
        
        # 1. 创建项目（如果还没有）
        if project_name not in self.git_urls:
            result = self.create_project(project_name)
            if not result["success"]:
                return result
            git_url = result["git_url"]
        else:
            git_url = self.git_urls[project_name]
        
        # 2. Git 操作
        git_dir = local_path / ".git"
        
        if not git_dir.exists():
            # 初始化 git
            subprocess.run(["git", "init"], cwd=local_path, check=True)
            subprocess.run(["git", "remote", "add", "overleaf", git_url], cwd=local_path, check=True)
        
        # 3. 提交并推送
        try:
            subprocess.run(["git", "add", "."], cwd=local_path, check=True)
            subprocess.run(["git", "commit", "-m", "Update from Academic Paper Writer"], 
                          cwd=local_path, check=True, capture_output=True)
        except subprocess.CalledProcessError:
            pass  # 可能没有变更
        
        # 推送到 Overleaf
        result = subprocess.run(
            ["git", "push", "overleaf", "master"], 
            cwd=local_path, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            return {
                "success": True,
                "message": f"Successfully synced to Overleaf project: {project_name}",
                "git_url": git_url,
                "view_url": f"https://www.overleaf.com/project/{self._extract_project_id(git_url)}"
            }
        else:
            return {
                "success": False,
                "error": result.stderr,
                "git_url": git_url
            }
    
    def _extract_project_id(self, git_url: str) -> str:
        """从 git URL 提取项目 ID"""
        # https://git.overleaf.com/xxxxx
        parsed = urlparse(git_url)
        return parsed.path.strip("/")


# 简单的非自动化版本（手动输入 git URL）
class OverleafGitSync:
    """手动 Overleaf Git 同步"""
    
    def __init__(self):
        self.config_file = Path.home() / ".overleaf_sync.json"
        self.projects = self._load_config()
    
    def _load_config(self) -> dict:
        """加载配置"""
        if self.config_file.exists():
            import json
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_config(self):
        """保存配置"""
        import json
        with open(self.config_file, 'w') as f:
            json.dump(self.projects, f, indent=2)
    
    def add_project(self, name: str, git_url: str):
        """添加项目配置"""
        self.projects[name] = {
            "git_url": git_url,
            "created_at": time.time()
        }
        self._save_config()
        print(f"[OK] Project '{name}' added with git URL")
    
    def sync(self, local_path: str, project_name: str = None):
        """同步项目"""
        local_path = Path(local_path)
        
        if project_name is None:
            # 尝试匹配本地文件夹名
            project_name = local_path.name
        
        if project_name not in self.projects:
            print(f"[Error] Project '{project_name}' not found in config")
            print(f"[Info] Available projects: {list(self.projects.keys())}")
            print(f"[Info] Add it first with: add_project('{project_name}', 'git_url')")
            return False
        
        git_url = self.projects[project_name]["git_url"]
        
        # Git 操作
        git_dir = local_path / ".git"
        
        if not git_dir.exists():
            subprocess.run(["git", "init"], cwd=local_path, check=True)
        
        # 检查 remote
        result = subprocess.run(
            ["git", "remote", "get-url", "overleaf"],
            cwd=local_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0 or "overleaf" not in result.stdout:
            subprocess.run(["git", "remote", "add", "overleaf", git_url], cwd=local_path)
        
        # 提交
        subprocess.run(["git", "add", "."], cwd=local_path)
        subprocess.run(
            ["git", "commit", "-m", f"Update {time.strftime('%Y-%m-%d %H:%M')}"],
            cwd=local_path,
            capture_output=True
        )
        
        # 推送
        result = subprocess.run(
            ["git", "push", "-u", "overleaf", "master"],
            cwd=local_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"[OK] Synced '{project_name}' to Overleaf")
            return True
        else:
            print(f"[Error] Sync failed: {result.stderr}")
            return False


def main():
    """命令行入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("Overleaf Auto Manager")
        print("")
        print("Usage:")
        print("  python overleaf_auto.py sync <local_path> [project_name]")
        print("  python overleaf_auto.py add <project_name> <git_url>")
        print("")
        print("Examples:")
        print('  python overleaf_auto.py add my-paper https://git.overleaf.com/xxxxx')
        print('  python overleaf_auto.py sync ./papers/paper_20260209 my-paper')
        return
    
    command = sys.argv[1]
    
    # 手动版本（不需要 Playwright）
    manager = OverleafGitSync()
    
    if command == "add" and len(sys.argv) >= 4:
        manager.add_project(sys.argv[2], sys.argv[3])
    elif command == "sync" and len(sys.argv) >= 3:
        local_path = sys.argv[2]
        project_name = sys.argv[3] if len(sys.argv) > 3 else None
        manager.sync(local_path, project_name)
    else:
        print("Invalid command")


if __name__ == "__main__":
    main()
