FROM python:3.11

COPY ./TechdocsAPI .

WORKDIR /

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]