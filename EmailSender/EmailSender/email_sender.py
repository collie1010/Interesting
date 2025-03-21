# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 23:37:29 2025

@author: user
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import time
import pandas as pd
import sys
import os
import json

class EmailSender:
    def __init__(self):
        self.config_file = 'email_config.json'
        self.sender_email = ''
        self.sender_password = ''
        self.email_content = ''
        self.email_subject = '通知信件'  # 預設主旨
        
    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.sender_email = config.get('email', '')
                    return True
            return False
        except:
            return False

    def save_config(self):
        config = {
            'email': self.sender_email
        }
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except:
            pass

    def log_message(self, message):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] {message}")
        
    def get_credentials(self):
        print("\n=== Email 寄送程式 ===")
        
        if self.load_config():
            print(f"\n找到上次使用的 Email: {self.sender_email}")
            use_saved = input("是否使用此 Email？(y/n): ").lower() == 'y'
            if not use_saved:
                self.sender_email = input("\n請輸入您的 Gmail 帳號: ")
        else:
            self.sender_email = input("\n請輸入您的 Gmail 帳號: ")
            
        self.sender_password = input("請輸入您的 Gmail 應用程式密碼: ")
        
        save_config = input("\n是否記住這個 Email 帳號？(y/n): ").lower() == 'y'
        if save_config:
            self.save_config()

    def select_file(self, file_type='.csv', purpose=''):
        while True:
            print(f"\n請輸入{purpose}的完整路徑（或直接拖曳檔案到此視窗）: ")
            file_path = input().strip()
            
            # 移除可能的引號
            file_path = file_path.strip('"').strip("'")
            
            if not file_path:
                print("未輸入檔案路徑！")
                continue
                
            if not os.path.exists(file_path):
                print("找不到指定的檔案！請確認路徑是否正確。")
                continue
                
            if not file_path.lower().endswith(file_type):
                print(f"請選擇{file_type}檔案！")
                continue
                
            return file_path

    def load_email_content(self):
        # 讓使用者輸入郵件主旨
        self.email_subject = input("\n請輸入郵件主旨 (直接按 Enter 使用預設主旨): ").strip()
        if not self.email_subject:
            self.email_subject = '通知信件'

        # 選擇郵件內容檔案
        content_file = self.select_file('.txt', '郵件內容文字檔')
        
        try:
            # 使用 UTF-8 編碼讀取檔案，保留格式
            with open(content_file, 'r', encoding='utf-8') as f:
                self.email_content = f.read()
            
            # 顯示郵件內容預覽
            print("\n=== 郵件內容預覽 ===")
            print(f"主旨: {self.email_subject}")
            print("內文:")
            print(self.email_content)
            print("=== 預覽結束 ===")
            
            # 確認內容
            if input("\n確認使用此郵件內容？(y/n): ").lower() != 'y':
                return False
            return True
            
        except Exception as e:
            print(f"\n讀取郵件內容檔案時發生錯誤：{str(e)}")
            return False

    def send_email(self, receiver_email):
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = receiver_email
        message["Subject"] = self.email_subject

        # 將當前時間加入到郵件內容的最後
        full_content = f"{self.email_content}\n\n寄送時間：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # 使用 plain 格式，保留原始格式
        message.attach(MIMEText(full_content, "plain"))
        return message

    def run(self):
        try:
            # 取得認證資訊
            self.get_credentials()
            
            # 讀取郵件內容
            if not self.load_email_content():
                input("\n按 Enter 鍵結束程式...")
                return
            
            # 選擇 CSV 檔案
            csv_file = self.select_file('.csv', 'email 清單 CSV 檔')
            
            # 讀取 CSV 檔案
            try:
                df = pd.read_csv(csv_file, header=None, names=['email'])
                emails = df['email'].tolist()
                emails = [email.strip() for email in emails if isinstance(email, str)]
            except Exception as e:
                print(f"\n讀取 CSV 檔案時發生錯誤：{str(e)}")
                input("\n按 Enter 鍵結束程式...")
                return
            
            # 顯示讀取到的 email
            print(f"\n成功讀取到 {len(emails)} 個 email 地址：")
            for email in emails:
                print(f"- {email}")
                
            # 確認是否發送
            confirm = input(f"\n確定要發送郵件給這 {len(emails)} 個收件者嗎？(y/n): ").lower()
            if confirm != 'y':
                print("\n取消發送！")
                input("\n按 Enter 鍵結束程式...")
                return
                
            # 建立 SMTP 連線
            self.log_message("正在連線到 SMTP 伺服器...")
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            
            # 登入
            self.log_message("正在登入...")
            server.login(self.sender_email, self.sender_password)
            self.log_message("登入成功！")
            
            # 發送郵件
            for i, receiver_email in enumerate(emails, 1):
                try:
                    message = self.send_email(receiver_email)
                    text = message.as_string()
                    server.sendmail(self.sender_email, receiver_email, text)
                    self.log_message(f"成功寄送第 {i}/{len(emails)} 封郵件給 {receiver_email}")
                    
                    if i < len(emails):
                        time.sleep(2)
                        
                except Exception as e:
                    self.log_message(f"寄送給 {receiver_email} 時發生錯誤：{str(e)}")
                    
        except Exception as e:
            self.log_message(f"發生錯誤：{str(e)}")
            
        finally:
            try:
                server.quit()
                self.log_message("SMTP 連線已關閉")
            except:
                pass
            
        input("\n按 Enter 鍵結束程式...")

if __name__ == "__main__":
    sender = EmailSender()
    sender.run()
