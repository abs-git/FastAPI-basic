from fastapi import Form, File, UploadFile
from pydantic import BaseModel

class AwesomForm(BaseModel):
    username: str
    password: str
    file: UploadFile

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        password: str = Form(...),
        file: UploadFile = File(...)
    ):
        return cls(
            username=username,
            password=password,
            file = file
        )