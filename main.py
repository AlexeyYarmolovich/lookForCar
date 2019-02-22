from telepot.aio import Bot
from time import sleep
from MapInfo import MapTracker
from UserSession import UserSession
from Command import Command
import asyncio
from telepot.aio.loop import MessageLoop


token = "654254537:AAGtYin0OQ5PRUCY9GdqOdIiU3ICBcKsL-s"
url = "https://api.telegram.org/bot/"

map_info = MapTracker()
bot = Bot(token)
active_sessions = {}


async def main():
    print("start")

    cars_info = map_info.get_cars_info()
    print("found cars count =", len(cars_info))

    loop = asyncio.get_event_loop()
    print('1')
    loop.create_task(MessageLoop(bot).run_forever())
    print('2')
    loop.run_forever()
    print('3')
    #MessageLoop(bot, handle).run_as_thread()


async def send_message_response(chat_id, cars_in_range):

    await bot.sendMessage(chat_id, cars_in_range) #'\n'.join(cars_in_range))


async def on_chat_message(message):
    chat_id = message['chat']['id']
    print(message)
    if chat_id in active_sessions:
        chat_session = active_sessions[chat_id]
    else:
        chat_session = UserSession(map_info, chat_id, send_message_response)
        active_sessions[chat_id] = chat_session
    command = Command.create_command(message)
    await process_command(chat_session, command)
        

def unknown_command_response():
    print('unknown_command_response')


async def process_command(session, command):
    print('received command: ', command)

    if command.type == Command.UNKNOWN:
        unknown_command_response()
    elif command.type == Command.START:
        await session.start()
    elif command.type == Command.SET_LOCATION:
        await session.set_last_location(command.properties['location'])
    else:
        print('this should never happen, cant handle command: ', command)


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    print('1')
    loop.create_task(MessageLoop(bot, {'chat': on_chat_message}).run_forever())
    print('2')
    loop.run_forever()

    asyncio.run(main())
