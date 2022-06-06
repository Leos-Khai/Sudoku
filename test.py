"""
https://docs.python.org/3/library/typing.html
https://www.delftstack.com/howto/python/python-open-all-files-in-directory/#:~:text=You%20can%20mainly%20use%20two,glob()%20function.
https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/
"""
import glob
import json
from cryptography.fernet import Fernet

array = [
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5],
]

print(len(glob.glob("thing/*.dat")))

for filename in glob.glob("thing/*.txt"):
    print(filename)
