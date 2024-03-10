from email.mime.text import MIMEText

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from smtplib import SMTP_SSL

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def hello():
    return {'Details': 'Add /docs'}


@app.post("/send_mail/")
def send_mail(
    send_to: str,
    header: str,
    text: str,
    MAIL_USERNAME: str,
    MAIL_SERVER: str,
    MAIL_PORT: str,
    MAIL_PASSWORD: str
):
    sent = send_code_to_email_utils(send_to, header, text, MAIL_USERNAME, MAIL_SERVER, MAIL_PORT, MAIL_PASSWORD)
    return sent


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})



def send_code_to_email_utils(send_to, header, text, MAIL_USERNAME, MAIL_SERVER, MAIL_PORT, MAIL_PASSWORD):
    try:
        msg = MIMEText(text, "html")
        msg['Subject'] = f'{header}'
        msg['From'] = f'MAIL_FROM <{MAIL_USERNAME}>'
        msg['To'] = send_to

        # Connect to the email server
        server = SMTP_SSL(MAIL_SERVER, MAIL_PORT)
        server.login(MAIL_USERNAME, MAIL_PASSWORD)

        # Send the email
        server.send_message(msg)
        server.quit()
        return True

    except Exception as e:
        print(e)
        return False
