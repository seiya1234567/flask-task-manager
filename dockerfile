FROM python:3.11.5

WORKDIR /usr/src/app
ENV FLASK_APP=app

COPY app/requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# アプリ本体をコピー（appディレクトリの中身を全てコピー）
COPY app ./app