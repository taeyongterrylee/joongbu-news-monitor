import streamlit as st
import feedparser
import google.generativeai as genai
import urllib.parse
import time

# 1. 페이지 설정
st.set_page_config(page_title="중부상사 비즈니스 리포트", layout="wide")
st.title("📊 중부상사 주류시장 종합 분석 리포트")
st.sidebar.info("오늘의 뉴스 전반을 분석하여 전략적 인사이트를 도출합니다.")

# 2. API 키 및 모델 설정
API_KEY = st.secrets.get("GOOGLE_API_KEY", "")
if not API_KEY:
    st.error("⚠️ API 키 설정이 필요합니다.")
    st.stop()

genai.configure(api_key=API_KEY)
# 2026년 기준 가장 안정적인 모델명 사용
model = genai.GenerativeModel('gemini-2.5-flash')

# 뉴스 수집 함수
def get_news(keyword):
    safe_keyword = urllib.parse.quote(keyword)
    rss_url = f"https://news.google.com/rss/search?q={safe_keyword}+주류&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)
    # 제목과 링크만 추출해서 텍스트로 만듦
    return [f"- {entry.title} ({entry.link})" for entry in feed.entries[:5]]

# 3. 실행 버튼
if st.button('📈 오늘의 시장 종합 분석 시작'):
    keywords = ["주류도매", "주세법 개정"]
    
    all_news_text = ""
    progress_bar = st.progress(0)
    
    with st.spinner('전국 주류 뉴스를 수집 중입니다...'):
        for idx, kw in enumerate(keywords):
            news_items = get_news(kw)
            if news_items:
                all_news_text += f"\n### 키워드: {kw}\n" + "\n".join(news_items) + "\n"
            progress_bar.progress((idx + 1) / len(keywords))

    # 수집된 뉴스 목록을 화면에 살짝 보여줌
    with st.expander("📋 수집된 뉴스 원본 목록 확인"):
        st.markdown(all_news_text)

    # 4. 전체 뉴스 종합 분석 (AI 호출은 딱 한 번!)
    st.divider()
    st.subheader("🤖 AI 전략 컨설턴트의 종합 분석 결과")
    
    with st.spinner('전체 흐름을 읽고 중부상사 맞춤 전략을 짜는 중입니다...'):
        prompt = f"""
        당신은 인천 지역 종합주류도매사 '중부상사'의 수석 전략가입니다.
        아래는 오늘 수집된 주류 시장의 주요 뉴스 목록입니다.
        
        {all_news_text}
        
        이 뉴스 전반을 분석하여 중부상사 이태용 대표님께 다음 4가지 관점에서 종합 리포트를 작성하세요:
        
        1. 📢 시장 핵심 요약: (현재 시장의 가장 큰 흐름 3가지)
        2. 💰 비즈니스 기회: (도매 매출 확대 및 신규 거래처 확보 전략)
        3. ⚠️ 주의가 필요한 리스크: (법규 변화, 단가 상승, 경쟁 심화 등)
        4. 🏃 중부상사 실행 제언: (오늘 바로 영업 현장에서 강조해야 할 점)
        
        분석은 전문적이고 단호하면서도 실행 가능한 방향으로 작성하세요.
        """
        
        try:
            # 전체를 한 번에 분석하므로 훨씬 깊이 있는 결과가 나옵니다.
            response = model.generate_content(prompt)
            st.success("✅ 종합 리포트 작성이 완료되었습니다.")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"종합 분석 중 오류 발생: {e}")
