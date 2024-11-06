# Library import
import streamlit as st

# 여러 dashboard app을 담는 class 정의
class MultiApp:
    def __init__(self):
        """ dashboard app들을 저장하기 위한 empty list 생성"""
        self.apps = []

    def add_app(self, title, func):
        """ dashboard app들을 추가하기 위한 class method
        Args:
            title ([str]): dashboard 이름
            func: dashboard 별 Python function
        """

        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        # dashboard 선택을 위해 sidebar에 selectbox 구현
        st.sidebar.header('**:rainbow[Aromatics Process Dashboard]**')
        app = st.sidebar.radio(
            'Manu Select',
            self.apps,
            format_func=lambda app: app['title']
        )
        st.sidebar.write("")  # 한 줄 공백
        st.sidebar.write("")  # 두 번째 줄 공백
        # 선택된 dashboard app 구동 [하위 메소드 구동을 위해 선택된 dashboard title 인수로 입력. ex) 제안 사항 메일 알림]
        app['function'](app['title'])