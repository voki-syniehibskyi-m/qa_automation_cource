import re
from datetime import datetime
from sre_constants import error
from turtledemo.clock import datum
import time


# Логирование вынес вне калькулятора.
def calc_logger(operation, args, result=None, error=None):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_data = {
        'timestamp': timestamp,
        'operation': operation,
        'arguments': str(args),
        'result': str(result) if result is not None else 'N/A'
    }
    if error is not None:
        log_data['error'] = str(error)

    with open('calc_log.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(f"[{timestamp}] Log Entry:\n")
        for key, value in log_data.items():
            log_file.write(f"  {key.capitalize()}: {value}\n")
        log_file.write('\n')


# Декоратор который поможет нам логировать вызываемые функции.
def log_method(operation):
    def decorator(func):
        def wrapper(self, *args, log=True, **kwargs):
            if not log:
                return func(self, *args, **kwargs)
            try:
                result = func(self, *args, **kwargs)
                calc_logger(operation, args, result=result)
                return result
            except ZeroDivisionCatcher as e:
                calc_logger(operation, args, error=str(e))
                print(f'{e}')
                return None
            except Exception as e:
                calc_logger(operation, args, error=str(e))
                raise

        return wrapper

    return decorator


class ZeroDivisionCatcher(ZeroDivisionError):
    def __init__(self, message='На ноль делить не стоит, введите число > 0'):
        super().__init__(message)


class BasicCalc:
    def _number_validator(self, a):
        return a if isinstance(a, (int, float)) else 0

    @log_method('Add')
    def add(self, a, b=None):
        if a is None and b is None:
            raise ValueError('Оба аргумента отсутствуют')
        if b is None:
            if not hasattr(a, '__iter__'):
                raise TypeError(f'Аргумент {a} не является итерируемым')
            res = 0
            for i in a:
                res += self._number_validator(i)
            return res
        a, b = map(self._number_validator, (a, b))
        return a + b

    @log_method('Subtract')
    def subtract(self, a, b):
        a, b = map(self._number_validator, (a, b))
        return a - b

    @log_method('Multiply')
    def multiply(self, a, b):
        a, b = map(self._number_validator, (a, b))
        return a * b

    @log_method('Divide')
    def divide(self, a, b):
        a, b = map(self._number_validator, (a, b))
        if b == 0:
            raise ZeroDivisionCatcher()
        return a / b

    @log_method('CalculateUserInput')
    def calculate_user_input(self):
        math_operations = {
            '+': self.add,
            '-': self.subtract,
            '*': self.multiply,
            '/': self.divide
        }
        while True:
            user_input = input('Введите математическое выражение: ')
            string_to_match = re.match(r"(^\d+(\.\d+)?)([-+*/])(\d+(\.\d+)?$)", user_input)
            if string_to_match:
                calc_logger('UserInput', (user_input,), result='Parsed')
                break
            else:
                calc_logger('UserInput', (user_input,), error='Invalid expression')
                print('Введено неверное выражение, повторите ввод')

        first_num = float(string_to_match.group(1))
        second_num = float(string_to_match.group(4))
        math_symbol = string_to_match.group(3)
        return math_operations.get(math_symbol)(first_num, second_num)


class CalcWithMemory(BasicCalc):
    def __init__(self):
        super().__init__()
        self.memory = []

    @log_method('MemoPlus')
    def memo_plus(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError(f'Сохранять можно только числа, получено {value}')
        if len(self.memory) >= 3:
            self.memo_minus()
        self.memory.append(value)
        return value

    @log_method('MemoMinus')
    def memo_minus(self):
        if not self.memory:
            raise IndexError('Память пуста, нечего удалить из памяти или взять')
        return self.memory.pop()

    @log_method('Add')
    def add(self, a, b=None):
        b = b if b else self.memo_minus()
        return self.memo_plus(super().add(a, b, log=False))

    @log_method('Subtract')
    def subtract(self, a, b=None):
        b = b if b else self.memo_minus()
        return self.memo_plus(super().subtract(a, b, log=False))

    @log_method('Multiply')
    def multiply(self, a, b=None):
        b = b if b else self.memo_minus()
        return self.memo_plus(super().multiply(a, b, log=False))

    @log_method('Divide')
    def divide(self, a, b=None):
        b = b if b else self.memo_minus()
        result = super().divide(a, b, log=False)
        if result is not None:
            return self.memo_plus(result)
        return None

    @property
    @log_method('LastValue')
    def last_value(self):
        if not self.memory:
            raise IndexError('Память пуста, нечего удалять')
        return self.memory[-1]


