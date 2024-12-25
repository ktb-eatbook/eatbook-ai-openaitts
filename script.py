import io
import os
import time
from typing import List, Dict, Any, Optional

from pydub import AudioSegment

from text_module import read_paragraphs_from_text, split_paragraph_into_sentences
from metadata import create_metadata
from save_audio import save_audio, save_audio_local
from save_metadata import save_metadata, save_metadata_local
from gen_tts import gen_tts

def process_text_file(
    text_content: str,
    mode: str = "s3",
    audio_path: Optional[str] = None,
    metadata_path: Optional[str] = None,
    audio_uuid: Optional[str] = None,
    metadata_uuid: Optional[str] = None,
    filename: Optional[str] = None,
    voiceId: Optional[str] = "alloy",
    speed: Optional[float] = 1
) -> List[Dict[str, Any]]:

    start_time = time.time()
    print("[INFO] TTS synthesis start!")

    # 로컬 저장일 경우, output_files 디렉토리 확인/생성
    OUTPUT_DIR = filename
    if mode == "local" and not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 1) 텍스트를 문단으로 분리
    paragraphs = read_paragraphs_from_text(text_content)
    paragraph_count = len(paragraphs)

    results = []

    for paragraph_idx, paragraph in enumerate(paragraphs):
        # 2) 문장을 분리
        sentences = split_paragraph_into_sentences(paragraph)

        # 3) 각 문장별 TTS 수행 후 AudioSegment 생성
        audio_segments = []
        for sentence in sentences:
            # tts 호출 (bytes 형태의 mp3 데이터를 반환한다고 가정)
            audio_data = gen_tts(input_text=sentence,
                                 voiceId=voiceId,
                                 speed=speed)

            if not isinstance(audio_data, bytes):
                audio_data = audio_data.read()

            segment = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")
            audio_segments.append(segment)

        # 4) 문단 내 모든 문장을 하나로 합치기
        combined_audio_segment = AudioSegment.silent(duration=0)
        for seg in audio_segments:
            combined_audio_segment += seg

        # 5) 메타데이터 생성
        metadata = create_metadata(sentences, audio_segments)

        # 6) 파일 이름 설정
        if mode == "s3":
            # S3 업로드 시, 매개변수로 받은 UUID와 경로가 필요
            if not audio_uuid or not metadata_uuid:
                raise ValueError("S3 업로드에는 audio_uuid, metadata_uuid가 필수입니다.")
            if not audio_path or not metadata_path:
                raise ValueError("S3 업로드에는 audio_path, metadata_path가 필수입니다.")

            audio_file_name = audio_uuid
            metadata_file_name = metadata_uuid

            # S3 저장
            save_audio(combined_audio_segment, audio_file_name, audio_path, audio_format="mp3")
            save_metadata(metadata_file_name, metadata, metadata_path)

        elif mode == "local":
            # 로컬에 저장할 경우, output_files 내에 paragraph 인덱스 기반 파일명 생성
            audio_file_name = f"{filename}_{paragraph_idx+1}.mp3"
            metadata_file_name = f"{filename}_{paragraph_idx+1}.json"

            local_audio_path = os.path.join(OUTPUT_DIR, audio_file_name)
            local_metadata_path = os.path.join(OUTPUT_DIR, metadata_file_name)

            # 로컬 저장
            save_audio_local(combined_audio_segment, local_audio_path, audio_format="mp3")
            save_metadata_local(local_metadata_path, metadata)

        else:
            raise ValueError("mode 파라미터는 's3' 또는 'local' 이어야 합니다.")

        # 결과 리스트에 저장
        results.append({
            "paragraph_index": paragraph_idx + 1,
            "audio_file": audio_file_name,
            "metadata_file": metadata_file_name,
            "sentences": sentences
        })

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"[INFO] 문단 : {paragraph_count}개")
    print(f"[INFO] 총 소요 시간: {elapsed_time:.2f}초")

    return results