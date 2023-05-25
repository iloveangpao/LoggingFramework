from ..logClass.LoggingMeta import LoggingMeta
import pytest
import tempfile
import logging

class ExampleClass(metaclass=LoggingMeta):
    # @pytest.fixture(autouse = True)
    def __init__(self, name, filter = logging.INFO , filename = 'logs.txt'):
        self.name = name

    def greet(self):
        return f"Hello, {self.name}!"

@pytest.fixture
def eg_instance(temp_logpath):
    # print(temp_logpath)
    return ExampleClass(name = 'John', filename = temp_logpath, filter = logging.DEBUG)

@pytest.fixture
def filter_instance(temp_logpath):
    # print(temp_logpath)
    return ExampleClass(name = 'Kelly', filename = temp_logpath, filter = logging.WARN)

# @pytest.fixture
# def eg_logOutput():
#     return 'Calling __init__\
# __init__ returned: None\
# Calling greet\
# Calling greet\
# greet returned: Hello, John!\
# greet returned: Hello, John!'

@pytest.fixture
def temp_logpath(tmp_path_factory):
    p = tmp_path_factory.getbasetemp() / 'logs.txt'
    return p

@pytest.fixture
def setupRotateTest(tmp_path_factory):
    d = tmp_path_factory.getbasetemp() / 'lolol.txt'
    instance = ExampleClass(name = 'Mark', filename = d, filter = logging.DEBUG)
    return instance


