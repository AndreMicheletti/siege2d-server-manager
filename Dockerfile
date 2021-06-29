FROM python:3

WORKDIR /app/

COPY ./manager/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./manager ./

EXPOSE 5000

CMD [ "python", "app.py" ]
