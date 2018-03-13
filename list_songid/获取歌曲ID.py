# encoding=utf8
import requests
from bs4 import BeautifulSoup

headers = {
    'Referer': 'http://music.163.com/',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

def main():


    play_url = 'http://music.163.com/playlist?id=%d' % _id
    s = requests.session()
    s = BeautifulSoup(s.get(play_url, headers=headers).content, 'lxml')

    load = s.find('ul', {'class': 'f-hide'})

    all_list = []
    songid_list = []
    for music in load.find_all('a'):
      songid = str(music['href'][9:])
      info = str(music.text) + " " + songid + "\n"
      all_list.append(info)

      songid = str(music['href'][9:])
      songid_list.append(songid + "\n")

    with open("list\%d.txt" % _id, 'w') as f:
       f.writelines(songid_list)
       print("歌单-歌曲ID文件写入完毕" ,end=' ')

    with open("songid.txt", 'a') as f:
      f.writelines(songid_list)
      print("总歌曲ID列表写入完毕")


if __name__ == "__main__":
    global _id
    _id = int(input("歌单ID: "))
    main()


    # with open('IntputListID.txt' , 'r') as f:
    #     f_list = f.readlines()
    #     print ("共 %d 个" %len(f_list))
    #
    # with open('count.txt' , 'r') as c:
    #     i = int(c.readlines()[-1])
    #
    # l = len(f_list)
    # t = 0
    # for t in range(i-1,l):
    #     _id = int(f_list[t][:-1])
    #     print (t+1,_id,end=' ')
    #     main()
    #     t = t+1
    #     with open('count.txt', 'a') as f:
    #         f.write("%d" % (t) +  '\n')
    # print("写入完毕")