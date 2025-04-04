import re

class BasicCalc:

    @staticmethod
    def add(a, b=None):
        # функция сложения обновлена, если 1 аргумент, то ждёт итерируемый объект.
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
        return a / b



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

        first_num = string_to_match.group(1)
        second_num = string_to_match.group(4)
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

    def memo_plus(self, value):
        if len(self.memory) >= 3:
            self.memory.pop(0)
        self.memory.append(value)

    def memo_minus(self):
        return self.memory.pop()


    def add(self, a, b = None):
        if b is None:
            b = self.memory[-1]
        result = super().add(a, b)
        self.memo_plus(result)
        return result

    def subtract(self, a, b = None):
        if b is None:
            b = self.memory[-1]
        result = a - b
        self.memo_plus(result)
        return result

    def divide(self, a, b = None):
        if b is None:
            b = self.memory[-1]
        result = a / b
        self.memo_plus(result)
        return result

    def multiply(self, a, b = None):
        if b is None:
            b = self.memory[-1]
        result = a * b
        self.memo_plus(result)
        return result

    @property
    def last_value(self):
        return self.memory[-1] if self.memory else None




