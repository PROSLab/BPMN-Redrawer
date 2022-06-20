FROM python:3.8

ARG BACKEND_MODE=production
ARG BACKEND_URL=http://localhost:5000
ARG BACKEND_PORT=5000

ENV BACKEND_MODE=${BACKEND_MODE}
ENV BACKEND_URL=${BACKEND_URL}
ENV BACKEND_PORT=${BACKEND_PORT}

RUN mkdir /app
WORKDIR /app
RUN mkdir /backend
RUN mkdir /frontend
COPY backend/bpmn_redrawer_backend backend/bpmn_redrawer_backend/
COPY frontend frontend
RUN [ -f backend/bpmn_redrawer_backend/detectron_model/final_model.pth ] && echo "Object Detection model found" || { echo "Object Detection model not found!"; wget -O backend/bpmn_redrawer_backend/detectron_model/final_model.pth https://huggingface.co/PROSLab/BPMN-Redrawer-Models/resolve/main/final_model.pth; }
RUN [ -f backend/bpmn_redrawer_backend/detectron_model/kp_final_model.pth ] && echo "KeyPoint Prediction model found" || { echo "KeyPoint Prediction model not found!"; wget -O backend/bpmn_redrawer_backend/detectron_model/kp_final_model.pth https://huggingface.co/PROSLab/BPMN-Redrawer-Models/resolve/main/kp_final_model.pth; }

RUN apt-get install -y apt-transport-https
RUN echo 'deb https://notesalexp.org/tesseract-ocr-dev/bullseye/ bullseye main' >> /etc/apt/sources.list
RUN wget -O - https://notesalexp.org/debian/alexp_key.asc | apt-key add -
RUN apt-get update
RUN apt-get install -y tesseract-ocr
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get update
RUN apt-get install -y nodejs
RUN npm install -g yarn

COPY backend/requirements.txt backend/requirements.txt
RUN pip install -U pip
RUN pip install -r backend/requirements.txt
RUN pip install git+https://github.com/facebookresearch/detectron2.git@v0.6

CMD rm -rf backend/bpmn_redrawer_backend/static && cd frontend && yarn && yarn build && cd .. && mv frontend/dist/spa backend/bpmn_redrawer_backend/static && cd backend && uvicorn --host 0.0.0.0 --port ${BACKEND_PORT} --factory bpmn_redrawer_backend.app:create_app

EXPOSE ${BACKEND_PORT}
