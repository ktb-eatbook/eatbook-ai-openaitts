from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, AnyHttpUrl
import uuid
import requests
from script import process_text_file
from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI()

# 요청 데이터 모델 정의
class TTSRequest(BaseModel):
    s3_presigned_url: AnyHttpUrl
    novelId: str
    episodeId: str

def get_s3_audio_path(novel_id: str, episode_id: str, audio_uuid: str) -> str:
    """
    ktb-eatbook-private 버킷 내부에
    {novelId}/episodes/{episodeId}/audio/{audio_uuid} 경로를 반환하는 함수
    """
    bucket_name = os.getenv("BUCKET_NAME")
    return f"{bucket_name}/{novel_id}/episodes/{episode_id}/audio/{audio_uuid}"

def get_s3_metadata_path(novel_id: str, episode_id: str, metadata_uuid: str) -> str:
    """
    ktb-eatbook-private 버킷 내부에
    {novelId}/episodes/{episodeId}/audio/{audio_uuid} 경로를 반환하는 함수
    """
    bucket_name = "ktb-eatbook-private"
    return f"{bucket_name}/{novel_id}/episodes/{episode_id}/audio/{metadata_uuid}"

def read_text_file_from_presigned_url(presigned_url: AnyHttpUrl) -> str:
    """
    S3 Presigned URL을 통해 텍스트 파일 내용을 반환
    """
    try:
        response = requests.get(presigned_url)
        response.raise_for_status()
        return response.text

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
        episode = read_text_file_from_presigned_url(request.s3_presigned_url)

        process_text_file(episode, audio_path, metadata_path)

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