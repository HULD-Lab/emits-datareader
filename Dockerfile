FROM python:3.8-slim
COPY code /code
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
