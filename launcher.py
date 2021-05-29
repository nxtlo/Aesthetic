from core import Amaya
from core.ext import PgPool
from setuptools import Extension, setup
from Cython.Build import cythonize
from time import sleep
import sys
import asyncio
import os.path
import logging

log = logging.getLogger(__name__)
run = asyncio.get_event_loop().run_until_complete
pool = run(PgPool().__ainit__())

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def main() -> None:
    build_c()
    bot = Amaya()
    bot.pool = pool
    bot.run()

def rebuild() -> None:
    log.exception("Cython extension found! rebuilding now.")
    if os.path.isdir('cxcode'):
        os.remove('cxcode/proto.c')
        sleep(1)
        setup(
            name='amaya', 
            ext_modules=cythonize(
                Extension(
                    'cxcode.proto', 
                    sources=
                        [
                    'cxcode/proto.pyx', 'cxcode/include/instance.c'
                    ]
                )
            )
        )
        log.info("Rebulit Cython extension.")

def build_c() -> None:
    if not os.path.isfile('cxcode/proto.c'):
        setup(
            name='amaya', 
            ext_modules=cythonize(
                Extension(
                    'cxcode.proto', 
                    sources=
                        [
                    'cxcode/proto.pyx', 'cxcode/include/instance.c'
                    ]
                )
            )
        )
        log.info("Completed building Cython extension!")
    rebuild()

if __name__ == "__main__":
    main()