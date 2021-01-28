#モジュル読み込み
from bs4 import BeautifulSoup
import requests
import pprint
import itertools
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import webbrowser
import json

# print("ユーザー名を入力\n")
# usrname = input()
# print("パスワードを入力\n")
# password = input()


#ユーザー情報
usrname = ""
password =  ""


#Jsonとかやりたいな...
with open("UserData.json") as fr:
    js = json.load(fr)
    if (js["UserData"]["usrname"] == None):
        with open("UserData.json", "w") as fw:
            usr = input("ユーザー名を入力してください")
            usrname = usr
            js["UserData"]["usrname"] = usr
            json.dump(js, fw)
    else:
        usrname = js["UserData"]["usrname"]
    if (js["UserData"]["password"] == None):
        with open("UserData.json", "w") as fw:
            pss = input("パスワードを入力してください")
            password = pss
            js["UserData"]["password"] = pss
            json.dump(js, fw)
    else:
        password = js["UserData"]["password"]

# print(usrname)
# print(password)

#授業名
lesson_name = " "

#GUI用変数
header = ["授業名", "URL"]

#スクレイピング用 HTML 出席ワード
at = "出欠を送信する"

#セッション作成
url = "https://lms.iput.ac.jp/login/index.php"
session = requests.session()
response = session.get(url)
bs = BeautifulSoup(response.text, "html.parser")

#クッキーとトークン作成
auth = bs.find(attrs={"name" : "logintoken"}).get("value")
cookie = response.cookies

#ログイン情報
info = {
    "token" : auth,
    "username" : usrname,
    "password" : password
}

#ログイン実行
res = session.post(url, data=info, cookies = cookie)

#ログイン後情報取得
bs = BeautifulSoup(res.text, "html.parser")

test = session.get("https://lms.iput.ac.jp/mod/assign/view.php?id=8071&action=editsubmission")
testbs = BeautifulSoup(test.text, "html.parser")
print(testbs.find("input", {"type" : "hidden"})["value"])

#授業名全取得
selected = bs.select("h3 > a[class=coursecard-coursename]")
mp = dict()
for sel in selected:
    mp[str(sel.string)] = str(sel.get("href"))

valmp = dict()
for (val, i) in zip(mp, range(len(mp))):
    print(f"{i+1} : {val}")
    valmp[i+1] = val

x = int(input("授業番号入力"))
lesson_name = valmp[x]


#授業のURLを取得する
def IputAttend(url):
    ses = session.get(url)
    bs = BeautifulSoup(ses.text, "html.parser")
    selectes = bs.select("ul > li .attendance" )
    att = selectes[0].get("data-href")
    return att

#出席ページに遷移
def transAttend(url):
    ses = session.get(url)
    bs = BeautifulSoup(ses.text, "html.parser")
    selected = bs.find_all("tr", class_="lastrow")
    return selected

#リストから出席ページの入力URLを返す
def getAttend(lists):
    lis = list() #分解用リスト
    for val in lists:
        lis.append(val.select("tr > td > a")) #これでとれる
    #print(lis) #debug
    lis = [x for x in lis if x != []] #空リスト削除
    #print(lis)
    for a in lis:
        for b in a:
            #print(b.string)
            if (b.string == at):
                #print(b.get("href"))
                return b.get("href")


def IputComfirm(lists):
    lis = list()  # 分解用リスト
    for val in lists:
        lis.append(val.select("a"))  # これでとれる
    #print(lis)
    for a in lis:
        for b in a:
            if (b.string == "すべて"):
                return b.get("href")

#授業リスト取得
a2 = IputAttend(mp[lesson_name])

#主席ページ取得
b = transAttend(a2)
#print(b) #strip前の確認
cc = getAttend(b)
#print(cc) #s出席URL取得

#確認用URL
dd = IputComfirm(b)
#print(dd)

if cc:
    webbrowser.open(cc)
else:
    print("URLを見つけられませんでした\n確認用ページに飛びます\n")
    dd = IputComfirm(b)
    webbrowser.open(dd)


"""
全力で未完成
"""

"""
passwd = "7931"
info = {

    "_qf_mod_attendance_student_attendance_form" : 1,
    "mform_isexpanded_id_session" : 1,
    "submitbutton" : "変更を保存する",
    "studentpassword" : passwd
}
#res = session.post(cc, data=info, cookies = cookie)
"""


lists = list()
for i in mp:
    lists.append((i, mp[i]))
#print(lists)

#GUI設計
class TableModel(QAbstractTableModel):
    def rowCount(self, parent):
        return len(lists)
    def columnCount(self, parent):
        return 2
    def data(self, index, role):
        if role != Qt.DisplayRole:
            return QVariant()
        return lists[index.row()][index.column()]
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return QVariant()
        return header[section]

# app = QApplication([])
# app.setApplicationName("IPUT ATTENDANCE SUPPORT")
# model = TableModel()
# view = QTableView()
# view.setModel(model)
# view.show()
# app.exec_()