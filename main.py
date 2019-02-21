from telepot import Bot
from telepot.loop import MessageLoop
from time import sleep
from MapInfo import MapTracker
from UserSession import UserSession
from Command import Command

token = "654254537:AAGtYin0OQ5PRUCY9GdqOdIiU3ICBcKsL-s"
url = "https://api.telegram.org/bot/"

map_info = MapTracker()
bot = Bot(token)
active_sessions = {}


def main():
    print("start")

    MessageLoop(bot, handle).run_as_thread()
    cars_info = map_info.get_cars_info()
    print("found cars count =", len(cars_info))

    while True:
        sleep(1)


def send_message_response(chat_id, cars_in_range):
    bot.sendMessage(chat_id, '\n'.join(cars_in_range))


def handle(message):
    chat_id = message['chat']['id']
    print(message)
    if chat_id in active_sessions:
        chat_session = active_sessions[chat_id]
    else:
        chat_session = UserSession(map_info, chat_id, send_message_response)
        active_sessions[chat_id] = chat_session
    command = Command.create_command(message)
    process_command(chat_session, command)
        

def unknown_command_response():
    print('unknown_command_response')


def process_command(session, command):
    if command.type == Command.UNKNOWN:
        return
    elif command.type == Command.UNKNOWN:
        unknown_command_response()
    elif command.type == Command.START:
        session.start()
    elif command.type == Command.SET_LOCATION:
        session.set_last_location(command.properties['location'])
    else:
        print('this should never happen')


if __name__ == '__main__':
    main()
