from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# 크롬 브라우저가 자동으로 닫히지 않게 하기 위해 options와 chromedrivermanager를 이용해 관리
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# 일련의 동작 후 대기를 위해 time 라이브러리 추가
import time

# 찾으려는 요소를 모두 가져올 때 까지 기다리기 위해 사용
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


options = ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# 아이디, 비밀번호 입력
id = input("인스타그램 id> ")
pw = input("인스타그램 pw> ")

# 태그, 댓글에 입력할 문구 작성
tag_name = input("검색할 키워드/태그> ")
comm = input("댓글 내용> ")

# 태그명을 적을 때 #을 입력 안 했다면 맨 앞에 추가
if not tag_name.startswith("#"):
    tag_name = "#" + tag_name

# 입력 받은 아이디와 비밀번호가 있는 경우에만 로그인
if id and pw:
    driver.get("https://www.instagram.com/")

#대기 동작 구현
wait = WebDriverWait(driver, 10)

# name 요소를 통해 html 태그를 찾는다
id_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
pw_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))

# html 요소에 입력받은 아이디와 비밀번호를 입력해준다
id_input.send_keys(id)
pw_input.send_keys(pw)

#1.5초 대기
time.sleep(1.5)

# CSS_SELECTOR를 통해 클래스 이름으로 로그인 버튼에 해당하는 html 태그를 찾아준 후 
# Keys.RETURN(엔터 동작)을 send_keys 함수로 보내 엔터 동작으로 로그인
login_btn = driver.find_element(By.CSS_SELECTOR, "._acan._acap._acas._aj1-._ap30")
login_btn.send_keys(Keys.RETURN)

# 검색 버튼을 찾은 후 클릭
elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".x9f619.xxk0z11.xii2z7h.x11xpdln.x19c4wfv.xvy4d1p")))
search_btn = elements[2]
search_btn.click()

# 태그 검색
search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".x1lugfcp")))
search_input.send_keys(tag_name)

# 태그 검색 결과 중 맨 위의 태그 선택
result = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".x9f619.x1n2onr6.x1ja2u2z.x78zum5.x2lah0s.x1qughib.x6s0dn4.xozqiw3.x1q0g3np")))
target_tag = result[0]
target_tag.click()

time.sleep(1)
# 피드 선택 후 닫기
pids = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "._aagw")))
time.sleep(1.5)
for pid in pids:
    try:
        pid.click()
    except Exception as e:
        print("피드 선택 중 오류가 발생했습니다:", e)    

    # 팔로우 버튼 클릭
    try:
        follow_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "._acan._acao._acas._aj1-._ap30")))
        follow_btn.click()
    except Exception as e:
        print("이미 팔로우가 되어 있습니다")
        pass  

    time.sleep(1.5)
    try:
        like_btn = driver.find_element(By.CSS_SELECTOR, '._aamu._ae3_._ae47._ae48 [aria-label="좋아요"]')
        comment_path = driver.find_element(By.XPATH, '//textarea[@aria-label="댓글 달기..."]')
        print("댓글 입력창: ", comment_path)
        if like_btn:
            like_btn.click()

            driver.implicitly_wait(1)
            try:
                comment_path.click()
                comment_path = driver.find_element(By.TAG_NAME, 'textarea')
                comment_path.send_keys(comm)
                time.sleep(1)
                comment_path.send_keys(Keys.ENTER)
            except Exception as comm_error:
                print("댓글 작성 중 에러 발생", comm_error)
                pass
    except Exception as like_error:
        print("좋아요 중 에러 발생(못 찾았거니 이미 되어 있습니다.)")
        pass

        time.sleep(1)

    try:
        # 닫기 버튼이 클릭 가능한 상태가 될 때까지 대기 (최대 10초)
        # 만약 같은 클래스를 가지고 있는 태그들이 많고, 순서를 특정할 수 없다면 
        # xPath나 아래와 같이 다른 요소를 가지고 원하는 태그를 찾을 수 있다.
        close_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="닫기"]')))
        close_btn.click()

        # 다음 피드를 클릭하기 전에 1초 대기
        time.sleep(2)
    except Exception as e:
        print("닫기 버튼을 클릭할 수 없습니다:", e)