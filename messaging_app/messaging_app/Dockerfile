FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r messaging_app/requirements.txt

EXPOSE 8000

# manage.py doesn't know "-p"
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
