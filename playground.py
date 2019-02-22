import asyncio
from time import sleep
import time


async def small_loop(number):
    print('statred small loop #', number)
    await asyncio.sleep(1.5)
    print('finished small loop #', number)


async def main_loop():
    print('statred big loop')
    counter = 0
    while True:
        counter+=1
        print('big loop tick ', counter)
        await small_loop(counter)
        await asyncio.sleep(1)

asyncio.run(main_loop())