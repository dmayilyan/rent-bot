# -*- coding: utf-8 -*-

import os
import re

available_devices = {'iPhone 7 128GB',
                     'iPhone 7 32GB',
                     'iPhone 7 Plus 128GB',
                     'Galaxy S8 64GB',
                     'Galaxy S8+ 64GB',
                     'Drone BEBOP',
                     'Drone BEBOP 2',
                     'Vive',
                     'Virtual Reality Glasses Rift VR',
                     'MacBook 12\" M-5Y31, 8GB RAM, 516GB',
                     'MacBook Air 11\" i7 2.2, 8GB RAM, 512GB',
                     'MacBook Air 13\" i5-5250U, 4GB RAM, 128GB',
                     'MacBook Pro 13\" i5-3210M, 4GB RAM, 500GB',
                     'Convertible Laptop Surface Book 512GB SSD Intel Core i7 16GB RAM dGPU',
                     'Convertible Laptop YOGA 300-11IBR 80M1004KGE',
                     'Watch 38mm',
                     'Watch 42mm',
                     'Watch Ambit 3',
                     'Watch V800',
                     'Watch WI503Q-1LDBR0001',
                     'Alexa Dot',
                     'Alexa Echo',
                     'Qbo Milk Master',
                     'Robotic Vacuum Cleaner POWERbot VR20J9020UR/EG',
                     'Robotic Vacuum Cleaner POWERbot VR20J9259U/EG'}

# Need a setter getter approach :/
# For now let it be so
user_info = {'user_name': 'user', 'rent_device': 'device'}


def get_files():
    '''
    Get the messages list
    '''
    m_path = 'messages'
    files = os.listdir(m_path)
    files = [os.path.join(m_path, f) for f in files]
    return files

def read_file(file):
    '''
    Rad one file and analyse.
    '''
    global user_name
    global rent_device


    with open(file, 'r') as f:
        content = f.read()
        # print(content)


        name_pattern = [r'regards,*\n(\w+)',
                        r'cheers,*\n(\w+)',
                        r'My name is (\w+)']
        # false_device = [r'(\w+) is broken']
        device_pattern = [r'rent a* ([A-Za-z0-9 ]+)\.',
                          r'borrow a* ([A-Za-z0-9 ]+)\.',
                          r'one of your* ([A-Za-z0-9 ]+)\.']

        patlist = {'user_name': name_pattern, 'rent_device': device_pattern}

        for pns in patlist.items():
            # print(pns[1])
            found_pattern = False
            for pattern in pns[1]:
                if found_pattern:
                    continue
                regex = re.compile(pattern)
                for result in regex.findall(content):
                    if result == '':
                        print('Pattern not found')
                    else:
                        found_pattern = True
                        print('Found %s: %s.  Skipping other patterns...\n' % (pns[0], result))
                        user_info[pns[0]] = result


def make_greeeting():
    '''
    Make the greting.
    '''
    user_info['user_name'] = ' ' + user_info['user_name']
    return 'Hello{un},\n\n'.format(un=user_info['user_name'])


def make_content():
    ans = '''Your {device} can be picked up at Super Strasse 43.\n\n'''.format(device=user_info['rent_device'])
    return ans


def make_end():
    '''
    Make signature
    '''
    ans = 'Best regards,\nHans Mueller\nGrover team'
    return ans


def compile_answer():
    '''
    Compiling an answer.
    '''
    answer = ''
    answer += make_greeeting()
    answer += make_content()
    answer += make_end()
    return answer


def main():
    fl = get_files()
    for file in fl:
        read_file(file)
        print(compile_answer())
        print('------------------------')


if __name__ == '__main__':
    main()
