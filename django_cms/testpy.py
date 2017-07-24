# coding:utf-8



def foo():
    a =1
    def bar():
        b =a*2
        a =b +1

        print a
    return bar

foo()()