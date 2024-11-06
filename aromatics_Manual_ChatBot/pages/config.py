# config.py

FONT_PATH = "NanumGothic-Regular.ttf"

LANGCHAIN_ENV = {
    'LANGCHAIN_TRACING_V2': 'true',
    'LANGCHAIN_ENDPOINT': 'https://api.smith.langchain.com',
    'LANGCHAIN_API_KEY': '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',
    'LANGCHAIN_PROJECT': 'OpenAI_cws_streamlit'
}

API_KEY = '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'

CSS_STYLE = """
<style>
    .gradient-text {
        font-weight: bold;
        background: -webkit-linear-gradient(left, red, orange);
        background: linear-gradient(to right, red, orange);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline;
        font-size: 3em;
    }
</style>
<div class="gradient-text">UOP Aromatics Process Manual Chat-Bot 💬</div>
"""

INFO_MESSAGE = """
###### * 본 페이지는 UOP Aromaics 공정 Manual에 대해 궁금한 사항을 물어보면 답변해주는 Chat-Bot Page 입니다.
###### * 좌측에서 질문하고 싶은 해당 공정을 선택 하신 후 아래 대화창에서 Chat-Bot 과 대화를 시작해 보세요.
"""

MODEL_OPTIONS = ['gpt-4o-mini']

MANUAL_OPTIONS = [
    'NHT', 'Platforming', 'No.1 CCR', 'No.2 CCR', 'PAREX', 'ISOMAR', 'Sulfolane',
    'No.1 PX ACCS EI&DB', 'No.2 PX ACCS EI&DB', 'No.1 CCR ALHCS EI&DB', 'No.2 CCR CRCS EI&DB'
]

CONTACT_INFO = """
<div style='position: fixed; bottom: 10px; font-size: 0.7em;'>
<hr>
&#128276; 페이지 오류 발생 시 연락처:<br>
&nbsp;&nbsp;&nbsp; 방향족기술팀 최완섭
</div>
"""

CHAT_INPUT_PLACEHOLDER = '대화 tip! 질문의 주요 단어를 영어로 작성해주시면 보다 정확한 결과를 얻을수 있습니다. 예)흡착제 : adsorbent'

PROMPT_TEMPLATE = """
                    당신은 지능적이고 창의적인 AI 어시스턴트입니다. 주어진 질문에 대해 관련 정보를 조합하여 통찰력 있는 답변을 제공해야 합니다.
                    #Context:
                    {context}
                    #Question:
                    {question}
                    위의 정보를 바탕으로 다음 작업을 수행하세요:
                    1. 가중치가 높은 정보를 우선적으로 고려하되, 모든 관련 정보를 종합적으로 분석하세요.
                    2. 정보들 사이의 연관성을 파악하고, 이를 바탕으로 통찰력 있는 답변을 작성하세요.
                    3. 답변에 사용된 주요 정보의 출처를 간략히 언급하여 신뢰성을 높이세요.
                    4. 질문과 직접적으로 관련이 없는 정보는 과감히 제외하세요.
                    5. 필요하다면 제공된 정보를 넘어서는 합리적인 추론을 포함하세요.
                    답변은 한국어로 작성하며, 전문적이면서도 이해하기 쉽게 설명해주세요.
                    """


# PROMPT_TEMPLATE = """
# You are an advanced AI assistant specializing in question-answering tasks based on provided context. Follow these instructions carefully:

# 1. Question Translation:
#    - If the question is in Korean, translate it to English.
#    - Present the translated question as: "Translated Question: [English translation]"
#    - If the question is in Korean, perform Context Analysys using "Translated Question: [English Translation]".

# 2. Context Analysis:
#    - Thoroughly analyze the provided context to find relevant information.
#    - Use only the information from the given context to formulate your answer.

# 3. Answer Formulation:
#    - Provide a comprehensive and detailed answer in English.
#    - Summarize all relevant content from the context.
#    - Aim for a long, detailed explanation.

# 4. Korean Translation:
#    - Translate your English answer into Korean.
#    - Ensure the translation maintains the same level of detail and accuracy.

# 5. Source Citation:
#    - Indicate the specific page numbers or sections in the original document where the information was found.
#    - Format: "Source: Page [number(s)]"

# 6. Response Format:
#    #Translated Question: [If original question was in Korean]
   
#    #English Answer:
#    [Detailed answer in English]
   
#    #Korean Answer (한국어 답변):
#    [Detailed answer in Korean]
   
#    #Source (출처):
#    [Page numbers or sections]

# 7. Handling Unanswerable Questions:
#    - If the answer cannot be found in the provided context, respond with:
#      "해당 내용을 문서에서 찾을 수 없었습니다. 질문의 주요 단어를 영어로 작성해서 다시 한 번 질문해 주세요. 
#      (위에 번역된 질문으로 다시 질문해 보세요)."
#    - Provide the English translation of the original question for reference.

# Remember: Only use the information from the provided context. Do not include external knowledge or personal opinions.

# #Context:
# {context}

# #Question:
# {question}

# """