import requests
from telepot import Bot
from telepot.loop import MessageLoop
from time import sleep
from MapInfo import MapTracker
from UserSession import UserSession

token = "654254537:AAEYgcQt0F0G9UeOMhL77vIo6E5iibnO4cY"
url = "https://api.telegram.org/bot/"


def get_updates_json(urlBase, lastProcessedUpdate):
    print("get_updates_json start, last was ", str(lastProcessedUpdate))
    url = urlBase + 'getUpdates?timeout=5&offset=' + str(lastProcessedUpdate + 1)
    response = requests.get(url)
    print("get_updates_json finish")
    return response.json()


def last_update(data):
    results = data['result']

    if len(results) == 0:
        return None
    total_updates = len(results) - 1
    return results[total_updates]


def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id

def check_distance(userLocation):
    cars_info = requests.get('http://service.drivetime.by/api/cars').json()['cars']
    print(cars_info)

def send_mess(chat, text):
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response

map_info = MapTracker()

def main():
    print("start")

    bot = Bot(token)
    MessageLoop(bot, handle).run_as_thread()

    cars_info = map_info.get_cars_info()
    print("found cars count =", len(cars_info))


    while True:
        sleep(1)


def handle(message):
    user_id = message['from']['id']
    user_location = 'location' in message
    if user_location == True:
        session = UserSession(map_info, user_id, user_location)
        session.start()
    else:
       print('no location found in message', message)

if __name__ == '__main__':
    main()
