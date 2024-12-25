# eatbook-ai-openaitts

## Table of Contents

[ 📝 Overview](#📝-overview)  
[ 📁 Project Structure](#📁-project-structure)  
[ 🚀 Getting Started](#🚀-getting-started)  
[ 💡 Motivation](#💡-motivation)

## 📝 Overview
이 프로젝트는 텍스트 파일을 입력으로 받아 음성 파일과 메타데이터를 생성하는 기능을 제공합니다. 

### Main Purpose
- 텍스트를 음성으로 변환하여 오디오 파일을 생성합니다.
- 텍스트 파일의 내용을 기반으로 음성을 생성하여, 청취할 수 있도록 합니다.
- 서비스화에 적합한 메타데이터를 생성합니다.
- aws s3에 생성된 데이터를 저장합니다.

### Key Features
- 텍스트 파일을 문단 단위로 읽어 음성 파일로 변환
- 생성된 음성에 대한 메타데이터 자동 생성
- AWS S3에 음성 파일과 메타데이터 저장

### Core Technology Stack
- FastAPI
- Python
- AWS S3
- OpenAI TTS

## 🚀 Getting Started

### Development Environment
- mac os 15.0.1
- python 3.11

### Installation

```bash
# Clone the repository
git clone https://github.com/wwjin-j/eatbook-ai-openaitts/.git
cd eatbook-ai-openaitts

# Install required packages
pip install -r requirements.txt

# Configure environments
# 환경 설정 파일(.env 등)을 설정합니다.
```

### Usage
- local test
```bash
# test for local
python test_local.py
# Enter file path, voice, speed
```
- run server
```bash
uvicorn server:app --host 127.0.0.1 --port 8000 --reload
```

## 💡 Motivation
- 특히, 독서가 어려운 사용자들이나 바쁜 일상 속에서 콘텐츠를 소비하고자 하는 사용자들에게 도움을 주기 위해 개발되었습니다.
- e-book 서비스 연동을 위한 정밀한 메타데이터 생성을 지원합니다.



