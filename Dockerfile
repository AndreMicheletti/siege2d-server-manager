FROM python:3

WORKDIR /app/

RUN pip install --upgrade pip

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./

ENV FLASK_APP="main"
ENV FLASK_ENV="production"

EXPOSE 5000

CMD [ "flask", "run" ]
