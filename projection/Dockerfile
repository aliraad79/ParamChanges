FROM python:3.12-slim

# Iranian PyPI mirror — pypi.org is unreachable from inside containers in Iran.
# Override with --build-arg PIP_INDEX_URL=... if you have a working proxy.
ARG PIP_INDEX_URL=https://mirror-pypi.runflare.com/simple/
ENV PIP_INDEX_URL=${PIP_INDEX_URL} \
    PIP_TRUSTED_HOST=mirror-pypi.runflare.com

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
