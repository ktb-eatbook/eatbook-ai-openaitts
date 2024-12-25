import json
import boto3
import io
import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

load_dotenv()

def save_metadata(file_name: str, metadata: dict, s3_metadata_path: str) -> None:
    # s3_metadata_path 파싱 -> 버킷 이름, 업로드 키(prefix) 추출
    parts = s3_metadata_path.split("/", 1)
    if len(parts) < 2:
        raise ValueError(
            "s3_metadata_path 형식이 잘못되었습니다. "
            "예) 'my-bucket/metadata-folder/sub-folder'"
        )
    # 버킷 이름, path 분리
    bucket_name, path_prefix = parts[0], parts[1]

    # S3에 저장할 오브젝트 Key
    s3_key = f"{path_prefix}/{file_name}"

    # JSON 직렬화 -> 메모리 버퍼에 쓰기
    json_bytes = json.dumps(metadata, ensure_ascii=False, indent=2).encode("utf-8")
    buffer = io.BytesIO(json_bytes)
    buffer.seek(0)

    # boto3를 이용한 S3 업로드
    s3_client = boto3.client("s3",
                             aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                             aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                             region_name=os.getenv("AWS_REGION"))
    s3_client.upload_fileobj(buffer, bucket_name, s3_key)

    print(f"[INFO] 메타데이터 파일 저장 완료: {file_name}")

def save_metadata_local(output_path: str, metadata: Dict[str, Any]):
    """로컬에 메타데이터 파일(.json) 저장"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    import json
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)
    print(f"[LOCAL SAVE] Metadata saved at: {output_path}")