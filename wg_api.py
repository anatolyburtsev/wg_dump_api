import requests
import config
import json
import time


def dump_data_from_api(start_id, finish_id):
    req = "http://api.wotblitz.ru/wotb/account/info/?application_id={}&fields=nickname&account_id={}"
    filename = "nicknames_dump_" +str(start_id) + "_" + str(finish_id)
    f = open(filename, 'w')
    S = requests.session()

    for i in range((finish_id - start_id) // 100):
        account_ids_list = []
        for account_id in range(start_id + i*100, start_id + (i+1)*100):
            account_ids_list.append(str(account_id))
        full_req = req.format(config.wargaming_id, ",".join(account_ids_list))

        response = S.get(full_req).json()
        nicknames = extract_nickname_from_response(response)
        for i in nicknames:
            f.write(i+"\n")

    f.close()


def extract_nickname_from_response(json_response):
    assert type(json_response) == dict
    while json_response["status"] != "ok":
        print(json_response)
        time.sleep(1)
    result = []
    for i in json_response["data"].values():
        if i:
            result.append(i["nickname"])
    return result




if __name__ == "__main__":
    t = time.time()
    dump_data_from_api(0, 100000000)
    print(str(time.time() - t) + " secs")

    # file = "test/accounts.json"
    # with open(file) as data_file:
    #     data = json.load(data_file)
    # print(extract_nickname_from_response(data))
