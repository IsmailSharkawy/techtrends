FROM --platform=linux/x86_64  python:3.8
LABEL maintainer="Ismail Sharkawy"

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python init_db.py
EXPOSE 3111
ENV HOST '0.0.0.0'
# command to run on container start

CMD [ "python", "app.py" ]
