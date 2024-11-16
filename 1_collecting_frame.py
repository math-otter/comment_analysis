# 0. 프로그램에 필요한 패키지 임포트
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

# 1. 브라우저 열기
driver_path = "chromedriver.exe" # 크롬 드라이버 사용
service = Service(driver_path) # 서비스 객체 생성
browser = webdriver.Chrome(service=service) # 브라우저 객체 생성

# 2. 사이트로 이동
url = "https://www.youtube.com/watch?v=RGZ_IIe3Zg0" # 방문하려는 사이트 주소
browser.get(url) # 사이트 방문
time.sleep(5) # 컨텐츠가 모두 로드될 때까지 일정 시간 대기

# 2-1. 모든 댓글 로딩
last_height = browser.execute_script("return document.documentElement.scrollHeight") # 현재 스크롤 높이 반환
while True: # 루프 탈출할 때까지 무한 반복
    browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)") # 스크롤을 끝까지 내리기
    time.sleep(5)  # 페이지 로드 시간 대기
    new_height = browser.execute_script("return document.documentElement.scrollHeight") # 새로운 스크롤 높이 반환
    if new_height == last_height:  # 새로운 스크롤 높이가 이전 스크롤 높이와 같다면, 더 이상 스크롤 되지 않는다는 뜻이므로 루프 탈출
        break
    else: # 그렇지 않으면 마지막 스크롤 높이를 저장하고 계속 루프 실행
        last_height = new_height 

# 3. 댓글 요소 추출 및 저장
authors = browser.find_elements(By.CSS_SELECTOR, "#author-text") # 작성자 닉네임 요소 추출
authors = [author.text for author in authors] # 텍스트 추출
comments = browser.find_elements(By.CSS_SELECTOR, "#content-text") # 작성된 댓글 요소 추출
comments = [comment.text.replace("\n", " ") for comment in comments] # 텍스트 추출 및 줄바꿈 제거
df = pd.DataFrame({"authors": authors, "comments": comments}) # 데이터 프레임으로 저장
df.to_csv("comments.csv", index=False, encoding="utf-8-sig") # csv 파일로 저장

# 4. 브라우저 닫기
input("브라우저를 닫으려면 Enter 키를 누르세요...") # Enter 키 입력을 기다리면서 브라우저 열어두기
browser.quit() # Enter 키 입력 후 브라우저 종료