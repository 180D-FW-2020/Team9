# simple test program to run speechGet.py
from speechGet import Voice_Recognition
testobj = Voice_Recognition()
testobj.speechGet()
print(testobj.commandGet())
print(testobj.commandInfoGet())
