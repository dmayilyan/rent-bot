# -*- coding: utf-8 -*-

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

import re
import pprint

devices = {(1, 'iPhone 7 128GB', 'Apple', 'Phones & Tablets'): 44.99,
           (2, 'iPhone 7 32GB', 'Apple', 'Phones & Tablets'): 39.99,
           (3, 'iPhone 7 Plus 128GB', 'Apple', 'Phones & Tablets'): 49.99,
           (4, 'Galaxy S8 64GB', 'Samsung', 'Phones & Tablets'): 44.99,
           (5, 'Galaxy S8+ 64GB', 'Samsung', 'Phones & Tablets'): 49.99,
           (6, 'Drone BEBOP', 'Parrot', 'Drones'): 49.99,
           (7, 'Drone BEBOP 2', 'Parrot', 'Drones'): 59.99,
           (8, 'Vive', 'HTC', 'Gaming & VR'): 59.99,
           (9, 'Virtual Reality Glasses Rift VR', 'Oculus',
            'Gaming & VR'): 59.99,
           (10, 'MacBook 12\" M-5Y31, 8GB RAM, 516GB', 'Apple',
            'Computing'): 59.99,
           (11, 'MacBook Air 11\" i7 2.2, 8GB RAM, 512GB', 'Apple',
            'Computing'): 64.99,
           (12, 'MacBook Air 13\" i5-5250U, 4GB RAM, 128GB', 'Apple',
            'Computing'): 69.99,
           (13, 'MacBook Pro 13\" i5-3210M, 4GB RAM, 500GB', 'Apple',
            'Computing'): 74.99,
           (14, 'Convertible Laptop Surface Book 512GB SSD ' +
            'Intel Core i7 16GB RAM dGPU', 'Microsoft', 'Computing'): 59.99,
           (15, 'Convertible Laptop YOGA 300-11IBR 80M1004KGE', 'Lenovo',
            'Computing'): 59.99,
           (16, 'Watch 38mm', 'Apple', 'Wearables'): 39.99,
           (17, 'Watch 42mm', 'Apple', 'Wearables'): 44.99,
           (18, 'Watch Ambit 3', 'Suunto', 'Wearables'): 39.99,
           (19, 'Watch V800', 'Polar', 'Wearables'): 39.99,
           (20, 'Watch WI503Q-1LDBR0001', 'Asus', 'Wearables'): 44.99,
           (21, 'Alexa Dot', 'Amazon', 'Smart Home'): 44.99,
           (22, 'Alexa Echo', 'Amazon', 'Smart Home'): 49.99,
           (23, 'Qbo Milk Master', 'Tchibo', 'Smart Home'): 29.99,
           (24, 'Robotic Vacuum Cleaner POWERbot VR20J9020UR/EG', 'Samsung',
            'Smart Home'): 39.99,
           (25, 'Robotic Vacuum Cleaner POWERbot VR20J9259U/EG', 'Samsung',
            'Smart Home'): 39.99}

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


class ActionRequest(Action):
    def name(self):
        return 'action_request'

    def _set_color(self, t):
        '''
        Making the output colored
        '''
        return '\033[0;31m' + t + '\033[0m'

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
                    print(self._set_color('Max rent period is set to 12.'))
                    return 12
        else:
            return 1

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

    def _get_brand(self, brand_req):
        '''
        Getting the brand
        '''
        pattern = r'(\w+) +(laptop|phone|comput|' \
                   'tablet|watch|quadrocopt)+[ers]*'
        regex = re.compile(pattern, flags=re.IGNORECASE)
        result = regex.findall(brand_req)
        # print(result)

        if result != []:
            return result[0]
        else:
            return []

    def _check_in_brands(self, brand_req):
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
                matches.append((item[1], devices[item]))
            # if is_brand and not is_category:
            #     matches.append(item[1])

        # print(matches)
        return matches

    def _check_in_devs(self, req):
        '''
        Chcking for the device in the list
        '''
        matches = []
        for item in devices.keys():
            if req.lower() in item[1].lower():
                matches.append((item[1], devices[item]))

        # print(matches)
        return matches


    # def run(self, request):
    def run(self, dispatcher, tracker, domain):
        matches = []
        time_period = 1
        calc_price = 1

        request = tracker.get_slot('device')
        time_req = tracker.get_slot('time')
        if time_req is not None:
            time_period = self._get_time_period(time_req)
        print(time_req)

        if request is not None:
            matches = self._check_in_devs(request)
            # print(matches)
            if matches == []:
                brand = self._get_brand(request)

                print(brand)
                brand = self._replace_syns(brand)
                matches = self._check_in_brands(brand)
            pprint.pprint(matches)

            if len(matches) > 1:
                dispatcher.utter_template("utter_which")
                return [SlotSet('device_list', matches if matches is not None else [])]
            elif len(matches) == 1:
                resp = "Selected the only one: {}\nMinimal rent is for a month."
                if time_period == 1:
                    resp += "\nFor how long do you want it?"
                calc_price = matches[0][1] * time_period
                dispatcher.utter_message(resp.format(matches))
                return [SlotSet('device', matches[0][0] if matches is not None else []),
                        SlotSet('one_price', matches[0][1] if matches is not None else []),
                        SlotSet('time', time_period if time_period is not None else 1),
                        SlotSet('price', calc_price if time_period is not None else 1)]
            else:
                dispatcher.utter_template("utter_not_found")

        one_price = tracker.get_slot('one_price')
        if one_price is not None:
            calc_price = one_price * time_period
        else:
            calc_price = 1

        return [SlotSet('time', time_period if time_period is not None else 1),
                SlotSet('price', calc_price if calc_price is not None else 1)]


if __name__ == '__main__':
    t0 = 'Apple laptop'
    t1 = 'Apple laptops'
    t2 = 'Convertible Laptop YOGA'
    t3 = 'Samsung phones'
    t4 = 'Lenovo computer'
    t5 = 'Parrot Quadrocopter'
    test = ActionRequest()
    # test.run(t0)
    # test.run(t1)
    test.run(t2)
    test.run(t3)
    test.run(t4)
    test.run(t5)
