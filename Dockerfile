FROM alpine:3.18

RUN adduser -D convecter

WORKDIR /home/convecter

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app convecter
COPY migrations migrations
COPY app.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R convecter:convecter ./
USER convecter

EXPOSE 80
ENTRYPOINT ["./boot.sh"]
