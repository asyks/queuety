ARG BASE_IMAGE=alpine:3.10

FROM ${BASE_IMAGE} as builder

RUN apk add --no-cache \
    build-base \
    gcc \
    binutils \
    ca-certificates \
    python3 \
    python3-dev \
    py-pip \
    py3-virtualenv

RUN mkdir -p /opt/py-hello

WORKDIR /opt/py-hello
COPY requirements.txt .
COPY setup.py .
COPY setup.cfg .

RUN python3 -m pip install --upgrade pip==19.0.1 \
    && virtualenv -p python3 /opt/py-hello-virtualenv \
    && . /opt/py-hello-virtualenv/bin/activate \
    && pip install -r requirements.txt

FROM ${BASE_IMAGE}

# Set locale to avoid https://bugs.python.org/issue19846
ENV PYTHONUNBUFFERED=1 \
    PATH="/opt/py-hello-virtualenv/bin:${PATH}"

RUN apk add --no-cache \
    ca-certificates \
    python3

RUN mkdir -p /opt/py-hello
COPY --from=builder /opt/py-hello-virtualenv /opt/py-hello-virtualenv

WORKDIR /opt/py-hello
COPY requirements.txt .
COPY setup.py .
COPY setup.cfg .
COPY py_hello py_hello
COPY tests tests

CMD [ "python", "py_hello/main.py"]
