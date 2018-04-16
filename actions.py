# from __future__ import absolute_import
# from __future__ import division
# from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet



class ActionRequest(Action):
    def __init__(self):
        self.devices = {(1, 'iPhone 7 128GB', 'Apple', 'Phones & Tablets'): '44.99',
                        (2, 'iPhone 7 32GB', 'Apple', 'Phones & Tablets'): '39.99',
                        (3, 'iPhone 7 Plus 128GB', 'Apple', 'Phones & Tablets'): '49.99',
                        (4, 'Galaxy S8 64GB', 'Samsung', 'Phones & Tablets'): '44.99',
                        (5, 'Galaxy S8+ 64GB', 'Samsung', 'Phones & Tablets'): '49.99',
                        (6, 'Drone BEBOP', 'Parrot', 'Drones'): '49.99',
                        (7, 'Drone BEBOP 2', 'Parrot', 'Drones'): '59.99',
                        (8, 'Vive', 'HTC', 'Gaming & VR'): '59.99',
                        (9, 'Virtual Reality Glasses Rift VR', 'Oculus', 'Gaming & VR'): '59.99',
                        (10, 'MacBook 12\" M-5Y31, 8GB RAM, 516GB', 'Apple', 'Computing'): '59.99',
                        (11, 'MacBook Air 11\" i7 2.2, 8GB RAM, 512GB', 'Apple', 'Computing'): '64.99',
                        (12, 'MacBook Air 13\" i5-5250U, 4GB RAM, 128GB', 'Apple', 'Computing'): '69.99',
                        (13, 'MacBook Pro 13\" i5-3210M, 4GB RAM, 500GB', 'Apple', 'Computing'): '74.99',
                        (14, 'Convertible Laptop Surface Book 512GB SSD Intel Core i7 16GB RAM dGPU', 'Microsoft', 'Computing'): '59.99',
                        (15, 'Convertible Laptop YOGA 300-11IBR 80M1004KGE', 'Lenovo', 'Computing'): '59.99',
                        (16, 'Watch 38mm', 'Apple', 'Wearables'): '39.99',
                        (17, 'Watch 42mm', 'Apple', 'Wearables'): '44.99',
                        (18, 'Watch Ambit 3', 'Suunto', 'Wearables'): '39.99',
                        (19, 'Watch V800', 'Polar', 'Wearables'): '39.99',
                        (20, 'Watch WI503Q-1LDBR0001', 'Asus', 'Wearables'): '44.99',
                        (21, 'Alexa Dot', 'Amazon', 'Smart Home'): '44.99',
                        (22, 'Alexa Echo', 'Amazon', 'Smart Home'): '49.99',
                        (23, 'Qbo Milk Master', 'Tchibo', 'Smart Home'): '29.99',
                        (24, 'Robotic Vacuum Cleaner POWERbot VR20J9020UR/EG', 'Samsung', 'Smart Home'): '39.99',
                        (25, 'Robotic Vacuum Cleaner POWERbot VR20J9259U/EG', 'Samsung', 'Smart Home'): '39.99'}

    def name(self):
        return 'action_request'

    def check_in_dict(self, req):
        matches = []
        for item in self.devices.keys():
            if req.lower() in item[1].lower():
                matches.append(item[1])

        # print(matches)
        return matches

    def _print_matches(self, matches):
        # [print('%d) %s' % (i,t)) for (i,t) in enumerate(matches)]
        return [(i, t) for (i, t) in enumerate(matches)]

    def run(self, dispatcher, tracker, domain):
    # def run(self, text):
        request = tracker.get_slot('device')
        matches = self.check_in_dict(request)
        # self.check_in_dict(text)
        self._print_matches(matches)

        if len(matches) == 0:
            response = 'We do not have {req} you requested. Do you want any other device?'.format(req=request)
        elif len(matches) == 1:
            response  = 'We do have {req} you requested.'.format(req=request)
            # print(response)
        elif len(matches) > 1:
            response = 'We have several devices matching your request. Which one do you want?\n{}'.format(self._print_matches(matches))
            # print(response)

        dispatcher.utter_message(response)
        return [SlotSet('device', request)]

    # def run(self, dispatcher, tracker, domain):
    #     from apixu.client import ApixuClient
    #     api_key = '...'  # your apixu key
    #     client = ApixuClient(api_key)

    #     loc = tracker.get_slot('location')
    #     current = client.getCurrentWeather(q=loc)

    #     country = current['location']['country']
    #     city = current['location']['name']
    #     condition = current['current']['condition']['text']
    #     temperature_c = current['current']['temp_c']
    #     humidity = current['current']['humidity']
    #     wind_mph = current['current']['wind_mph']

    #     response = """It is currently {} in {} at the moment. The temperature is {} degrees, the humidity is {}% and the wind speed is {} mph.""".format(condition, city, temperature_c, humidity, wind_mph)

    #     dispatcher.utter_message(response)
    #     return [SlotSet('location', loc)]


# if __name__ == '__main__':
#     text = 'iPhone 7'
#     test = ActionRequest()
#     test.run(text)