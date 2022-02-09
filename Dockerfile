FROM python:3

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

ENV PATH=$PATH:/root/.poetry/bin
ENV PYTHONUNBUFFERED=1

COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]

WORKDIR /app
