import os
import streamlit as st
from datetime import datetime
from fpdf import FPDF
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import ChatMessage
from langchain_community.vectorstores import FAISS
from . import config  # 만약 config.py가 같은 디렉토리에 있는 경우

  # config.py 파일에서 설정을 불러옵니다

def app(dashboard_title):
    
    # 환경 변수 설정
    for key, value in config.LANGCHAIN_ENV.items():
        os.environ[key] = value
    
    print('LangSmith [OpenAI_cws_streamlit] 추적 시작... ')

    # Streamlit 페이지 설정
    
    # CSS 스타일 적용
    st.markdown(config.CSS_STYLE, unsafe_allow_html=True)
    
    # st.info(config.INFO_MESSAGE)
    
    # 세션 상태 초기화
    if "chat_history" not in st.session_state:
        st.session_state['chat_history'] = []
    
    if "store" not in st.session_state:
        st.session_state['store'] = {}
    
    # 함수 정의
    def add_history(role, message):
        st.session_state['chat_history'].append(ChatMessage(role=role, content=message))
    
    def print_history():
        for chat_msg in st.session_state['chat_history']:
            st.chat_message(chat_msg.role).write(chat_msg.content)
    
    def save_chat_to_pdf():
        pdf = FPDF()
        pdf.add_page()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(current_dir, "NanumGothic-Regular.ttf")
        pdf.add_font("NanumGothic", "", font_path, uni=True)       
        pdf.set_font("NanumGothic", size=12)
        
        pdf.set_font("NanumGothic", size=14)
        pdf.cell(200, 10, txt="UOP Aromatics Process Manual Chat History", ln=1, align='C')
        pdf.ln(5)
        
        pdf.set_font("NanumGothic", size=10)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pdf.cell(200, 5, txt=f"생성일시: {current_time}", ln=1)
        pdf.ln(5)
        
        pdf.set_font("NanumGothic", size=10)
        for chat_msg in st.session_state['chat_history']:
            pdf.multi_cell(0, 5, txt=f"{chat_msg.role}: {chat_msg.content}")
            pdf.ln(2)
        
        filename = f"chat_history_{current_time.replace(':', '-')}.pdf"
        pdf.output(filename)
        return filename
    
    def setup_rag_chain(selected_manual, selected_model):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        save_directory = os.path.join(current_dir, f"saved_vectorstore_{selected_manual} Manual")
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.load_local(save_directory, embeddings, allow_dangerous_deserialization=True)
        retriever = vectorstore.as_retriever()
        
        prompt = PromptTemplate.from_template(config.PROMPT_TEMPLATE)
        
        model = ChatOpenAI(
            model_name=selected_model,
            temperature=0.7,
            presence_penalty=0.6,
            frequency_penalty=0.6
        )
        
        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )
        return rag_chain
    
    # 사이드바 설정
    with st.sidebar:
        os.environ["OPENAI_API_KEY"] = config.API_KEY
    
        selected_manual = st.selectbox(
        ':pushpin: Process Manual 선택',
        config.MANUAL_OPTIONS,
        index=None, placeholder="Select Process"
        )
        st.divider()
                
        selected_model = st.selectbox(':pushpin: Chat-Bot 모델선택', config.MODEL_OPTIONS, index=0)
        st.divider()
          
        st.empty()
    
        st.markdown(config.CONTACT_INFO, unsafe_allow_html=True)
    
    # RAG Chain 설정
    rag_chain = ''
    if selected_manual:
        st.caption(f"✅ 선택된 Manual : :blue[{selected_manual} Process]")
        rag_chain = setup_rag_chain(selected_manual, selected_model)
    else:
        st.warning('대화를 시작하기 전 좌측의 Process Manual을 먼저 선택해 주세요.', icon="ℹ️")
        st.stop()
    
    # 채팅 인터페이스
    print_history()
    User_input = st.chat_input(config.CHAT_INPUT_PLACEHOLDER)
    
    if User_input:
        st.chat_message('User').write(User_input)
    
        with st.chat_message('AI'):
            chat_container = st.empty()
            try:
                answer = rag_chain.stream(User_input)
    
                AI_answer = ""
                for token in answer:
                    AI_answer += token
                    chat_container.markdown(AI_answer)
    
                add_history('User', User_input)
                add_history('AI', AI_answer)
            except Exception as e:
                st.error(f"죄송합니다. 응답을 생성하는 동안 오류가 발생했습니다: {str(e)}")
    
    # PDF 저장 버튼
    if st.button(":floppy_disk: PFD로 대화내용 저장"):
        try:
            with st.spinner("대화내용 파일 저장 중..."):
                filename = save_chat_to_pdf()
            st.success(f":heavy_check_mark: 대화 내용 저장 완료 {filename}")
            
            with open(filename, "rb") as file:
                btn = st.download_button(
                    label=":inbox_tray: Download PDF",
                    data=file,
                    file_name=filename,
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"PDF 저장 중 오류가 발생했습니다: {str(e)}")
    