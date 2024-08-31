import streamlit as st
import requests
from datetime import datetime
import json

# 설정
NEIS_API_KEY = "your_neis_api_key_here"
SCHOOL_CODE = "7011292"  # 인덕과학기술고등학교 코드
OFFICE_CODE = "B10"  # 서울특별시교육청 코드

# 데이터 파일 경로
DATA_FILE = "survey_data.json"

# 데이터 로드 함수
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"like": 0, "neutral": 0, "dislike": 0}

# 데이터 저장 함수
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# 오늘의 급식 메뉴 가져오기
def get_today_menu():
    today = datetime.now().strftime("%Y%m%d")
    url = f"https://open.neis.go.kr/hub/mealServiceDietInfo"
    params = {
        "KEY": NEIS_API_KEY,
        "Type": "json",
        "ATPT_OFCDC_SC_CODE": OFFICE_CODE,
        "SD_SCHUL_CODE": SCHOOL_CODE,
        "MLSV_YMD": today
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "mealServiceDietInfo" in data:
            menu = data["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"].replace("<br/>", ", ")
            return menu
    return "오늘의 메뉴 정보를 가져올 수 없습니다."

# Streamlit 앱
def main():
    st.set_page_config(page_title="오늘의 급식 만족도 조사", page_icon="🍱")
    st.title("오늘의 급식 만족도 조사")

    # 오늘의 메뉴 표시
    menu = get_today_menu()
    st.subheader(f"오늘의 메뉴: {menu}")

    # 투표 버튼
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("좋아요 👍"):
            vote("like")
    with col2:
        if st.button("보통이에요 😐"):
            vote("neutral")
    with col3:
        if st.button("별로에요 👎"):
            vote("dislike")

    # 결과 표시
    data = load_data()
    total = sum(data.values())
    
    st.subheader("실시간 만족도 결과")
    for option in ["like", "neutral", "dislike"]:
        count = data[option]
        percentage = (count / total * 100) if total > 0 else 0
        st.progress(percentage / 100)
        st.text(f"{option.capitalize()}: {count} ({percentage:.1f}%)")

# 투표 함수
def vote(option):
    data = load_data()
    data[option] += 1
    save_data(data)
    st.experimental_rerun()

if __name__ == "__main__":
    main()
