## Public import
import streamlit as st

## Custom import
from common.multiapp import MultiApp
import projects.no2_px_ml.dashboard
import projects.aromatics_Manual_ChatBot.dashboard


## page configuration 지정
page_title = 'Aromatics Dashboard'
st.set_page_config(page_title=page_title, page_icon='gs_logo.png', layout='wide')


# 기본 삽입된 회면 상단 수평선 색상 변경
st.markdown( """
        <style>
            .css-fk4es0{        
            background-image : linear-gradient(90deg, rgb(0, 168, 149), rgb(255, 253, 128))
            }
        </style>
         """, unsafe_allow_html=True)

# 상단 여백 줄이기
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

## MultiApp instance 생성
dashboard_portal = MultiApp()

## projects 패키지 내 개별 dashboard app을 dashboard_portal에 추가
dashboard_portal.add_app('No.2 PX Monitoring & Purity 예측 :mag_right:', projects.no2_px_ml.dashboard.app)
dashboard_portal.add_app('Aromatics Manual Chat-Bot :speech_balloon:', projects.aromatics_Manual_ChatBot.dashboard.app)


## 기동
dashboard_portal.run()