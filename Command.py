class Command:
    INITIAL = "/start"
    START = "start"
    STOP = "stop"
    SET_LOCATION = "update_location"
    UNKNOWN = "unknown"

    properties = {}

    @classmethod
    def create_command(cls, message):
        if 'text' in message:
            return Command.create_command_from_text(message['text'])
        elif 'location' in message:
            return Command.create_command_from_location(message['location'])

    @classmethod
    def create_command_from_text(cls, text):
        command = Command()
        if text == Command.INITIAL:
            command.type = Command.INITIAL
        elif text == Command.START:
            command.type = Command.START
        elif text == Command.STOP:
            command.type = Command.STOP
        else:
            command.type = Command.UNKNOWN
        return command

    @classmethod
    def create_command_from_location(cls, location):
        command = Command()
        command.type = Command.SET_LOCATION
        command.properties['location'] = (location['longitude'], location['latitude'])
        return command