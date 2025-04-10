import re

class ZeroDivisionCatcher(ZeroDivisionError):
    def __init__(self, message = 'На ноль делить не стоит, введите число > 0'):
        super().__init__(message)

class BasicCalc:
  
    @staticmethod
    def add(a, b=None):
        if b is None:
            res = 0
            for i in a:
                res += i
            return res
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        try:
            if b == 0:
                raise ZeroDivisionCatcher
            else:
                return a / b
        except ZeroDivisionCatcher as e:
            print(f'{e}')



    @staticmethod
    def calculate_user_input():
        math_operations = {
            '+': BasicCalc.add,
            '-': BasicCalc.subtract,
            '*': BasicCalc.multiply,
            '/': BasicCalc.divide
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
        """
        Есть идея использовать в качестве памяти deque, но так как нам нужно хранить только 3 значения
        то по идее разница с обычным списком не будет заметна.
        """
        self.memory = []

    """Если введёно не число, то заменяем на 0"""
    def _number_validator(self, a):
        return a if isinstance(a, (int, float)) else 0

    def memo_plus(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError(f'Сохранять можно только числа, получено {value}')
        if len(self.memory) >= 3:
            self.memory.pop(0)
        self.memory.append(value)

    def memo_minus(self):
        if not self.memory:
            raise IndexError('Память пуста, нечего удалять')
        return self.memory.pop()


    def add(self, a, b = None):
        if b is None:

            if self.memory:
                b = self.memory[-1]
            else:
                raise ValueError('Второй аргумент не задан и память пуста.')

        a, b = map(self._number_validator, (a,b))
        result = super().add(a, b)
        self.memo_plus(result)
        return result

    def subtract(self, a, b = None):
        if b is None:
            if self.memory:
                b = self.memory[-1]
            else:
                raise ValueError('Второй аргумент не задан и память пуста.')

        a, b = map(self._number_validator, (a, b))
        result = a - b
        self.memo_plus(result)
        return result

    def divide(self, a, b = None):
        try:
            if b is None:
                if self.memory:
                    b = self.memory[-1]
                else:
                    raise ValueError('Второй аргумент не задан и память пуста.')

            a, b = map(self._number_validator, (a,b))
            if b == 0:
                raise ZeroDivisionCatcher('Попытка деления на 0!')
            result = a / b
            self.memo_plus(result)
            return result
        except ZeroDivisionCatcher as e:
            print(f'{e}')
            return None


    def multiply(self, a, b = None):
        if b is None:
            if self.memory:
                b = self.memory[-1]
            else:
                raise ValueError('Второй аргумент не задан и память пуста.')

        a, b = map(self._number_validator, (a,b))

        result = a * b
        self.memo_plus(result)
        return result

    @property
    def last_value(self):
        if not self.memory:
            raise IndexError('Память пуста, удалить нечего.')
        return self.memory[-1]


