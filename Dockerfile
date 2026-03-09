FROM python:3.12-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ .
EXPOSE 53/tcp
EXPOSE 53/udp
CMD [ "python", "./dnproxy.py" ]
