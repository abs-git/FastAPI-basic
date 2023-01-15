import shutil
from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

UPLOAD_FILES_DIR = './uploaded_files/'

@app.get('/')
def home():
    return {'hello':'world'}


def generate_html_response():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.post('/uploadfile/', response_class=HTMLResponse)
async def create_upload_file(files: List[UploadFile] = File(...)):
    for data in files:
        with open(UPLOAD_FILES_DIR + f'{data.filename}', 'wb') as buffer:
            shutil.copyfileobj(data.file, buffer)

    return generate_html_response()






