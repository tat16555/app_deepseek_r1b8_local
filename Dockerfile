FROM python:3.10-slim

WORKDIR /app

# ติดตั้ง system dependencies
RUN apt-get update && apt-get install -y build-essential git

# คัดลอก requirements
COPY requirements.txt /app/requirements.txt
COPY langchain-gemma-ollama-chainlit-main/requirements.txt /app/langchain-req.txt

# รวม requirements
RUN cat /app/langchain-req.txt >> /app/requirements.txt

# อัปเกรด pip และติดตั้ง dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# คัดลอกโค้ดทั้งหมด
COPY . .

EXPOSE 8000

CMD ["chainlit", "run", "langchain-gemma-ollama-chainlit-main/langchain_gemma_ollama.py"]
