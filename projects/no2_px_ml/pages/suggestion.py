import streamlit as st
from common import toffice_email


def app(dashboard_title):
    # Side bar

    # Main Page
    st.subheader('개선 사항 제안')
    st.write('''
    - No.2 PX Unit Dashboard 사용 관련하여, 개선 필요사항이 있으시면 부담없이 제안주시기 바랍니다.
    - 아래 작성하여 제안해주신 사항은 익명으로 전달받으며, 해당 내용 검토하여 추가 개선을 진행하도록 하겠습니다.
    - 담당자 : 방향족기술팀 최완섭 책임
    ''')

    columns = st.columns([3, 1])  # 2개의 칼럼을 폭 3:1 크기로 생성
    with columns[0]:
        title = st.text_input('제목', value='')
    with columns[1]:
        name = st.text_input('이름', value='')

    content = st.text_area('내용', height=250, value='')
    files = st.file_uploader('첨부파일', accept_multiple_files=True)

    if st.button('제출'):
        if '' in [title, name, content]:  # 필수 기재 항목 누락 시 에러메시지 출력
            st.error('제목, 이름, 내용을 모두 기재해주세요.')

        else:  # 제안사항 이메일 전송
            content = f'1. 제안자 : {name}\n\n2. 제안내용\n' + content
            toffice_email.send_email('notice@dashboard.com', 'wschoi@gscaltex.com',
                                     subject=f'[신규 제안 : {dashboard_title}] {title} (제안자 : {name})', content=content,
                                     files=files)
            st.success('제출이 완료되었습니다.')