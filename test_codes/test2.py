import json
from cryptography.fernet import Fernet
import glob

if len(glob.glob("thing/key.key")) == 1:
    with open("thing/key.key", "rb") as file:
        key = file.read()
fernet = Fernet(key)
a = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
b = [
    [1, 2, 4],
    [4, 4, 4],
    [22, 23, 24],
]
thing = {"uno": a, "dos": b}

with open("thing/dict.txt", "w") as file:
    json.dump(thing, file)

with open("thing/dict.txt", "r") as file:
    thing2 = json.load(file)

# print(thing2["uno"][0][0])
# thing3 = thing2["dos"]
# print(thing3)
# print(type(thing3))
"""
print(thing)
print(thing2)
a[0][0] = "a"
print(thing)
print(thing2)
"""
# ec = fernet.encrypt()
ec = json.dumps(thing, indent=2).encode("utf-8")
# print(ec)
ec = fernet.encrypt(ec)
# print(ec)
ec = fernet.decrypt(ec)
# print(ec)
ec = json.loads(ec)
print(ec)
print(ec["uno"])