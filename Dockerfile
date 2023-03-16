FROM python:3.11-slim

COPY ./ ./

# install dependencies
RUN apt-get update && apt-get install -y \
    build-essential

RUN pip install 'pipenv==2018.11.26' && \
    pipenv lock -r > /requirements.txt && \
    pip install -r /requirements.txt --no-cache-dir

EXPOSE 5000

CMD [ "gunicorn", "--bind=0.0.0.0:5000", "src.app:app" ]