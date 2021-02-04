import random

#大文字リスト
cap = list(range(65,91))
#print(cap)

#小文字リスト
low = list(range(97, 123))
#print(low)

#数字
num = list(range(48,58))
#print(num)

#全リスト
al = cap + low + (num * 2)
#print(al)


def GenNum():
    #桁数入力
    val = int(input("桁数入力\n"))

    #無作為選択
    ans = random.choices(al, k=val)
    #print(ans)

    #ASC2変換
    ansl = [chr(i) for i in ans]
    #print(ansl)

    #文字列変換
    anss = "".join(ansl)
    print(anss)

GenNum()