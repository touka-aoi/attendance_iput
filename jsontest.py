import json

a = open("UserData.json")
b = json.load(a)
c = b["UserData"]["usrname"]
d = b["UserData"]["password"]
print(c)
print(d)

b["UserData"]["password"] = "pypy"
print(b["UserData"]["password"])
a = open("UserData.json" ,"w")
json.dump(b, a)