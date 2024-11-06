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
        color: #000000;
    }
    .custom-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 내용 마크다운
    container = st.container()
    with container:
        st.markdown('''
        <div class="custom-container">
            <h4 style="color: #000000; margin-bottom: 0px;">1. Monitoring</h4>
            <div class="big-font" style="margin-bottom: 5px;">
                - No.2 PX 공정 (PAREX/ISOMAR/Xylene)의 주요 운전현황을 Trend로 모니터링 할수 있습니다.
            </div>            
            <h4 style="color: #000000; margin-bottom: 0px;">2. 머신러닝 예측 결과</h4>
            <div class="big-font" style="margin-bottom: 5px;">
                - 머신러닝 모델의 분석 결과를 Trend 및 Table로 확인할 수 있습니다.
            </div>            
            <h4 style="color: #000000; margin-bottom: 0px;">3. Purity Simulation</h4>
            <div class="big-font" style="margin-bottom: 5px;">
                - 사용자가 지정한 운전 조건에서 No.2 PAREX PX 제품(Finishing BTM PX) Purity 예측값을 확인할 수 있습니다.<br>
                - 또한, 사용자가 지정한 Target Purity를 맞추기 위한 예상 L2/A 값을 확인할수 있습니다.<br>
                &nbsp;&nbsp;(⚠️주의! 예상된 L2/A 값은 머신러닝 모델을 통한 예측값이므로, 실제와 차이가 있을수 있으니 참고치로 활용바랍니다.)
            </div>            
            <h4 style="color: #000000; margin-bottom: 0px;">4. 개선사항 제안</h4>
            <div class="big-font">
                - 분석 모델 또는 대시보드 관련 개선 필요사항을 제안할 수 있는 페이지입니다.
            </div>
        </div>
        ''', unsafe_allow_html=True)