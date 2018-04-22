# -*- coding: utf-8 -*-

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


class ActionBrandRequest(Action):
    def name(self):
        return 'action_brand_request'

    def _replace_syns(self, matches):
        syns = {'laptop': 'comput',
                'phon': 'phone',
                'fon': 'phone',
                'cleaner': 'home',
                'watch': 'wearable',
                'quadrocopt': 'drone'}

        for item in matches:
            item = item.lower()
            if item in syns.keys():
                matches = (matches[0], item.replace(item, syns[item]))

        return matches

    def _check_in_dict(self, brand_req):
        '''
        Checking for brand devices
        '''
        matches = []
        br = brand_req[0].lower()
        cat = brand_req[1].lower()
        for item in devices.keys():
            is_brand = False
            is_category = False

            is_brand = br in item[2].lower()
            is_category = cat in item[3].lower()
            # make_response()
            # print(is_brand, is_category)
            if is_brand and is_category:
                matches.append(item[1])
            # if is_brand and not is_category:
            #     matches.append(item[1])

        # print(matches)
        return matches

    def _get_brand(self, brand_req):
        '''
        Getting the brand
        '''
        print(brand_req)
        pattern = r'(\w+) +(laptop|phone|comput|' \
                   'tablet|watch|quadrocopt)+[ers]*'
        regex = re.compile(pattern, flags=re.IGNORECASE)
        result = regex.findall(brand_req)

        return result[0]

    # def run(self, text):
    def run(self, dispatcher, tracker, domain):
        try:
            brand_req = tracker.get_slot('brand')
            brand = self._get_brand(brand_req)
            # brand = self._get_brand(text)
            brand = self._replace_syns(brand)
            matches = self._check_in_dict(brand)
        except AttributeError:
            print('Brand not found.')

        response = '\033[0;31mFor the {brand} we have ' \
                   'these devices:\n{bl}\033[0m'.format(brand=brand[0].title(),
                                                        bl=matches)
        # print(response)

        dispatcher.utter_message(response)
        return [SlotSet('brand', brand if brand is not None else [])]


class ActionRequest(Action):
    def name(self):
        return 'action_request'

    def _check_in_dict(self, req):
        '''
        Chcking for the device in the list
        '''
        matches = []
        for item in devices.keys():
            if req.lower() in item[1].lower():
                matches.append((item[1], devices[item]))

        # print(matches)
        return matches

    def _get_time_period(self, text):
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
        calc_price = 1
        matches = []
        try:
            request = tracker.get_slot('device')
            matches = self._check_in_dict(request)
        except AttributeError:
            print('Device not found.')
        # Checking for how long is the rent request
        try:
            time_req = tracker.get_slot('time')
            time_period = self._get_time_period(time_req)
        except TypeError:
            time_period = 1
            print('Time period not mentioned.')
        # matches = self._check_in_dict(text)
        # time_period = self._get_time_period(text)

        if len(matches) == 0:
            response = '\033[0;31mWe do not have what you requested. ' \
                       'Do you want any other device?\033[0m'
            # print(response)
        elif len(matches) == 1:
            calc_price = matches[0][1] * time_period
            response = '\033[0;31mWe do have {req} for {price} overall.' \
                       '\033[0m'.format(req=matches[0][0].title(),
                                        price=calc_price)
            # print(response)
        elif len(matches) > 1:
            response = '\033[0;31mWe have several devices ' \
                       'matching your request.\nWhich one ' \
                       'do you want?\n{}\033[0m'.format(matches)
            # print(response)

        dispatcher.utter_message(response)
        return [SlotSet('device', request if request is not None else ''),
                SlotSet('price', calc_price if calc_price is not None else -1)]


if __name__ == '__main__':
    # text = 'two months'
    # test = ActionRequest()
    # test.run(text)
    text = 'Apple laptop'
    t1 = 'Apple laptops'
    t2 = 'Samsung phone'
    t3 = 'Samsung phones'
    t4 = 'Lenovo computer'
    t5 = 'Parrot Quadrocopter'
    test = ActionBrandRequest()
    test.run(text)
    test.run(t1)
    test.run(t2)
    test.run(t3)
    test.run(t4)
    test.run(t5)
    # test._check_in_dict(text)
    # test._check_in_dict(t1)
    # test._check_in_dict(t2)

    # brand = test._get_brand(t2)
    # test._check_in_dict(t4)
