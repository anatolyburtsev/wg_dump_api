import requests
import config
import json
import time
import logging
# import eventlet

# eventlet.monkey_patch()
logging.basicConfig(level=logging.CRITICAL)

class SourceNotAvailableException(Exception):
    pass


def dump_data_from_api(start_id, finish_id):
    req = "http://api.wotblitz.ru/wotb/account/info/?application_id={}&fields=nickname&account_id={}"
    filename = "nicknames_dump_" +str(start_id) + "_" + str(finish_id)
    f = open(filename, 'a')
    S = requests.session()
    for i in range((finish_id - start_id) // 100):
        if i % 10 == 0:
            logging.critical("current start_id: {}".format(str(start_id + i*100)))
        account_ids_list = []
        for account_id in range(start_id + i*100, start_id + (i+1)*100):
            account_ids_list.append(str(account_id))
        full_req = req.format(config.wargaming_id, ",".join(account_ids_list))

        # with eventlet.Timeout(30):
        response = S.get(full_req, timeout=30).json()

        try:
            nicknames = extract_nickname_from_response(response)
        except SourceNotAvailableException:
            logging.error("Caught SOURCE_NOT_AVAILABLE, start_id + i*100 = " + str(start_id + i*100))
            S.close()
            time.sleep(1)
            S = requests.session()
            response = S.get(full_req, timeout=30).json()
            nicknames = extract_nickname_from_response(response)

        for i in nicknames:
            f.write(i+"\n")
    f.close()


def extract_nickname_from_response(json_response):
    assert type(json_response) == dict
    time_to_sleep = 1
    time_to_sleep_limit = 60
    while json_response["status"] != "ok":
        if json_response["error"]["code"] == 504:
            raise SourceNotAvailableException
        print(json_response)
        time.sleep(time_to_sleep)
        if time_to_sleep < time_to_sleep_limit:
            time_to_sleep *= 2
    result = []
    for i in json_response["data"].values():
        if i:
            result.append(i["nickname"])
    return result


if __name__ == "__main__":
    t = time.time()
    dump_data_from_api(10561000, 100000000)
    print(str(time.time() - t) + " secs")

    # file = "test/accounts.json"
    # with open(file) as data_file:
    #     data = json.load(data_file)
    # print(extract_nickname_from_response(data))
