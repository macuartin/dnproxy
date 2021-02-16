FROM python:3.8
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
EXPOSE 53/tcp
EXPOSE 53/udp
CMD [ "python", "./dnproxy.py" ] 