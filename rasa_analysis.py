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
    pprint.pprint(interpreter.parse(u'Hello, I would like to rent a Samsung phone.')[:2])
    pprint.pprint(interpreter.parse(u'Hello, I would like to rent a Samsung Galaxy S7. Regards, Dave')[:2])


if __name__ == '__main__':
    # train('./data/data.json', './config_spacy.json', './models/')
    run()
