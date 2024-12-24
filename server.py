from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, AnyHttpUrl
import uuid
import requests
from script import process_text_file
from dotenv import load_dotenv
import os
import boto3
load_dotenv()

# uuid를 파일명으로
app = FastAPI()

# 요청 데이터 모델 정의
class TTSRequest(BaseModel):
    novelId: str
    episodeId: str
    scriptId: str

def get_s3_audio_path(novel_id: str, episode_id: str, audio_uuid: str) -> str:
    """
    ktb-eatbook-private 버킷 내부에
    {novelId}/episodes/{episodeId}/audio/{audio_uuid} 경로를 반환하는 함수
    """
    bucket_name = os.getenv("BUCKET_NAME")
    return f"{bucket_name}/{novel_id}/episodes/{episode_id}/audio"

def get_s3_metadata_path(novel_id: str, episode_id: str, metadata_uuid: str) -> str:
    """
    ktb-eatbook-private 버킷 내부에
    {novelId}/episodes/{episodeId}/audio/{audio_uuid} 경로를 반환하는 함수
    """
    bucket_name = os.getenv("BUCKET_NAME")
    return f"{bucket_name}/{novel_id}/episodes/{episode_id}/metadata"

def read_text_file(novel_id: str, episode_id: str, script_id: str) -> str:
    """
    S3 Presigned URL을 통해 텍스트 파일 내용을 반환
    """
    try:
        s3 = boto3.client("s3",
                                 aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                                 aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                                 region_name=os.getenv("AWS_REGION"))

        bucket_name = os.getenv("BUCKET_NAME")

        text_file_path = f"{novel_id}/episodes/{episode_id}/script/{script_id}"

        response = s3.get_object(Bucket=bucket_name, Key=text_file_path)

        text = response['Body'].read().decode("utf-8")

        #response.raise_for_status()
        return text

    except Exception as e:
        raise ValueError(f"Failed to read file from presigned URL: {e}") from e
@app.post("/tts")
async def create_tts(request: TTSRequest):
    try:
        # uuid 생성

        audio_uuid = str(uuid.uuid4())
        metadata_uuid = str(uuid.uuid4())

        # s3 버킷 경로 생성
        audio_path = get_s3_audio_path(request.novelId, request.episodeId, audio_uuid)
        metadata_path = get_s3_metadata_path(request.novelId, request.episodeId, metadata_uuid)

        # 1개 episode text 데이터
        episode = read_text_file(request.novelId, request.episodeId, request.scriptId)
        print("restart")
        process_text_file(episode, audio_path, metadata_path,audio_uuid, metadata_uuid)

        return {
            "success": True,
            "audio_uuid": audio_uuid,
            "metadata_uuid": metadata_uuid
        }

    except Exception as e:
        # 처리 중 오류가 발생한 경우
        return {
            "success": False,
            "error": "음성 생성 실패"
        }

if __name__ == "__main__":
     import uvicorn
     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)