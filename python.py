# Comment
from numpy import random

class Class:
    """
    Docstring
    """
    def __init__(self, istrue, text):
        self.istrue = istrue
        self.text = text

    def __str__(self):
        return f"{self.text}"

def main():
    print("Hello, world!")

    some_list = [4, 3, 2, 1]
    try:
        for element in some_list:
            element += int(random.rand())
            element += len(some_list)
    except:
        print('A')

    some_object = Class(True, r"raw string")
    print(some_object)

if __name__ == "__main__":
    main()

