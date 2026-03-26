import streamlit as st
import feedparser
import google.generativeai as genai
import urllib.parse
import time

# 1. 페이지 설정
st.set_page_config(page_title="중부상사 비즈니스 모니터링", layout="wide")
st.title("🍷 중부상사 실시간 뉴스 분석기")
st.sidebar.info("중부상사 맞춤형 주류 시장 인사이트")

# 2. API 키 가져오기
API_KEY = st.secrets.get("GOOGLE_API_KEY", "")

if not API_KEY:
    st.error("⚠️ API 키가 설정되지 않았습니다. Streamlit Secrets에 GOOGLE_API_KEY를 넣어주세요.")
    st.stop()

# 3. AI 모델 초기화
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('models/gemini-1.0-pro')
except Exception as e:
    st.error(f"모델 초기화 실패: {e}")
    st.stop()

# 4. 뉴스 수집 함수
def get_news(keyword):
    safe_keyword = urllib.parse.quote(keyword)
    # 검색 결과의 신뢰도를 높이기 위해 '주류' 관련 맥락을 추가하여 검색합니다.
    rss_url = f"https://news.google.com/rss/search?q={safe_keyword}+주류&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)
    return feed.entries[:5]

# 5. 실행 버튼
if st.button('🚀 전 품목 실시간 뉴스 분석 시작'):
    # 대표님이 요청하신 키워드 리스트
    keywords = ["주류도매", "주세법 개정"]
    #, "소주", "맥주", "위스키", "와인", "주점", "주류"
    
    # 분석 진행 상태 표시
    progress_text = "전체 품목 뉴스를 수집하고 분석 중입니다. 잠시만 기다려 주세요..."
    my_bar = st.progress(0)
    
    with st.spinner(progress_text):
        for idx, kw in enumerate(keywords):
            st.markdown(f"## 🔍 키워드: **{kw}**")
            items = get_news(kw)
            
            if not items:
                st.write(f"'{kw}' 관련 최신 뉴스가 없습니다.")
            else:
                for item in items:
                    with st.expander(f"📌 {item.title}"):
                        st.write(f"[기사 원문 보기]({item.link})")
                        
                        # 중부상사 관점의 맞춤형 프롬프트
                        prompt = f"""
                        당신은 인천 지역 종합주류도매사 '중부상사'의 전략 컨설턴트입니다.
                        다음 뉴스를 읽고 도매업자의 입장에서 분석하세요.
                        뉴스 제목: {item.title}
                        
                        출력 형식:
                        1. 사업적 기회:
                        2. 리스크 요소:
                        3. 현장 대응 전략:
                        """
                        
                        try:
                            # [핵심] 유료 계정이라도 API 호출 간격을 위해 1.2초 쉽니다.
                            time.sleep(1.2) 
                            response = model.generate_content(prompt)
                            st.info(response.text)
                        except Exception as e:
                            # 에러 원인을 화면에 구체적으로 표시합니다.
                            st.warning(f"분석 일시 중단 (원인: {e})")
            
            # 진행바 업데이트
            my_bar.progress((idx + 1) / len(keywords))
    
    st.success("✅ 모든 키워드 분석이 완료되었습니다!")
