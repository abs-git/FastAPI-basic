import shutil
import os

from typing import List
from fastapi import FastAPI, Request, Depends
from fastapi import File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from schemas import AwesomForm

app = FastAPI()

templates = Jinja2Templates(directory='templates')

################################################################################################
# html sample

@app.get('/home/', response_class=HTMLResponse)
def home(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('home.html', context)

@app.get('/home/{user_name}', response_class=HTMLResponse)
def write_home(request: Request, user_name: str):
    context = {'request': request,
               'username': user_name}
    return templates.TemplateResponse('home.html', context)


################################################################################################
# file response and return

UPLOAD_FILES_DIR = './uploaded_files/'

@app.get('/files')
def files():
    file_path = os.path.join(UPLOAD_FILES_DIR, 'numbers0.json')
    return FileResponse(file_path, media_type="json")



################################################################################################
# Login and file upload form sample

@app.get('/awesome', response_class=HTMLResponse)
def get_form(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('awesome.html', context) 


@app.post('/awesome', response_class=HTMLResponse)
def post_form(request: Request, form_data: AwesomForm = Depends(AwesomForm.as_form)):
    print(form_data)
    context = {'request': request}
    return templates.TemplateResponse('awesome.html', context) 


################################################################################################
# file upload

UPLOAD_FILES_DIR = './uploaded_files/'

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

