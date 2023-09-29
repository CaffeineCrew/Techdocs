FROM python:3.11

WORKDIR /TechdocsAPI/backend
RUN pip install --no-cache-dir --upgrade -r /TechdocsAPI/backend/requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]