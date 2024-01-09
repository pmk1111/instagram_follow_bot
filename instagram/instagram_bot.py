import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

class InstagramAutomationGUI:
    def __init__(self, master):
        self.master = master
        master.title("Instagram_Bot")

        self.label_id = ttk.Label(master, text="인스타그램 ID:")
        self.label_id.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        self.entry_id = ttk.Entry(master)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        self.label_pw = ttk.Label(master, text="인스타그램 PW:")
        self.label_pw.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.entry_pw = ttk.Entry(master, show="*")
        self.entry_pw.grid(row=1, column=1, padx=5, pady=5)

        self.label_tag = ttk.Label(master, text="검색할 키워드/태그:")
        self.label_tag.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

        self.entry_tag = ttk.Entry(master)
        self.entry_tag.grid(row=2, column=1, padx=5, pady=5)

        self.label_comment = ttk.Label(master, text="댓글 내용:")
        self.label_comment.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)

        self.entry_comment = ttk.Entry(master)
        self.entry_comment.grid(row=3, column=1, padx=5, pady=5)

        self.label_duration = ttk.Label(master, text="시간:")
        self.label_duration.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)

        self.entry_duration = ttk.Entry(master)
        self.entry_duration.grid(row=4, column=1, padx=5, pady=5)

        self.label_sec_min = ttk.Label(master, text="시간 단위:")
        self.label_sec_min.grid(row=5, column=0, sticky=tk.W, padx=2, pady=5)

        # 라디오 버튼을 위한 변수
        self.radio_var = tk.StringVar(value="초")
        
        # 라디오 버튼 생성
        self.radio_sec = ttk.Radiobutton(master, text="초", variable=self.radio_var, value="초")
        self.radio_sec.grid(row=5, column=1, padx=(0, 110))

        self.radio_min = ttk.Radiobutton(master, text="분", variable=self.radio_var, value="분")
        self.radio_min.grid(row=6, column=1, padx=(0, 110))

        self.run_button = ttk.Button(master, text="실행", command=self.run_instagram_automation)
        self.run_button.grid(row=7, column=0, columnspan=2, pady=10)

    def run_instagram_automation(self):
        id_value = self.entry_id.get()
        pw_value = self.entry_pw.get()
        tag_name = self.entry_tag.get()
        comm = self.entry_comment.get()
        duration = self.entry_duration.get()
        time_unit = self.radio_var.get()

        options = ChromeOptions()
        options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        # 태그명을 적을 때 #을 입력 안 했다면 맨 앞에 추가
        if not tag_name.startswith("#"):
            tag_name = "#" + tag_name

        if id_value and pw_value:
            driver.get("https://www.instagram.com/")

        wait = WebDriverWait(driver, 10)

        id_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        pw_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        id_input.send_keys(id_value)
        pw_input.send_keys(pw_value)
        driver.implicitly_wait(5)  

        login_btn = driver.find_element(By.CSS_SELECTOR, "._acan._acap._acas._aj1-._ap30")
        login_btn.send_keys(Keys.RETURN)

        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".x9f619.xxk0z11.xii2z7h.x11xpdln.x19c4wfv.xvy4d1p")))
        search_btn = elements[2]
        search_btn.click()

        search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".x1lugfcp")))
        search_input.send_keys(tag_name)
        time.sleep(2)
         
        result = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".x9f619.x1n2onr6.x1ja2u2z.x78zum5.x2lah0s.x1qughib.x6s0dn4.xozqiw3.x1q0g3np")))
        target_tag = result[0]
        target_tag.click()

        driver.implicitly_wait(3)  

        pids = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "._aagw")))
        driver.implicitly_wait(5)  

        for pid in pids:
            try:
                pid.click()
            except Exception as e:
                print("피드 선택 중 오류가 발생했습니다:", e)
            driver.implicitly_wait(3)  

            try:
                follow_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div._ap3a._aaco._aacw._aad6._aade")))
                follow_btn.click()
            except Exception as e:
                print("이미 팔로우가 되어 있습니다")
                pass

            time.sleep(3)
            try:
                like_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span._aamw svg[aria-label="좋아요"]')))
                comment_path = wait.until(EC.element_to_be_clickable((By.XPATH, '//textarea[@aria-label="댓글 달기..."]')))
                print("댓글 입력창: ", comment_path)
                if like_btn:
                    like_btn.click()
                    time.sleep(2)
                    try:
                        comment_path.click()
                        comment_path = driver.find_element(By.XPATH, '//textarea[@aria-label="댓글 달기..."]')
                        comment_path.send_keys(comm)
                        time.sleep(1)
                        comment_path.send_keys(Keys.ENTER)
                    except Exception as comm_error:
                        print("댓글 작성 중 에러 발생", comm_error)
                        pass
            except Exception as like_error:
                print("좋아요 중 에러 발생(못 찾았거니 이미 되어 있습니다.)")
                pass

                time.sleep(2)  

            try:
                close_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="닫기"]')))
                close_btn.click()
                driver.implicitly_wait(5) 
            except Exception as e:
                print("닫기 버튼을 클릭할 수 없습니다:", e)
            
            if time_unit == '초':
                time.sleep(int(duration))
            else:
                time.sleep(int(duration)*60)

if __name__ == "__main__":
    root = tk.Tk()
    app = InstagramAutomationGUI(root)
    root.mainloop()
