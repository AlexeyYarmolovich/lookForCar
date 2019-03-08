from telepot.aio import Bot
import sys
import telepot
from MapInfo import MapTracker
from UserSession import UserSession
from Command import Command
import asyncio
from telepot.aio.loop import MessageLoop

print('that is the first print in the app')
map_info = MapTracker()
bot = Bot(sys.argv[1])
active_sessions = {}


async def send_message_response(chat_id, cars_in_range):
    try:
        await bot.sendMessage(chat_id, cars_in_range) #'\n'.join(cars_in_range))
    except telepot.exception.BotWasBlockedError as error:
        active_sessions[chat_id].stop()
        del active_sessions[chat_id]
        print('stopped session because user blocked ', chat_id)

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
    print('received command: ', command.__dict__)

    if command.type == Command.UNKNOWN:
        await send_message_response(session.chat_id, 'CHTO ETO ZA SLOVO')
        unknown_command_response()
    elif command.type == Command.INITIAL:
        await send_message_response(session.chat_id, 'hello my friend')
    elif command.type == Command.START:
        await session.start(command.properties.get('range'))
    elif command.type == Command.SET_LOCATION:
        await session.set_last_location(command.properties['location'])
    elif command.type == Command.STOP:
        await send_message_response(session.chat_id, 'ok say no more')
        session.stop()
        del active_sessions[session.chat_id]

    else:
        print('this should never happen, cant handle command: ', command.__dict__)


if __name__ == '__main__':
    print('message loop created')
    loop = asyncio.get_event_loop()
    loop.create_task(MessageLoop(bot, {'chat': on_chat_message}).run_forever())
    loop.run_forever()