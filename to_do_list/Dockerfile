FROM python:3.12-slim
RUN groupadd -r groupdjango &&  \
    useradd -r -g groupdjango userdj

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

RUN pip install --upgrade pip
WORKDIR /app/www/to_do_list
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

USER userdj

EXPOSE 8000
# CMD ["python", "to_do_list/manage.py", "runserver"]
