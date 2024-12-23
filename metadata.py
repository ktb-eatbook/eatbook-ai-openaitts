import json

from typing import List, Dict, Any

from pydub import AudioSegment

def format_time(seconds: float) -> str:
    """
    초(Seconds)를 "MM:SS" 형태로 변환.
    예: 0.0초 -> "00:00", 2.3초 -> "00:02", 65초 -> "01:05"
    """
    total_seconds = int(seconds)
    m = total_seconds // 60
    s = total_seconds % 60
    return f"{m:02d}:{s:02d}"

def create_metadata(sentences: List[str],
                    audio_segments: List[AudioSegment]) -> Dict[str, Any]:
    metadata = {}
    current_time = 0.0

    for idx, sentence in enumerate(sentences):
        segment = audio_segments[idx]
        duration_sec = len(segment) / 1000.0

        start_str = format_time(current_time)
        end_str   = format_time(current_time + duration_sec)

        metadata[str(idx + 1)] = [sentence, start_str, end_str]

        current_time += duration_sec

    return metadata

def save_metadata(file_name, metadata):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"[INFO] 메타데이터 파일 저장 완료: {file_name}")