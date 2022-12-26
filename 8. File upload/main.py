# File 클래스는 Form 클래스를 상속하기 때문에 file 들은 form data로 업로드 된다. 
# UploadFile 클래스는 스풀링을 사용함으로서 큰 사이즈의 파일들을 메모리에 모두 올리지 않고 처리할 수 있다.

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post('/files/')
async def create_file(file: bytes = File(...)):
    return {'file_size': len(file)}

@app.post('/uploadfile/')
async def create_upload_file(file: UploadFile = File(...)):
    return {'filename': file.filename}

