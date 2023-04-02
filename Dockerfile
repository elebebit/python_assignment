FROM python:3.8

WORKDIR /app
COPY . /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "financial/manage.py"]