import re
from datetime import datetime
from sre_constants import error
from turtledemo.clock import datum


class ZeroDivisionCatcher(ZeroDivisionError):
    def __init__(self, message = 'На ноль делить не стоит, введите число > 0'):
        super().__init__(message)

class BasicCalc:
    """добавлен метод класса который будет логировать данные по совершённым
     операциям, время, операция, аргументы, результат, """
    def _calc_logger(self, operation, args, result=None, error=None):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_data = {
            'timestamp': timestamp,
            'operation': operation,
            'arguments': str(args),
            'result': str(result) if result is not None else 'N/A'
        }
        log_string = (
            f"[{log_data['timestamp']}] "
            f"Operation: {log_data['operation']}, "
            f"Arguments: {log_data['arguments']}, "
            f"Result: {log_data['result']}"
        )
        """Ошибка опциональная, не хотел выводить что ошибок нет если всё ок, 
         лучше выведем если будут, а лог будет чище."""
        if error is not None:
            log_string += f", Error: {str(error)}"
        log_string += '\n'
        with open('calc_log.txt', 'a', encoding='utf-8') as log_file:
            log_file.write(log_string)


    def add(self, a, b=None):
        if b is None:
            res = 0
            for i in a:
                res += i
            self._calc_logger('Add', a, res)
            return res
        result = a + b
        self._calc_logger('Add', (a,b), result)
        return result

    def subtract(self, a, b):
        result = a - b
        self._calc_logger('subtract', (a, b), result)
        return result

    def multiply(self, a, b):
        result = a * b
        self._calc_logger('Multiply', (a, b), result)
        return result

    def divide(self, a, b):
        try:
            if b == 0:
                raise ZeroDivisionCatcher
            result = a / b
            self._calc_logger('Divide', (a, b), result)
            return result
        except ZeroDivisionCatcher as e:
            self._calc_logger('Divide', (a, b), error=e)
            print(f'{e}')
            return None

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

            if string_to_match is not None:
                break
            else:
                print('Введено неверное выражение, повторите ввод')

        first_num = float(string_to_match.group(1))
        second_num = float(string_to_match.group(4))
        math_symbol = string_to_match.group(3)

        return math_operations.get(math_symbol)(first_num, second_num)

# Версия калькулятора с памятью
class CalcWithMemory(BasicCalc):
    def __init__(self):
        self.memory = []

    """Если введёно не число, то заменяем на 0"""
    def _number_validator(self, a):
        return a if isinstance(a, (int, float)) else 0

    def memo_plus(self, value):
        try:
            if not isinstance(value, (int, float)):
                raise ValueError(f'Сохранять можно только числа, получено {value}')
            if len(self.memory) >= 3:
                self.memo_minus()
            self.memory.append(value)
            self._calc_logger('MemoPlus', value, value)
        except ValueError as e:
            self._calc_logger('MemoPlus', value, error=e)
            raise

    def memo_minus(self):
        try:
            if not self.memory:
                raise IndexError('Память пуста, нечего удалить из памяти или взять')
            result = self.memory.pop()
            self._calc_logger('MemoMinus', None, result)
            return result
        except IndexError as e:
            self._calc_logger('MemoMinus', None, error=e)
            raise

    def add(self, a, b=None):
        try:
            if b is None:
                b = self.memo_minus()
            a, b = map(self._number_validator, (a, b))
            result = super().add(a, b)
            self.memo_plus(result)
            return result
        except ValueError as e:
            self._calc_logger('Add', (a, b) if b is not None else a, error=e)
            raise

    def subtract(self, a, b = None):
        try:
            if b is None:
                b = self.memo_minus()
            a, b = map(self._number_validator, (a, b))
            result = super().subtract(a, b)
            self.memo_plus(result)
            return result
        except ValueError as e:
            self._calc_logger('Subtract', (a, b) if b is not None else a, error=e)
            raise

    def divide(self, a, b=None):
        try:
            if b is None:
                b = self.memo_minus()
            a, b = map(self._number_validator, (a, b))
            if b == 0:
                raise ZeroDivisionCatcher('Попытка деления на 0!')
            result = super().divide(a, b)
            if result is not None:
                self.memo_plus(result)
            return result
        except ZeroDivisionCatcher as e:
            self._calc_logger('Divide', (a, b), error=e)
            print(f'{e}')
            return None
        except ValueError as e:
            self._calc_logger('Divide', (a, b) if b is not None else a, error=e)
            raise


    def multiply(self, a, b=None):
        try:
            if b is None:
                b = self.memo_minus()
            a, b = map(self._number_validator, (a, b))
            result = super().multiply(a, b)
            self.memo_plus(result)
            return result
        except ValueError as e:
            self._calc_logger('Multiply', (a, b) if b is not None else a, error=e)
            raise

    @property
    def last_value(self):
        try:
            if not self.memory:
                raise IndexError('Память пуста, нечего удалять')
            result = self.memory[-1]
            self._calc_logger('LastValue', None, result)
            return result
        except IndexError as e:
            self._calc_logger('LastValue', None, error=e)
            raise


