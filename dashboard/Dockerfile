FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit","run","dashboard/app.py","--server.address=0.0.0.0","--server.port=8501"]