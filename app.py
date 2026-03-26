import streamlit as st
import feedparser
import google.generativeai as genai

# 1. 보안 설정 (Streamlit Cloud의 Secrets에서 키를 가져옵니다)
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
    models = genai.GenerativeModel('models/gemini-1.5-pro')
except:
    st.error("API 키 설정이 필요합니다. Streamlit Settings > Secrets에 GOOGLE_API_KEY를 입력해주세요.")

# 웹사이트 화면 구성
st.set_page_config(page_title="중부상사 비즈니스 인텔리전스", layout="wide")
st.title("🍷 중부상사 실시간 뉴스 모니터링 & 분석")
st.sidebar.info("중부상사의 사업적 기회와 리스크를 AI가 분석합니다.")

# 뉴스 수집 함수
def get_news(keyword):
    rss_url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)
    return feed.entries[:5]

# 실행 버튼
if st.button('🚀 최신 뉴스 분석하기'):
    keywords = ["주류도매", "주세법 개정", "소주", "맥주", "위스키", "와인", "주점", "주류"]
    
    for kw in keywords:
        st.subheader(f"🔍 키워드: {kw}")
        news_items = get_news(kw)
        
        for item in news_items:
            with st.expander(f"📌 {item.title}"):
                st.write(f"[기사 원문 보기]({item.link})")
                
                # AI 분석 요청
                prompt = f"""
                당신은 종합주류도매업체 '중부상사'의 전략가입니다.
                다음 뉴스가 중부상사의 사업에 줄 영향을 분석하세요.
                뉴스 제목: {item.title}
                
                1. 기회 요인:
                2. 리스크 요소:
                3. 권장 대응 방향:
                """
                response = model.generate_content(prompt)
                st.info(response.text)
