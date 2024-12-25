import os
from script import process_text_file

def read_text_file(file_path: str) -> tuple[str, str]:

    filename_with_ext = os.path.basename(file_path)  
    filename_no_ext, _ = os.path.splitext(filename_with_ext)
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return filename_no_ext, content


def main():
    # 사용 안내 문구
    print("========================================")
    print(" [INFO] speed: 0.25 ~ 4.0  // default: 1.0")
    print(" [INFO] voice: alloy, echo, fable, onyx, nova, shimmer // default: alloy")
    print("========================================\n")

    file_path = input("Enter the file path: ").strip()
    if not file_path:
        print("[ERROR] 파일 경로가 입력되지 않았습니다.")
        return

    voice = input("Enter voice (press Enter for default 'alloy'): ").strip()
    if not voice:
        voice = "alloy"

    speed_input = input("Enter speed (0.25 ~ 4.0, press Enter for default 1.0): ").strip()
    if not speed_input:
        speed = 1.0
    else:
        try:
            speed = float(speed_input)
            if not (0.25 <= speed <= 4.0):
                print("[ERROR] speed는 0.25 ~ 4.0 범위여야 합니다.")
                return
        except ValueError:
            print("[ERROR] speed는 숫자 형태여야 합니다.")
            return

    # 파일 읽기 (파일명, 파일 내용)
    file_name, txt = read_text_file(file_path)

    process_text_file(
        text_content=txt,
        mode="local",
        voiceId=voice,
        speed=speed,
        filename=file_name
    )

# 터미널에서 직접 실행될 때만 main() 호출
if __name__ == "__main__":
    main()