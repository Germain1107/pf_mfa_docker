FROM python:3.11.1-slim-bullseye

WORKDIR /app
COPY . .
ENV FLASK_DEBUG=0
ENV FLASK_APP=app
RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
