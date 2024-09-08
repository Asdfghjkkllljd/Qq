import os
import requests
import certifi
import webbrowser
import hashlib
import ctypes
import json
import time
import mysql.connector
from colorama import init, Fore, Style

ctypes.windll.kernel32.SetConsoleTitleA(b'dev - https://t.me/flaskin_perehodnik')

init(autoreset=True)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_message(message, delay):
    for char in message:
        print(Fore.YELLOW + char, end='', flush=True)
        time.sleep(delay)
    print(Style.RESET_ALL)

def save_key_to_config(key):
    config_dir = 'C://Program Files (x86)/flaskin tools/'
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    config_path = os.path.join(config_dir, 'config.json')
    config_data = {'key': key}
    with open(config_path, 'w') as config_file:
        json.dump(config_data, config_file)

def get_hwid():
    hwid = hashlib.sha256(os.popen('wmic csproduct get uuid').read().encode()).hexdigest()
    return hwid

def check_key_in_database(user_key, hwid):
    try:
        connection = mysql.connector.connect(
            host='185.244.173.136',
            user='hwid_usr',
            password='MJGKh15McYLl7Q64',
            database='hwid',
            use_pure=True
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM `keys` WHERE `key` = %s", (user_key,))
        result = cursor.fetchone()
        
        if result:
            if result['hwid'] is None:
                cursor.execute("UPDATE `keys` SET `hwid` = %s WHERE `key` = %s", (hwid, user_key))
                connection.commit()
                save_key_to_config(user_key)
                cursor.close()
                connection.close()
                return True
            elif result['hwid'] == hwid:
                cursor.close()
                connection.close()
                return True
            else:
                clear_console()
                print(Fore.RED + 'Этот ключ уже используется на другом устройстве.')
        else:
            clear_console()
            print(Fore.RED + 'Такого ключа не существует.')
        
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
    return False

def process_response(response_data):
    if 'Status' in response_data and response_data['Status'] == 'Error':
        print(Fore.RED + 'Ошибка, свяжитесь с разработчиком для получения новой версии.')
        return

    num_of_results = response_data.get('NumOfResults', 0)
    if 'List' in response_data:
        for key, value in response_data['List'].items():
            if key == 'No results found':
                print(Fore.RED + 'Данные по вашему запросу не найдены.\n')
                return
            print(Fore.CYAN + f'Источник {Fore.WHITE}{key}{Fore.CYAN}:\n')
            if 'Data' in value and value['Data']:
                for data_entry in value['Data']:
                    for data_key, data_value in data_entry.items():
                        print(f'  {data_key}: {data_value}')
                print()
            else:
                print(Fore.RED + 'Данные по вашему запросу не найдены.\n')
    else:
        print(Fore.YELLOW + 'Данные по вашему запросу не найдены.\n')

    num_of_database = response_data.get('NumOfDatabase', 0)
    search_time = response_data.get('search time', 0)
    free_requests_left = response_data.get('free_requests_left', 0)

    print(Fore.GREEN + f'\n\n\nКоличество результатов: {num_of_results}')
    print(Fore.GREEN + f'Время поиска: {search_time} секунд')

def main():
    hwid = get_hwid()
    config_path = 'C://Program Files (x86)/flaskin tools/config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            config_data = json.load(config_file)
            user_key = config_data.get('key', '')
            if user_key:
                hwid = get_hwid()
                if check_key_in_database(user_key, hwid):
                    pass
                else:
                    clear_console()
                    animate_message('Введите ключ: ', 0.05)
                    print()
                    user_key = input()
            else:
                clear_console()
                animate_message('Введите ключ: ', 0.05)
                print()
                user_key = input()
    else:
        clear_console()
        animate_message('Введите ключ: ', 0.05)
        print()
        user_key = input()

    if check_key_in_database(user_key, hwid):
        webbrowser.open('https://t.me/+lY0XWVGfssAwMzYy')

        while True:
            clear_console()
            animate_message('Введите запрос: ', 0.05)
            print()
            request = input()
            clear_console()
            animate_message('Поиск запущен..', 0.05)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Referer': 'https://apimsk.xyz/dskadkjasldjks/dasjdsadasdsadsa.php',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'DNT': '1'
            }
            proxies = {
                'http': 'http://66.45.246.194:8888',
                'http': 'http://103.54.59.65:80',
                'http': 'http://64.201.163.133:80'
            }
            url = requests.get('https://apimsk.xyz/dskadkjasldjks/dasjdsadasdsadsa.php?&password=v2', verify=certifi.where(), proxies=proxies, headers=headers, timeout=5)
            tokenresp = url.text

            data = {
                'token': tokenresp,
                'request': request,
                'limit': 100,
                'lang': 'ru'
            }

            response = requests.post('https://server.leakosint.com/', json=data)
            try:
                clear_console()
                response_data = response.json()
                process_response(response_data)
            except json.JSONDecodeError:
                print(Fore.RED + 'Ошибка декодирования ответа. Проверьте правильность запроса и попробуйте снова.')

            animate_message('\n\n\n\nНажмите Enter, чтобы сделать новый запрос или CTRL+C, чтобы выйти..', 0.05)
            input()

main()