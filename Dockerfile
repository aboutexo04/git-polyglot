# 가벼운 파이썬 이미지를 사용
FROM python:3.9-slim

# 작업 폴더 설정
WORKDIR /app

# 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 코드 복사
COPY main.py .

# 실행 명령어
ENTRYPOINT ["python", "/app/main.py"]
