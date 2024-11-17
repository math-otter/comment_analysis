# 0. 프로그램에 필요한 패키지 임포트
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# 1. 브라우저 열기
driver_path = "chromedriver.exe" # 크롬 드라이버 사용
service = Service(driver_path) # 서비스 객체 생성
browser = webdriver.Chrome(service=service) # 브라우저 객체 생성

# 2. 사이트로 이동
url = "https://www.youtube.com/watch?v=RGZ_IIe3Zg0" # 방문하려는 사이트 주소
browser.get(url) # 사이트 방문

# 2-1. 모든 댓글 관련 컨텐츠 로딩
wait = WebDriverWait(browser, 100)  # 최대 100초까지 대기
last_height = browser.execute_script("return document.documentElement.scrollHeight")  # 현재 스크롤 높이 반환
while True:  # 루프 탈출할 때까지 무한 반복
    browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")  # 스크롤을 끝까지 내리기
    
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#body"))) # 로드될 때까지 대기
    
    new_height = browser.execute_script("return document.documentElement.scrollHeight")  # 새로운 스크롤 높이 반환
    
    if new_height == last_height:  # 새로운 스크롤 높이가 이전 스크롤 높이와 같다면, 더 이상 스크롤 되지 않는다는 뜻이므로 루프 탈출
        break
    else:  # 그렇지 않으면 마지막 스크롤 높이를 저장하고 계속 루프 실행
        last_height = new_height

# 3. 작성자와 댓글 데이터 동기화 수집
comment_items = browser.find_elements(By.CSS_SELECTOR, "#body")  # 댓글의 최상위 요소 추출

data = []
for item in comment_items:
    try:
        # 작성자와 댓글을 각각 추출
        author = item.find_element(By.CSS_SELECTOR, "#author-text").text  # 작성자 닉네임
        comment = item.find_element(By.CSS_SELECTOR, "#content-text").text.replace("\n", " ")  # 댓글 내용
    except Exception as e:
        # 작성자 또는 댓글이 누락된 경우 누락 처리
        author = "작성자 누락"
        comment = "댓글 누락"
    
    data.append({"authors": author, "comments": comment})  # 작성자와 댓글 저장

# 데이터프레임 생성
df = pd.DataFrame(data)

# CSV 파일로 저장
df.to_csv("comments_with_sync.csv", index=False, encoding="utf-8-sig")

# 브라우저 닫기
browser.quit()