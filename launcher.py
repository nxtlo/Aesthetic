from core import Amaya
import asyncio
from core.ext import PgPool
from setuptools import Extension, setup
from Cython.Build import cythonize
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


def build_c() -> None:
    if not os.path.isfile('cxcode/proto.c'):
        setup(
            name='amaya', 
            ext_modules=cythonize(
                Extension(
                    'cxcode', 
                    sources=
                        [
                    'core/cxcode/proto.pyx', 'core/cxcode/include/instance.c'
                    ]
                )
            )
        )
        log.info("Completed building Cython extension!")
    log.error("Cython extension already exists!")

def main() -> None:
    build_c()
    bot = Amaya()
    bot.pool = pool
    bot.run()


if __name__ == "__main__":
    main()