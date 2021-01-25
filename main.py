#モジュル読み込み
from bs4 import BeautifulSoup
import requests
import pprint
import itertools


#ユーザー情報
usrname = "TK200014"
password =  "Nkhry-7120q"

#スクレイピング用 HTML 出席ワード
at = "出欠を送信する"

python_attendance = "https://lms.iput.ac.jp/course/view.php?id=338#section-2"

#session create
url = "https://lms.iput.ac.jp/login/index.php"
session = requests.session()
response = session.get(url)
bs = BeautifulSoup(response.text, "html.parser")

#cookie and token
auth = bs.find(attrs={"name" : "logintoken"}).get("value")
cookie = response.cookies

#login info
info = {
    "token" : auth,
    "username" : usrname,
    "password" : password
}

res = session.post(url, data=info, cookies = cookie)
#print(res.text)

bs = BeautifulSoup(res.text, "html.parser")
#print(bs)
selected = bs.select("h3 > a[class=coursecard-coursename]")
mp = dict()
for sel in selected:
    mp[str(sel.string)] = str(sel.get("href"))
    #print(sel)
    #print(sel.string)
    #print(sel.get("href"))

print(mp)

test = "Pythonプログラミング（2020年度下期授業：B組）"

#授業のURLを取得する
def IputAttend(url):
    ses = session.get(url)
    bs = BeautifulSoup(ses.text, "html.parser")
    selectes = bs.select("ul > li .attendance" )

    #print(selectes[0])
    att = selectes[0].get("data-href")
    #print(att)
    return att

#出席ページに遷移
def transAttend(url):
    ses = session.get(url)
    bs = BeautifulSoup(ses.text, "html.parser")
    selected = bs.find_all("tr", class_="lastrow")
    return selected


a2 = IputAttend(mp[test])
b = transAttend(a2)
print(b) #strip前の確認

#リストから出席ページの入力URLを返す
def getAttend(lists):
    lis = list() #分解用リスト
    for val in lists:
        lis.append(val.select("tr > td > a")) #これでとれる
    print(lis) #debug
    lis = [x for x in lis if x != []] #空リスト削除
    print(lis)
    for a in lis:
        for b in a:
            print(b.string)
            if (b.string == at):
                print(b.get("href"))
                return b.get("href")

cc = getAttend(b)

def IputComfirm(lists):
    lis = list()  # 分解用リスト
    for val in lists:
        lis.append(val.select("a"))  # これでとれる
    print(lis)
    for a in lis:
        for b in a:
            if (b.string == "すべて"):
                return b.get("href")

print(IputComfirm(b))

passwd = "NURB"
info = {
    "submitbutton" : "変更を保存する",
    "studentpassword" : passwd
}
#res = session.post(cc, data=info, cookies = cookie)
