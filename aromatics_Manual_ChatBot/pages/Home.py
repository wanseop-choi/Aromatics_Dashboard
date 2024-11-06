import streamlit as st
import os

def app(dashboard_title):
    # 현재 파일이 있는 디렉토리의 경로를 가져옵니다
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 이미지 파일 경로
    image_path = os.path.join(current_dir, 'main_image.png')
    
    # 이미지 표시
    st.image(image_path, use_column_width=True)
    
    # 여백 추가
    st.markdown("<br>", unsafe_allow_html=True)

    # 스타일 정의
    st.markdown("""
    <style>
    @font-face {
        font-family: 'NanumGothic';
        src: url('NanumGothic-Regular') format('truetype');
    }
    .big-font {
        font-family: 'NanumGothic';
        font-size: 18px;
        color: #000000;  /* 글자색을 검정색으로 지정 */
    }
    .custom-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        color: #000000;  /* 컨테이너 내 기본 글자색을 검정색으로 지정 */
    }
    </style>
    """, unsafe_allow_html=True)

    # 컨테이너 생성 및 내용 표시
    container = st.container()
    with container:
        st.markdown('''
        <div class="custom-container">
            <h4 style="color: #000000;">1. Aromatics Manual Chat-Bot</h4>
            <div class="big-font">
                - UOP Licensor의 GSC 방향족공정 Manual을 학습한 Chat-Bot입니다.<br>
                - 좌측 메뉴의 Manual Chat-Bot 클릭 및 Process Manual을 선택하신 후 아래 대화창에서 Chat-Bot 과 대화를 시작해 보세요.<br>
                - 해당 Process Manual에 대해 궁금한 사항을 물어보시면 친철히 답변합니다.
            </div>
        </div>
        ''', unsafe_allow_html=True)
                              