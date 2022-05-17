FROM python:3.10-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/carddav-to-yealink-remote
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "./main.py" ]
