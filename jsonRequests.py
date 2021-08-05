from time import time,sleep

import requests
import json

HEADERS = {'User-Agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
PARAMS = dict(product_id='')
NEW_POST_NUM = 0


def notification_message():
    r = requests.get("https://timebank.by/index.php?route=api%2Fproduct", headers=HEADERS, params=PARAMS).json()
    fixing_json = str(r).strip("'<>() ").replace('\'', '\"').replace("False", "false").replace("None", "null")
    product_id = json.loads(fixing_json)
    json_length = len(product_id["products"])
    new_post_num = 0
    with open("product_id_new.txt", "r") as file_r:
        read_data = file_r.read()
    with open("product_id_new.txt", "a") as file_w:
        for k in range(0, len(product_id["products"])):
            if product_id["products"][k]["product_id"] not in read_data:
                new_post_num = k
                file_w.write(f"\n{product_id['products'][k]['product_id']}")
                break
    post_name = product_id["products"][new_post_num]["name"]
    post_description = product_id["products"][new_post_num]["description"]
    post_city = product_id["products"][new_post_num]["gorod"]
    # post_type = product_id["products"][new_post_num]["cat"]["parent"]
    post_connection_time = product_id["products"][new_post_num]["connecttime"]
    post_link = product_id["products"][new_post_num]["href"]
    message = f"<b>Тема объявления:</b> {post_name} \n<b>Описание:</b> {post_description} \n" \
              f"<b>Город:</b> {post_city} \n<b>Время для связи:</b> {post_connection_time}\n<b>Ссылка на пост:</b> {post_link}"
    return message


def post_checking():
    new_post_checker = False
    r = requests.get("https://timebank.by/index.php?route=api%2Fproduct", headers=HEADERS, params=PARAMS).json()
    fixing_json = str(r).strip("'<>() ").replace('\'', '\"').replace("False", "false").replace("None", "null")
    product_id = json.loads(fixing_json)
    print(len(product_id["products"]))
    with open("product_id.txt", "r") as file_read1:
        read_data = file_read1.read()
        for k in range(0, len(product_id["products"])):
            if product_id["products"][k]["product_id"] not in read_data:
                new_post_checker = True
                break
            else:
                new_post_checker = False
    with open("product_id.txt", "a") as file_write1:
        for k in range(0, len(product_id["products"])):
            if product_id["products"][k]["product_id"] not in read_data:
                file_write1.write(f"\n{product_id['products'][k]['product_id']}")
                break
    return new_post_checker


if __name__ == '__main__':
    r = requests.get("https://timebank.by/index.php?route=api%2Fproduct", headers=HEADERS, params=PARAMS).json()
    fixing_json = str(r).strip("'<>() ").replace('\'', '\"').replace("False", "false").replace("None", "null")
    product_id = json.loads(fixing_json)
    print()
    # print(product_id["products"][0]["cat"]["parent"])
    post_checking()
