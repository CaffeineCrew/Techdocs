FROM python:3.11

WORKDIR /

COPY ./requirements.txt /TechdocsAPI/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /TechdocsAPI/requirements.txt

COPY . .

WORKDIR /TechdocsAPI

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]