#!/usr/bin/env python3
"""测试 Playwright 和 overleaf_auto 模块"""

import sys
sys.path.insert(0, r'D:\apps\academic-paper-writer')

# 测试1: 检查 Playwright
print("Test 1: Checking Playwright installation...")
try:
    from playwright.sync_api import sync_playwright
    print("[OK] Playwright is installed")
    
    # 测试浏览器能否启动
    print("Test 2: Testing browser launch...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        print("[OK] Chromium browser launched successfully")
        
        # 测试访问网页
        page = browser.new_page()
        page.goto("https://www.google.com", timeout=10000)
        title = page.title()
        print(f"[OK] Can access web pages (title: {title})")
        
        browser.close()
    
except ImportError as e:
    print(f"[FAIL] Playwright not installed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"[FAIL] Browser test failed: {e}")
    sys.exit(1)

# 测试3: 检查 OverleafAutoManager
print("\nTest 3: Checking OverleafAutoManager...")
try:
    from overleaf_auto import OverleafAutoManager, PLAYWRIGHT_AVAILABLE
    
    if PLAYWRIGHT_AVAILABLE:
        print("[OK] PLAYWRIGHT_AVAILABLE = True")
    else:
        print("[FAIL] PLAYWRIGHT_AVAILABLE = False")
        sys.exit(1)
    
    # 测试初始化 (无账号)
    manager = OverleafAutoManager()
    print("[OK] OverleafAutoManager initialized")
    
    # 测试缺少凭证时的错误处理
    result = manager.create_project("test-project")
    if not result["success"] and "credentials" in result["error"].lower():
        print("[OK] Correctly reports missing credentials")
    else:
        print(f"[WARN] Unexpected result: {result}")
    
except Exception as e:
    print(f"[FAIL] OverleafAutoManager test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试4: 检查 OverleafGitSync
print("\nTest 4: Checking OverleafGitSync...")
try:
    from overleaf_auto import OverleafGitSync
    sync = OverleafGitSync()
    print("[OK] OverleafGitSync initialized")
    print(f"  Config file: {sync.config_file}")
    print(f"  Saved projects: {len(sync.projects)}")
    
except Exception as e:
    print(f"[FAIL] OverleafGitSync test failed: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("All tests passed!")
print("="*50)
print("\nNext steps:")
print("1. Set OVERLEAF_EMAIL and OVERLEAF_PASSWORD environment variables")
print("2. Run: python full_workflow.py ./test_project --auto --name my-paper")
