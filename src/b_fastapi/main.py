from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from pydantic import BaseModel
import os
import shutil
import pymysql
from datetime import datetime
import uuid
import pandas as pd
from fastapi.responses import JSONResponse

app = FastAPI()

class Message(BaseModel):
    message: str

@app.post("/")
async def receive_message(message: Message):
    # 받은 메시지를 로그에 출력합니다.
    print(message.message)
    return {"Received message": message.message}

# 로그 파일 경로
LOG_FILE_PATH = "./upload_log.txt"

@app.post("/upload_image/")
async def upload_image(
    file: UploadFile = File(...), 
    date: str = Form(...),
    time: str = Form(...),
    weekday: str = Form(...)
):
    print(date)
    print(time)
    # 허용된 이미지 확장자 목록
    allowed_extensions = {"jpeg", "jpg", "png"}

    # 파일 확장자 확인
    file_extension = file.filename.split('.')[-1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type. Only jpeg, jpg, and png files are allowed.")

    # 업로드 디렉토리 지정
    upload_directory = "./uploaded_images"
    os.makedirs(upload_directory, exist_ok=True)  # 디렉토리가 없으면 생성

    # 고유한 파일명 생성 (UUID 사용)
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_location = os.path.join(upload_directory, unique_filename)

    # 파일 저장
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # 현재 시간 저장
    request_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

   # 로그 파일에 파일 경로 및 관련 정보 저장
    log_entry = f"Time: {request_time}, File Path: {file_location}, Original File Name: {file.filename}\n"
    with open(LOG_FILE_PATH, "a") as log_file:
        log_file.write(log_entry)

    # 업로드 결과 반환
    return {
        "status": "success",
        "filename": file.filename,
        "file_location": file_location,
        "time": request_time
    }

@app.get("/show_predicts/")
async def upload_image(
    #date_time: str = Form(...),
):

    # 샘플 데이터 생성
    data = {
        "이름": ["홍길동", "이순신", "강감찬", "유관순"],
        "나이": [25, 32, 45, 29],
        "직업": ["의사", "장군", "수군", "학생"],
    }
    df = pd.DataFrame(data)
    return JSONResponse(content=df.to_dict(orient="records"))


