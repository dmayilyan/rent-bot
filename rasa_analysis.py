# -*- coding: utf-8 -*-

from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter

import pprint

def train(data, config, model_dir):
    train_data = load_data(data)
    trainer = Trainer(RasaNLUConfig(config))
    trainer.train(train_data)
    model_directory = trainer.persist(model_dir,
                                      fixed_model_name='request_bot')


def run():
    interpreter = Interpreter.load('models/default/request_bot',
                                   RasaNLUConfig('config_spacy.json'))
    pprint.pprint(interpreter.parse(u'Hello, I would like to rent a Samsung phone. Do you have any? Cheers, Marx Frankenstein'))
    pprint.pprint(interpreter.parse(u'Hello, I want to rent a Galaxy S7. Regards, Dave'))


if __name__ == '__main__':
    train('./data/data1.json', './config_spacy.json', './models/')
    run()
