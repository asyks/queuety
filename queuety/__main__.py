#!/usr/bin/env python

import asyncio

from . import log, main

if __name__ == "__main__":
    log.setup()
    asyncio.run(main.main())
