FROM resin/raspberry-pi-python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT ["/sbin/tini", "-g",  "--"]
STOPSIGNAL SIGTERM
CMD [ "python", "./exmaples/led_rotate.py" ]
