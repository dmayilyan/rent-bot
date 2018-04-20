# from __future__ import absolute_import
# from __future__ import division
# from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

import re

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
           (25, 'Robotic Vacuum Cleaner POWERbot VR20J9259U/EG', 'Samsung', 'Smart Home'): 39.99}

time_period = {('1', 'one', 'a'): 1,
               ('2', 'two'): 2,
               ('3', 'three'): 3,
               ('4', 'four'): 4,
               ('5', 'five'): 5,
               ('6', 'six'): 6,
               ('7', 'seven'): 7,
               ('8', 'eight'): 8,
               ('9', 'nine'): 9,
               ('10', 'ten'): 10,
               ('11', 'eleven'): 11,
               ('12', 'twelve'): 12}

# class ActionUnclear(Action):
#     def name(self):
#         return 'action_unclear'


class ActionRequest(Action):
    def name(self):
        return 'action_request'

    def check_in_dict(self, req):
        '''
        Chcking for the device in the list
        '''
        matches = []
        for item in devices.keys():
            if req.lower() in item[1].lower():
                matches.append((item[1], devices[item]))

        # print(matches)
        return matches

    def get_time_period(self, text):
        '''
        Finding requested time period
        '''
        month_pat = r'([0-9a-zA-Z]+) month.'
        regex = re.compile(month_pat)
        result = regex.findall(text)
        if result != []:
            for k_tup in time_period.keys():
                if result[0] in k_tup:
                    return time_period[k_tup]
        else:
            return 1

    # def run(self, text):
    def run(self, dispatcher, tracker, domain):
        matches = []
        try:
            request = tracker.get_slot('device')
            matches = self.check_in_dict(request)
        except AttributeError:
            print('Device not found.')
        # Checking for how long is the rent request
        try:
            time_req = tracker.get_slot('time')
            time_period = self.get_time_period(time_req)
        except TypeError:
            time_period = 1
            print('Time period not mentioned.')
        # matches = self.check_in_dict(text)
        # time_period = self.get_time_period(text)

        if len(matches) == 0:
            response = '\033[0;34mWe do not have what you requested. Do you want any other device?\033[0m'
            # print(response)
        elif len(matches) == 1:
            calc_price = matches[0][1] * time_period
            response  = '\033[0;34mWe do have {req} for {price} overall.\033[0m'.format(req=matches[0][0].title(), price=calc_price)
            # print(response)
        elif len(matches) > 1:
            response = '\033[0;34mWe have several devices matching your request.\nWhich one do you want?\n{}\033[0m'.format(matches)
            # print(response)

        dispatcher.utter_message(response)
        return [SlotSet('device', request if request is not None else [])]


if __name__ == '__main__':
    text = 'two months'
    test = ActionRequest()
    test.run(text)
