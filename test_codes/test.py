"""
https://docs.python.org/3/library/typing.html
https://www.delftstack.com/howto/python/python-open-all-files-in-directory/#:~:text=You%20can%20mainly%20use%20two,glob()%20function.
https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/
"""
import glob
import json
from cryptography.fernet import Fernet
import os
array = [
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5],
]
tmp = str(array)
tmp2 = list(tmp)
print(tmp2)
if not glob.glob("thing/grid.txt"):
    with open("thing/grid.txt", "wb") as file:
        file.write(array)
print(len(glob.glob("thing/*.dat")))

for filename in glob.glob("thing/*.txt"):
    print(os.path.basename(filename))
if len(glob.glob("thing/*.key")) == 0:
    key = Fernet.generate_key()
    with open("thing/key.key", "wb") as keyfile:
        keyfile.write(key)
else:
    with open("thing/key.key", "rb") as keyfile:
        key = keyfile.read()
fernet = Fernet(key)
with open("thing/grid.txt", "rb") as file:
    ori = file.read()
encrypt = fernet.encrypt(ori)
with open("thing/output.txt", "wb") as file:
    file.write(encrypt)
with open("thing/ori.txt", "wb") as file:
    file.write(ori)
