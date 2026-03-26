import streamlit as st
import feedparser
import google.generativeai as genai

# 웹사이트 상단 설정
st.set_page_config(page_title="중부상사 비즈니스 모니터링", layout="wide")
st.title("🍷 중부상사 실시간 뉴스 분석기")

# 1. API 키 설정 (보안 방식)
# 만약 Secrets 설정이 어려우시면 아래 따옴표 안에 직접 키를 넣으셔도 됩니다.
# 예: API_KEY = "AIza..."
API_KEY = st.secrets.get("GOOGLE_API_KEY", "여기에_직접_키를_넣으셔도_됩니다")

if not API_KEY or API_KEY == "여기에_직접_키를_넣으셔도_됩니다":
    st.error("⚠️ API 키가 설정되지 않았습니다. Streamlit Secrets에 키를 넣거나 코드에 직접 입력해주세요.")
    st.stop()

# 2. AI 모델 초기화 (에러 방지를 위해 전역 설정)
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

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
