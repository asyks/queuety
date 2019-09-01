#!/usr/bin/env python

import asyncio

from . import log, entry


log.setup()
asyncio.run(entry.simulate_ingress())
asyncio.run(entry.simulate_egress())
