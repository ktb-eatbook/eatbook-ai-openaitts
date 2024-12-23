from script import process_text_file

def read_text_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content

txt = read_text_file("dong_ep1.txt")
processed_txt = process_text_file(txt)