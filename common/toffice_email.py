import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(mail_from, mail_to, subject=None, content=None, files=[]):
    s = smtplib.SMTP('203.245.127.10', 25) #GSC 사내 SMTP 서버 주소 및 포트 지정

    # TLS 보안 시작
    #s.starttls() #GS칼텍스 SMTP는 TLS 인증 불필요

    # 로그인 인증
    #s.login('지메일 계정', '앱 비밀번호') #GS칼텍스 SMTP는 계정 인증 불필요

    # 메일 객체 생성 및 수신인, 발신인, 제목 설정
    msg = MIMEMultipart()
    msg['From'] = mail_from
    msg['To'] = mail_to
    msg['Subject'] = subject

    # 파일 첨부
    attachment_list = '<br><br><b>※ 첨부 파일 목록</b><br>' #본문 내 기재할 첨부파일 리스트 문자열 생성
    for i, file in enumerate(files):
        part = MIMEBase('application', 'octet_stream')
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=file.name) #한글파일명은 깨지는 문제 발생(2022.02.10)
        msg.attach(part)

        attachment_list += f'{i + 1}. {file.name}<br>' # 첨부파일 리스트에 추가

    # 메일 본문 설정
    content = content.replace('\n', '<br>') # 입력받은 내용에서 줄바꿈 문자 변경 (html 포맷팅 목적)
    html_content = f"""
        <p style="line-height: 1.5; font-family: 맑은 고딕; font-size: 10pt; margin-top: 0px; margin-bottom: 0px;">
        {content+attachment_list}
        </p>
    """
    msg.attach(MIMEText(html_content, 'html')) #html형태로 msg 기록

    # 메일 송부
    s.send_message(msg)

    # 세션 종료
    s.quit()