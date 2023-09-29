FROM python:3.11

WORKDIR /TechdocsAPI/backend

COPY /TechdocsAPI/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r /TechdocsAPI/requirements.txt

COPY . .

CMD ["uvicorn", "/TechdocsAPI/app:app", "--host", "0.0.0.0", "--port", "7860"]