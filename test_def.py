#!/usr/bin/env python3
def test1(a1):
    c=3
    return a1,c
def test2(a2):
     print(a2)
def test3(a1,b2):
    if test1(a1)[0]==4:
        print(test1(a1)[0])
        print(test1(a1)[1])
    test2(b2)
test3(4,5)