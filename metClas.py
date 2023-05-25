import logging
from logClass.LoggingMeta import LoggingMeta

class ExampleClass(metaclass=LoggingMeta):
    def __init__(self, name, filename = 'log.txt', filter = logging.INFO):
        self.name = name

    def greet(self):
        return f"Hello, {self.name}!"

 # Rotate log file every 10 lines with a maximum of 3 backup files

instance = ExampleClass(name = "Alice", filename='lolol.txt', filter = logging.WARN)
# print(instance.init_args)
instance2 = ExampleClass(name = "Kelly", filename='lolol.txt', filter = logging.DEBUG)
instance2.greet()
instance.greet()



