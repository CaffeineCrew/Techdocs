FROM python:3.11

WORKDIR /Techdocs/TechdocsAPI/backend
RUN pip install --no-cache-dir --upgrade -r /Techdocs/TechdocsAPI/backend/requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]