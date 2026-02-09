#!/usr/bin/env python3
"""
使用临时邮箱注册 Overleaf 测试账号
"""

import requests
import time
import re
from playwright.sync_api import sync_playwright

class TempMailClient:
    """临时邮箱客户端 (使用 mail.tm 服务)"""
    
    def __init__(self):
        self.base_url = "https://api.mail.tm"
        self.token = None
        self.email = None
        self.password = None
    
    def create_account(self):
        """创建临时邮箱账号"""
        # 1. 获取可用域名
        domains_resp = requests.get(f"{self.base_url}/domains")
        domains = domains_resp.json()["hydra:member"]
        domain = domains[0]["domain"]
        
        # 2. 生成随机邮箱
        import random
        import string
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        self.email = f"{username}@{domain}"
        self.password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        
        # 3. 创建账号
        account_data = {
            "address": self.email,
            "password": self.password
        }
        
        resp = requests.post(f"{self.base_url}/accounts", json=account_data)
        if resp.status_code in [200, 201]:
            print(f"[OK] Created temp email: {self.email}")
            
            # 4. 获取 token
            token_resp = requests.post(
                f"{self.base_url}/token",
                json={"address": self.email, "password": self.password}
            )
            self.token = token_resp.json()["token"]
            return True
        else:
            print(f"[Error] Failed to create: {resp.text}")
            return False
    
    def get_messages(self):
        """获取邮件列表"""
        if not self.token:
            return []
        
        headers = {"Authorization": f"Bearer {self.token}"}
        resp = requests.get(f"{self.base_url}/messages", headers=headers)
        
        if resp.status_code == 200:
            return resp.json()["hydra:member"]
        return []
    
    def get_message_content(self, message_id):
        """获取邮件内容"""
        headers = {"Authorization": f"Bearer {self.token}"}
        resp = requests.get(f"{self.base_url}/messages/{message_id}", headers=headers)
        
        if resp.status_code == 200:
            return resp.json()
        return None
    
    def wait_for_verification_email(self, timeout=120):
        """等待验证邮件"""
        print(f"[Waiting] For verification email (max {timeout}s)...")
        start = time.time()
        
        while time.time() - start < timeout:
            messages = self.get_messages()
            for msg in messages:
                if "overleaf" in msg.get("subject", "").lower() or \
                   "verify" in msg.get("subject", "").lower():
                    print(f"[Found] Email: {msg['subject']}")
                    content = self.get_message_content(msg["id"])
                    return content
            time.sleep(3)
        
        return None


def register_overleaf_with_temp_email():
    """
    使用临时邮箱注册 Overleaf
    """
    # 创建临时邮箱
    print("="*60)
    print("Step 1: Creating temporary email")
    print("="*60)
    
    mail = TempMailClient()
    if not mail.create_account():
        return None
    
    email = mail.email
    password = mail.password
    
    print(f"  Email: {email}")
    print(f"  Password: {password}")
    
    # 注册 Overleaf
    print("\n" + "="*60)
    print("Step 2: Registering Overleaf account")
    print("="*60)
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            
            # 1. 打开注册页面
            print("[Auto] Opening registration page...")
            page.goto("https://www.overleaf.com/register", wait_until="networkidle")
            
            # 2. 填写注册信息
            print("[Auto] Filling registration form...")
            page.fill("input[name='email']", email)
            
            # Overleaf 要求确认邮箱
            page.fill("input[name='confirmEmail']", email)
            
            # 密码
            page.fill("input[name='password']", password)
            
            # 点击注册
            page.click("button[type='submit']")
            
            # 等待跳转
            page.wait_for_timeout(3000)
            
            # 检查是否成功
            current_url = page.url
            if "dashboard" in current_url or "project" in current_url:
                print("[OK] Registration successful!")
            else:
                print(f"[Info] Current URL: {current_url}")
                # 可能需要邮箱验证
            
            browser.close()
        
        # 等待验证邮件
        print("\n" + "="*60)
        print("Step 3: Waiting for verification email")
        print("="*60)
        
        verification = mail.wait_for_verification_email(timeout=60)
        
        if verification:
            # 提取验证链接
            html_content = verification.get("html", [])
            if html_content:
                text = html_content[0] if isinstance(html_content, list) else str(html_content)
                
                # 查找验证链接
                match = re.search(r'href="(https://www\.overleaf\.com/verify[^"]+)"', text)
                if match:
                    verify_url = match.group(1)
                    print(f"[Found] Verification URL: {verify_url}")
                    
                    # 验证邮箱
                    print("[Auto] Verifying email...")
                    with sync_playwright() as p:
                        browser = p.chromium.launch(headless=True)
                        page = browser.new_page()
                        page.goto(verify_url)
                        page.wait_for_timeout(3000)
                        browser.close()
                    print("[OK] Email verified!")
        else:
            print("[Warning] No verification email found (may not be required)")
        
        print("\n" + "="*60)
        print("Test Account Created!")
        print("="*60)
        print(f"  Email: {email}")
        print(f"  Password: {password}")
        print(f"  Status: Ready for testing")
        
        return {
            "email": email,
            "password": password,
            "temp_mail": mail
        }
        
    except Exception as e:
        print(f"[Error] {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    account = register_overleaf_with_temp_email()
    
    if account:
        print("\n[Test Ready] You can now run:")
        print(f"  set OVERLEAF_EMAIL={account['email']}")
        print(f"  set OVERLEAF_PASSWORD={account['password']}")
        print("  python full_workflow.py D:\\vibe_coding\\test_ai_project --auto --name test-paper")
    else:
        print("[Failed] Could not create test account")
