FROM python:3.11

WORKDIR /TechdocsAPI/backend

COPY ./requirements.txt /TechdocsAPI/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /TechdocsAPI/requirements.txt

COPY . .

CMD ["cd", "TechdocsAPI","uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]