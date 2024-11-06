## Public import
import streamlit as st
from streamlit_option_menu import option_menu

## Custom import
from common.multipage import MultiPage
from .pages import Home
from .pages import Monitoring
from .pages import ML_Prediction
from .pages import Purity_Simulation
from .pages import suggestion



## 해당 app이 선택된 경우, dashboard_portal.py에서 설정한 이름을 변수로 입력받음
def app(dashboard_title):
    ## 대시보드 Title 표기
    # st.title(f'{dashboard_title} 대시보드')

    ## multipage instance 생성
    pages = MultiPage(dashboard_title)

    ## pages 패키지 내 개별 page app에 추가
    pages.add_page('Home', Home.app,'house')
    pages.add_page('Monitoring', Monitoring.app, 'search')
    pages.add_page('머신러닝 예측 결과', ML_Prediction.app,'lightbulb-fill')
    pages.add_page('Purity Simulation', Purity_Simulation.app,'calculator')
    pages.add_page('개선 제안', suggestion.app,'megaphone')

    ## app 기동
    pages.run()
