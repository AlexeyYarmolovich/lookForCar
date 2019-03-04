import asyncio
from time import sleep
import time


a = 'd2ca393f-1c68-4e5c-afaf-c969e2de'

shortA = a[-4:]
print(shortA)

class Simple:
    def __init__(self, value):
        self.value = value

    def __hash__(self):
        hashValue = hash(self.value)
        print('hash for {} is {}', self.value, hashValue)
        return hashValue

    def __eq__(self, other):
        print('eq for {} and {}', self, other)
        return self.value == other.value


known = set(['1','2','3'])
dismissed = set(['2','3','4'])
known.difference_update(dismissed)
print(known)

sleep(10000)

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