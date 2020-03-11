FROM python:3.6

LABEL maintainer="vinh-ngu@hotmail.com"

WORKDIR /app
ADD . .
RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
