# Library import
import streamlit as st
from streamlit_option_menu import option_menu # 메뉴 버튼을 만들기 위한 component 출처: https://github.com/victoryhb/streamlit-option-menu

# 개별 Dashboard를 구현하기 위한 class 정의
class MultiPage:
    def __init__(self, dashboard_title):
        """ 개별 dashboard의 page들을 저장하기 위해 empty list 생성
         Args:
             dashboard_title : dashboard_portal.py 에서 지정한 dashboard_title
        """
        self.dashboard_title = dashboard_title
        self.pages = {}

    def add_page(self, title, func, icon=None):
        """ 개별 dashboard page들을 추가하기 위한 class method
        Args:
            title ([str]): page 이름
            func: page 별 Python function
            icon : option menu에 표기될 page 별 icon 이름 ( https://icons.getbootstrap.com/ 에서 icon name 문자열 입력)
        """

        self.pages[title] = {'function' : func, 'icon' : icon}

    def run(self):
        # page 선택을 위해 option menu 생성
        with st.sidebar:
            page = option_menu(
                menu_title=None,
                options = list(self.pages.keys()),
                icons= [i['icon'] for i in self.pages.values()]
            )

        # 선택된 page 구동 [하위 메소드 구동을 위해 선택된 dashboard title 인수로 입력. ex) 제안 사항 메일 알림]
        self.pages[page]['function'](self.dashboard_title)