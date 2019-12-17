import json
import csv
from settings import BASE_DIR
import os

label_to_tag = {
    "组织结构": "ZZ",
    "地点": "D",
    "时间": "S",
    "职位": "ZW",
    "人物": "RW",
    "活动": "HD",
    "机构": "JG"
}

def load_json_datas(file_path):
    datas = open(file_path, 'r').readlines()
    datas = [json.loads(line) for line in datas]
    return datas

def write_csv_data(file_path, data):
    headers = ['text_a', 'label']
    with open(file_path, 'w')  as f:
        f_csv = csv.writer(f,delimiter="\t")
        f_csv.writerow(headers)
        f_csv.writerows(data)

def covert_to_list(datas):
    result = []
    for data in datas:
        labels = data['labels']
        text = data['text']
        length = len(text)
        print(length)
        label_tags = ["O"] * length
        for label in labels:
            tag = label_to_tag[label[2]]
            label_tags[label[0]] = "B-" + tag
            # label_tags[label[0]: label[1]] = "I-" + tag
            for i in range(label[0]+1, label[1]):
                label_tags[i] = "I-"+tag
        text = "\002".join(list(text))
        label_tags = "\002".join(label_tags)
        result.append([text, label_tags])
    return result

if __name__ == "__main__":
    origin_path = os.path.join(BASE_DIR, 'resources', 'datasets', 'huodong', 'datas')
    json_datas = load_json_datas(origin_path)
    train = json_datas[:400]
    train = covert_to_list(train)
    dev = json_datas[400:450]
    dev = covert_to_list(dev)
    test = json_datas[450:]
    test = covert_to_list(test)
    train_path = os.path.join(BASE_DIR, 'resources' , 'datasets', 'huodong', 'train.txt')
    dev_path = os.path.join(BASE_DIR, 'resources', 'datasets', 'huodong', 'dev.txt')
    test_path = os.path.join(BASE_DIR, 'resources', 'datasets', 'huodong', 'test.txt')
    write_csv_data(train_path, train)
    write_csv_data(dev_path, dev)
    write_csv_data(test_path, test)
    pass