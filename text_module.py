import re
from typing import List, Dict, Any

def read_paragraphs_from_text(text_content: str) -> List[str]:
    """
    txt 파일을 읽어와 문단단위로 list 형태 저장
    """
    paragraphs = text_content.strip().split('\n\n')
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    return paragraphs

def split_paragraph_into_sentences(paragraph: str) -> List[str]:
    """
    한 문단을 입력받아 각각의 문장으로 분할
    """
    sentences = re.split(r'(?<=[.?!])\s+', paragraph)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences
