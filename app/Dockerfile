FROM python:3.12.3

WORKDIR /code

COPY ./requirements.txt ./requirements.txt

RUN --mount=type=cache,mode=0755,target=/root/.cache \
  pip install -r requirements.txt

COPY ./ ./app

CMD ["python", "app/main.py"]
