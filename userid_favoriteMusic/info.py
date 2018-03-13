# _*_ coding: utf-8 _*_
from base64 import b64encode
import requests
import pandas as pd
import sys
import time

from Crypto.Cipher import AES

# _id = 355969309


def get_data():
    # global _id
    # _id = input("请输入用户id: ")
    # _id = "402955002"

    # for line in open("29498138.txt"):
    #     _id = line
    # print (_id)

    info = '{"uid":"%s","type":"-1","limit":"1000","offset":"0","total":"true","csrf_token":""}' % _id
    return info


def aes_encrypt(d, g):
    iv = "0102030405060708"
    cipher = AES.new(g, AES.MODE_CBC, iv)
    pad = 16 - len(d) % 16
    d = d + pad * chr(pad)
    aes_result = cipher.encrypt(d)
    return b64encode(aes_result)


def get_params(d):
    g = "0CoJUm6Qyw8W8jud"
    a = "F" * 16
    aes_result = aes_encrypt(d, g)
    params = aes_encrypt(aes_result.decode(), a)
    return params


def get_encSeckey():
    enc_sec_key = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return enc_sec_key


def post_data(params):
    data = {'params': params, "encSecKey": get_encSeckey()}
    return data


def to_excel(json_music):
    # 所有时间
    df = pd.DataFrame(columns=["歌名", "歌名id", "歌手", "歌手id", "百分百"])
    try:
        json_music['allData']
    except Exception as f:
        f = open('不可见.txt', 'a')
        f.write(_id + '\n')
        f.close()
        print("此用户不可见")
        return
    for data, count in zip(json_music['allData'], range(len(json_music['allData']))):
        score = data['score']
        music_name = data['song']['name']
        music_id = data['song']['id']
        ar = data['song']['ar']
        singer = []
        singer_id = []
        for a in ar:
            singer.append(a['name'])
            singer_id.append(str(a['id']))
        singer = "/".join(singer)
        singer_id = "/".join(singer_id)
        # print([music_name, music_id, singer, singer_id, score])
        df.loc[count] = [music_name, music_id, singer, singer_id, score]
    if df.count()['歌名'] == 0:
        print("没有结果结束运行！")
        # sys.exit(0)
        return 0
    df.to_excel("所有时间\所有时间_%s.xlsx" % _id, index=None)
    df.drop(df.index, inplace=True)

    # 最近一周
    for data, count in zip(json_music['weekData'], range(len(json_music['weekData']))):
        score = data['score']
        music_name = data['song']['name']
        music_id = data['song']['id']
        ar = data['song']['ar']
        singer = []
        singer_id = []
        for a in ar:
            singer.append(a['name'])
            singer_id.append(str(a['id']))
        singer = "/".join(singer)
        singer_id = "/".join(singer_id)
        df.loc[count] = [music_name, music_id, singer, singer_id, score]
    df.to_excel("最近一周\最近一周_%s.xlsx" % _id, index=None)
    df.drop(df.index, inplace=True)
    print("成功获取！")

def main():

    data = post_data(get_params(get_data()))
    url = "http://music.163.com/weapi/v1/play/record?csrf_token="
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Referer": "http://music.163.com/user/songs/rank?id=402955002"
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        print("响应错误!")
    to_excel(response.json())


if __name__ == "__main__":
    start_time = time.time()  # 开始时间
    # 单个ID
    global _id
    #_id = "378185543"
    _id  = int(input ("ID："))
    main()




    # 断点采集========================================
    # inputtxt = 'userID.txt'
    # global _id
    # f = open('%s'%inputtxt , 'r')
    # f_list = f.readlines()
    # print ("共 %d 个" %len(f_list))
    # f.close
    #
    # c = open('count.txt' , 'r')
    # i = int(c.readlines()[-1])
    # c.close
    #
    # l = len(f_list)
    # t = 0
    # for t in range(i-1,l):
    #     _id = f_list[t][:-1]
    #     print (t+1,_id,end=' ')
    #     main()
    #     # time.sleep(0.8)
    #     t = t+1
    #     f = open('count.txt', 'a')
    #     f.write("%d" % (t) +  '\n')
    #     f.close()


    end_time = time.time()  # 结束时间
    print("程序耗时%f秒." % (end_time - start_time))