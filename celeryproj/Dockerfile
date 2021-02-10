FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /celeryproj
COPY requirements.txt /celeryproj/
RUN pip install -r requirements.txt
COPY . /celeryproj/
COPY manage.py /celeryproj/
CMD ["python", "manage.py", "runserver", "0:8080"]