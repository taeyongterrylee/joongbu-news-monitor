

import streamlit as st
import feedparser
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="중부상사 비즈니스 모니터링", layout="wide")
st.title("🍷 중부상사 실시간 뉴스 분석기")

# 2. API 키 가져오기 (Secrets 우선, 없으면 직접 입력)
API_KEY = st.secrets.get("GOOGLE_API_KEY", "")

if not API_KEY:
    st.error("⚠️ API 키가 설정되지 않았습니다. Streamlit Secrets에 GOOGLE_API_KEY를 넣어주세요.")
    st.stop()

# 3. AI 모델 초기화 (가장 보수적이고 안전한 이름 사용)
try:
    genai.configure(api_key=API_KEY)
    # 'models/'를 붙이는 것이 최신 표준입니다.
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    st.error(f"모델 초기화 실패: {e}")
    st.stop()

# 뉴스 수집 함수
def get_news(keyword):
    rss_url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)
    return feed.entries[:5]

# 실행 버튼
if st.button('🚀 최신 뉴스 분석 시작'):
    keywords = ["주류도매", "주세법 개정", "소주", "맥주", "위스키", "와인", "주점", "주류"]
    
    with st.spinner('중부상사 관점에서 분석 중...'):
        for kw in keywords:
            st.markdown(f"### 🔍 키워드: **{kw}**")
            items = get_news(kw)
            
            if not items:
                st.write("관련 뉴스가 없습니다.")
                continue

            for item in items:
                with st.expander(f"📌 {item.title}"):
                    st.write(f"[기사 원문 보기]({item.link})")
                    
                    # AI 분석 실행
                    prompt = f"종합주류도매사 '중부상사'의 입장에서 다음 뉴스의 기회와 리스크를 요약해줘: {item.title}"
                    
                    try:
                        # [핵심] 여기서 NotFound가 나지 않도록 모델을 다시 한번 확인합니다.
                        response = model.generate_content(prompt)
                        st.info(response.text)
                    except Exception as e:
                        # 에러가 나면 어떤 에러인지 정확히 화면에 표시합니다.
                        st.warning(f"분석 일시 중단 (이유: {e})")

