import requests
from telepot import Bot
from telepot.loop import MessageLoop
from time import sleep
from MapInfo import MapTracker
from UserSession import UserSession

token = "654254537:AAGtYin0OQ5PRUCY9GdqOdIiU3ICBcKsL-s"
url = "https://api.telegram.org/bot/"

map_info = MapTracker()
bot = Bot(token)
current_chat_id = None

def main():
    print("start")

    MessageLoop(bot, handle).run_as_thread()

    cars_info = map_info.get_cars_info()
    print("found cars count =", len(cars_info))


    while True:
        sleep(1)


current_chat_id = 0

def process_cars(chat_id, cars_in_range):
    bot.sendMessage(chat_id, 'prepare to cars')
    bot.sendMessage(chat_id, '\n'.join(cars_in_range))

current_user_id = None

def handle(message):
    chat_id = message['chat']['id']
    user_id = message['from']['id']
    if 'location' in message:
        current_user_id = user_id
        session = UserSession(map_info, chat_id, message['location'])
        session.start(process_cars)
    else:
       print('no location found in message', message)

if __name__ == '__main__':
    main()
