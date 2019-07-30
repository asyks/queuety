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

RUN mkdir -p /opt/queuety

WORKDIR /opt/queuety
COPY requirements.txt .
COPY setup.py .
COPY setup.cfg .

RUN python3 -m pip install --upgrade pip==19.0.1 \
    && virtualenv -p python3 /opt/queuety-virtualenv \
    && . /opt/queuety-virtualenv/bin/activate \
    && pip install -r requirements.txt

FROM ${BASE_IMAGE}

# Set locale to avoid https://bugs.python.org/issue19846
ENV PYTHONUNBUFFERED=1 \
    PATH="/opt/queuety-virtualenv/bin:${PATH}"

RUN apk add --no-cache \
    ca-certificates \
    python3

RUN mkdir -p /opt/queuety
COPY --from=builder /opt/queuety-virtualenv /opt/queuety-virtualenv

WORKDIR /opt/queuety
COPY requirements.txt .
COPY setup.py .
COPY setup.cfg .
COPY queuety queuety
COPY tests tests

CMD [ "python", "queuety/main.py"]
