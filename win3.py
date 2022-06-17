import pprint
import os
import glob
from cryptography.fernet import Fernet
import json

path = "src/data/test_save_1/"
with open("src/data/test_save_1/thing.thingy", "rb") as file:
    key = file.read()
fernet = Fernet(key)

with open(path + "save.dat", "rb") as file:
    encrypt = file.read()
decrypt = fernet.decrypt(encrypt)
dict = json.loads(decrypt)
pprint.pprint(dict)
#print(encrypt)
