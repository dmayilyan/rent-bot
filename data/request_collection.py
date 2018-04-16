# -*- coding: utf-8 -*-
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.interpreter import RasaNLUInterpreter

import pprint




def run_weather_bot(serve_forever=True):
    interpreter = RasaNLUInterpreter('./models/default/request_bot')
    agent = Agent.load('./models/dialogue', interpreter=interpreter)

    if serve_forever:
        agent.handle_channel(ConsoleInputChannel())

return agent


def main():
    pprint.pprint(devices)


if __name__ == '__main__':
    main()