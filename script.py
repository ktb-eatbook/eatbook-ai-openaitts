import io
import os
import time
from typing import List, Dict, Any

from pydub import AudioSegment

from text_module import read_paragraphs_from_text, split_paragraph_into_sentences
from metadata import create_metadata, save_metadata
from save_audio import save_audio
from gen_tts import gen_tts

OUTPUT_DIR = "output_files"

def process_text_file(text_content: str) -> List[Dict[str, Any]]:
    """
    전체 txt 내용을 받아서
    Text_content : txt 읽어온 문자열 입력받아 문단별 mp3, 메타데이터 생성
    """
    start_time = time.time()

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    #문단 분리
    paragraphs = read_paragraphs_from_text(text_content)
    paragraph_count = len(paragraphs)

    results = []

    for paragraph_idx, paragraph in enumerate(paragraphs):
        #문장분리
        sentences = split_paragraph_into_sentences(paragraph)

        # 문장별 오디오 처리
        audio_segments = []
        for sentence in sentences:
            # tts 호출
            audio_data = gen_tts(sentence)

            if not isinstance(audio_data, bytes):
                audio_data = audio_data.read()

            segment = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")
            audio_segments.append(segment)

        # 문단 단위로 합치기
        combined_audio_segment = AudioSegment.silent(duration=0)
        for seg in audio_segments:
            combined_audio_segment += seg

        # 파일명 설정
        audio_file_name = os.path.join(OUTPUT_DIR, f"paragraph_{paragraph_idx + 1}.mp3")
        metadata_file_name = os.path.join(OUTPUT_DIR, f"paragraph_{paragraph_idx + 1}.json")

        # 최종 합쳐진 오디오 파일로 내보내기
        save_audio(combined_audio_segment, audio_file_name, audio_format="mp3")

        # 메타데이터 생성
        metadata = create_metadata(sentences, audio_segments)

        # 메타데이터 저장
        save_metadata(metadata_file_name, metadata)

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
