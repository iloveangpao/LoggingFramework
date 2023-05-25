import logging
import io
import sys
import pytest
from ..logClass.LoggingMeta import LoggingMeta
import os

class ExampleClass(metaclass=LoggingMeta):
    def __init__(self, name, filter = logging.INFO , filename = 'logs.txt'):
        self.name = name

    def greet(self):
        return f"Hello, {self.name}!"

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return 0

def test_func(eg_instance, caplog):
    eg_instance.greet()
    assert 'Calling greet' in caplog.text
    assert 'greet returned: Hello, John!' in caplog.text

def test_log(eg_instance, temp_logpath):
    eg_instance.greet()
    assert 'greet returned: Hello, John!\n' in temp_logpath.read_text()

def test_filter(filter_instance, temp_logpath):
    filter_instance.greet()
    assert 'greet returned: Hello, Kelly!' not in temp_logpath.read_text()

def test_rotate(setupRotateTest, tmp_path_factory):
    for i in range(5):
        setupRotateTest.greet()
    assert find('lolol.txt.1', tmp_path_factory.getbasetemp())


if __name__ == "__main__":
    pytest.main()
