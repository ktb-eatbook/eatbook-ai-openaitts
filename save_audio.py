import io
from pydub import AudioSegment


def save_audio(audio_segment: AudioSegment, file_name: str, audio_format: str = "mp3") -> None:
    """
    Local 저장버전
    """
    audio_data = io.BytesIO()
    audio_segment.export(audio_data, format=audio_format)

    with open(file_name, 'wb') as f:
        f.write(audio_data.getvalue())

    print(f"[INFO] 음성 파일 저장 완료: {file_name}")