import io
import os

import boto3
from pydub import AudioSegment
from dotenv import load_dotenv
load_dotenv()


def save_audio(audio_segment: AudioSegment, file_name: str, s3_audio_path: str, audio_format: str = "mp3") -> None:
    # s3_audio_path 파싱 -> 버킷 이름, 업로드 키(prefix) 추출
    parts = s3_audio_path.split("/", 1)
    if len(parts) < 2:
        raise ValueError(
            f"s3_audio_path 형식이 잘못되었습니다. "
            f"예) 'my-bucket/my-folder/sub-folder'"
        )
    # 버킷 이름, path 분리
    bucket_name, path_prefix = parts[0], parts[1]

    # S3에 저장할 오브젝트 Key
    s3_key = f"{path_prefix}/{file_name}"

    # 대충 오디오관련
    audio_buffer = io.BytesIO()
    audio_segment.export(audio_buffer, format=audio_format)
    audio_buffer.seek(0)  # export 후 버퍼 포인터를 처음으로 이동

    print(f"[INFO] 음성 파일 생성 완료: {file_name}")

    # boto3를 이용해 S3에 업로드
    s3_client = boto3.client("s3",
                             aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                             aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                             region_name=os.getenv("AWS_REGION"))
    s3_client.upload_fileobj(audio_buffer, bucket_name, s3_key)

    print(f"[INFO] 음성 파일 저장 완료: {file_name}")

def save_audio_local(audio_segment: AudioSegment, output_path: str, audio_format="mp3"):
    """로컬에 오디오 파일 저장"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    audio_segment.export(output_path, format=audio_format)

    print(f"[LOCAL SAVE] .mp3 saved at: {output_path}")
