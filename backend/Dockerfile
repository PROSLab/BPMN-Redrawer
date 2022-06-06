FROM python:3.8

RUN mkdir /app
WORKDIR /app

RUN apt-get install -y apt-transport-https
RUN echo 'deb https://notesalexp.org/tesseract-ocr-dev/bullseye/ bullseye main' >> /etc/apt/sources.list
RUN wget -O - https://notesalexp.org/debian/alexp_key.asc | apt-key add -
RUN apt-get update
RUN apt-get install -y tesseract-ocr

COPY requirements.txt ./
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/facebookresearch/detectron2.git@v0.6

COPY bpmn_redrawer_backend bpmn_redrawer_backend/

CMD gunicorn --bind 0.0.0.0:5000 --pythonpath bpmn_redrawer_backend wsgi:app

EXPOSE 5000
