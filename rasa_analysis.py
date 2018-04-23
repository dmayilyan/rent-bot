# -*- coding: utf-8 -*-

from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter

from rasa_core.interpreter import RasaNLUInterpreter

# import pprint


request_info = {}
devices = {(1, 'iPhone 7 128GB', 'Apple', 'Phones & Tablets'): 44.99,
           (2, 'iPhone 7 32GB', 'Apple', 'Phones & Tablets'): 39.99,
           (3, 'iPhone 7 Plus 128GB', 'Apple', 'Phones & Tablets'): 49.99,
           (4, 'Galaxy S8 64GB', 'Samsung', 'Phones & Tablets'): 44.99,
           (5, 'Galaxy S8+ 64GB', 'Samsung', 'Phones & Tablets'): 49.99,
           (6, 'Drone BEBOP', 'Parrot', 'Drones'): 49.99,
           (7, 'Drone BEBOP 2', 'Parrot', 'Drones'): 59.99,
           (8, 'Vive', 'HTC', 'Gaming & VR'): 59.99,
           (9, 'Virtual Reality Glasses Rift VR', 'Oculus', 'Gaming & VR'): 59.99,
           (10, 'MacBook 12\" M-5Y31, 8GB RAM, 516GB', 'Apple', 'Computing'): 59.99,
           (11, 'MacBook Air 11\" i7 2.2, 8GB RAM, 512GB', 'Apple', 'Computing'): 64.99,
           (12, 'MacBook Air 13\" i5-5250U, 4GB RAM, 128GB', 'Apple', 'Computing'): 69.99,
           (13, 'MacBook Pro 13\" i5-3210M, 4GB RAM, 500GB', 'Apple', 'Computing'): 74.99,
           (14, 'Convertible Laptop Surface Book 512GB SSD Intel Core i7 16GB RAM dGPU', 'Microsoft', 'Computing'): 59.99,
           (15, 'Convertible Laptop YOGA 300-11IBR 80M1004KGE', 'Lenovo', 'Computing'): 59.99,
           (16, 'Watch 38mm', 'Apple', 'Wearables'): 39.99,
           (17, 'Watch 42mm', 'Apple', 'Wearables'): 44.99,
           (18, 'Watch Ambit 3', 'Suunto', 'Wearables'): 39.99,
           (19, 'Watch V800', 'Polar', 'Wearables'): 39.99,
           (20, 'Watch WI503Q-1LDBR0001', 'Asus', 'Wearables'): 44.99,
           (21, 'Alexa Dot', 'Amazon', 'Smart Home'): 44.99,
           (22, 'Alexa Echo', 'Amazon', 'Smart Home'): 49.99,
           (23, 'Qbo Milk Master', 'Tchibo', 'Smart Home'): 29.99,
           (24, 'Robotic Vacuum Cleaner POWERbot VR20J9020UR/EG', 'Samsung', 'Smart Home'): 39.99,
           (25, 'Robotic Vacuum Cleaner POWERbot VR20J9259U/EG', 'Samsung', 'Smart Home'): '39.99'}


def train(data, config, model_dir):
    train_data = load_data(data)
    trainer = Trainer(RasaNLUConfig(config))
    trainer.train(train_data)
    model_directory = trainer.persist(model_dir,
                                      fixed_model_name='request_bot')


# def run():
#     interpreter = Interpreter.load('models/default/request_bot',
#                                    RasaNLUConfig('config_spacy.json'))
#     pprint.pprint(interpreter.parse(u'Hello, I would like to rent a Samsung phone. Do you have any? Cheers, Marx Frankenstein'))

#     sample_list = [u'Hello, I would to rent a Galaxy S8 64GB. I would like to have it for a month. How much will it cost? Best regards,Dezdemona',
#                    u'Hello. My name is Otello and I would like to rent a Alexa Echo for several days. Thanks in advance,Ben',
#                    u'Hello, I would like to rent a Watch Ambit 3. Regards, Jacob']

# # 'one of your' case
#     for text in sample_list:
#         result = interpreter.parse(text)
#         print(type(result['entities']))
#     # pprint.pprint(result)
#         print(extract_info(result['entities']))
#         # compile_answer()


# def extract_info(result):
#     for item in result:
#         if item['entity'] == 'name':
#             request_info['name'] = item['value'].title()
#         if item['entity'] == 'device':
#             request_info['device'] = item['value'].title().replace('.', '')

#     return request_info


# def compile_answer():
#     print('Dear {name},\n\nYou can take your {device} at Grossstrasse 42.'.format(name=request_info['name'], device=request_info['device']))


if __name__ == '__main__':
    train('./data/data.json', './config_spacy.json', './models/')
    # run()
    
