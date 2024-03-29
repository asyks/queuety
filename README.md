# queuety

A little queue implementation with asynchronous publish and subscribe routines.

Based on Lynn Root's ([@econchick](https://github.com/econchick)) blog series
["asyncio: We Did It Wrong"](https://www.roguelynn.com/words/asyncio-we-did-it-wrong/).

## Usage

Building and running
```
> docker build -t queuety .
...
> docker run -i queuety python -m queuety
...
```

Running tests
```
> docker run -i queuety python -m unittest -v
...
OR
> docker run -i queuety python setup.py test
...
```

### IPC signal handling

queuty is configured to shutdown when it recieves a terminal (SIGTERM), interrupt (SIGINT), or hangup (SIGHUP).

e.g.
```
> pkill -TERM -f "python -m queuety"
...
```

