class Person:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print(f"Hello, I'm {self.name}")


p = Person("Alice")
print(hasattr(p, "name"))  # 输出 True，对象有 name 属性
print(hasattr(p, "age"))  # 输出 False，对象没有 age 属性
print(hasattr(p, "say_hello"))  # 输出 True，对象有 say_hello 方法
