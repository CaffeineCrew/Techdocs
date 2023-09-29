FROM python:3.11

WORKDIR /TechdocsAPI

# COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# COPY . .

# WORKDIR /TechdocsAPI

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]