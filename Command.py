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
        else:
            return Command.create_unknown_command(message)

    @classmethod
    def create_command_from_text(cls, text):
        text = text.lower()
        command = Command()
        if text == Command.INITIAL:
            command.type = Command.INITIAL
        elif text.find(Command.START) == 0:
            start_option = text.replace(Command.START, '')
            try:
                search_range = float(start_option)
                command.properties['range'] = search_range
            except:
                pass
            command.type = Command.START
        elif text == Command.STOP:
            command.type = Command.STOP
        else:
            command.type = Command.UNKNOWN
            command.properties['text'] = text
        return command

    @classmethod
    def create_command_from_location(cls, location):
        command = Command()
        command.type = Command.SET_LOCATION
        command.properties['location'] = (location['longitude'], location['latitude'])
        return command

    @classmethod
    def create_unknown_command(cls, message):
        command = Command()
        command.type = Command.UNKNOWN
        command.properties['message'] = message
        return command