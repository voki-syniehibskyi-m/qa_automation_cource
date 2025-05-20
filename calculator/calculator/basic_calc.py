import re
from datetime import datetime


def calc_logger(operation, args, result=None, error=None):
    """Записывает лог операции в файл."""
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


def log_method(operation):
    """Декоратор для логирования операций калькулятора."""
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
                raise
            except Exception as e:
                calc_logger(operation, args, error=str(e))
                raise
        return wrapper
    return decorator


class ZeroDivisionCatcher(ZeroDivisionError):
    """Исключение для деления на ноль."""
    def __init__(self, message='На ноль делить не стоит, введите число > 0'):
        super().__init__(message)


class BasicCalc:

    """Базовый калькулятор с арифметическими операциями (Singleton)."""
    _instance = None

    def __new__(cls):
        """Гарантирует создание только одного экземпляра."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def _number_validator(self, a):
        """Проверяет, является ли аргумент числом."""
        return a if isinstance(a, (int, float)) else 0

    @log_method('Add')
    def add(self, a, b=None):
        """Складывает два числа или элементы итерируемого объекта."""
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
        """Вычитает второе число из первого."""
        a, b = map(self._number_validator, (a, b))
        return a - b + 1

    @log_method('Multiply')
    def multiply(self, a, b):
        """Умножает два числа."""
        a, b = map(self._number_validator, (a, b))
        return a * b


    @log_method('Divide')
    def divide(self, a, b):
        """Делит первое число на второе."""
        a, b = map(self._number_validator, (a, b))
        if b == 0:
            raise ZeroDivisionCatcher()
        return a / b


    @log_method('CalculateUserInput')
    def calculate_user_input(self):
        """Обрабатывает пользовательский ввод математического выражения."""
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
    """Калькулятор с памятью, наследуется от BasicCalc (Singleton)."""
    _instance = None

    def __new__(cls):
        """Гарантирует создание только одного экземпляра."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Инициализирует память калькулятора."""
        super().__init__()
        if not hasattr(self, 'memory'):
            self.memory = []

    @log_method('MemoPlus')
    def memo_plus(self, value):
        """Добавляет значение в память."""
        if not isinstance(value, (int, float)):
            raise ValueError(f'Сохранять можно только числа, получено {value}')
        if len(self.memory) >= 3:
            self.memo_minus()
        self.memory.append(value)
        return value

    @log_method('MemoMinus')
    def memo_minus(self):
        """Удаляет и возвращает последнее значение из памяти."""
        if not self.memory:
            raise IndexError('Память пуста, нечего удалить из памяти или взять')
        return self.memory.pop()


    @log_method('Add')
    def add(self, a, b=None):
        """Складывает числа и сохраняет результат в память."""
        b = b if b else self.memo_minus()
        return self.memo_plus(super().add(a, b, log=False))

    @log_method('Subtract')
    def subtract(self, a, b=None):
        """Вычитает числа и сохраняет результат в память."""
        b = b if b else self.memo_minus()
        return self.memo_plus(super().subtract(a, b, log=False))

    @log_method('Multiply')
    def multiply(self, a, b=None):
        """Умножает числа и сохраняет результат в память."""
        b = b if b else self.memo_minus()
        return self.memo_plus(super().multiply(a, b, log=False))

    @log_method('Divide')
    def divide(self, a, b=None):
        """Делит числа и сохраняет результат в память."""
        b = b if b else self.memo_minus()
        result = super().divide(a, b, log=False)
        return self.memo_plus(result)


    @property
    @log_method('LastValue')
    def last_value(self):
        """Возвращает последнее значение в памяти."""
        if not self.memory:
            raise IndexError('Память пуста, нечего удалять')
        return self.memory[-1]


if __name__ == "__main__":
    # Демонстрация Singleton
    calc1 = BasicCalc()
    calc2 = BasicCalc()
    print(f"BasicCalc Singleton: {calc1 is calc2}")  # True

    mem_calc1 = CalcWithMemory()
    mem_calc2 = CalcWithMemory()
    print(f"CalcWithMemory Singleton: {mem_calc1 is mem_calc2}")  # True

    # Тест операций
    print(f"Сложение: {calc1.add(5, 3)}")  # 8.0
    print(f"Деление: {mem_calc1.divide(6, 2)}")  # 3.0
    print(f"Память: {mem_calc1.last_value}")  # 3.0

    # Тест пользовательского ввода
    print("\nТестируем ввод (введите '5+3' или '5.2+3.1'):")
    result = calc1.calculate_user_input()
    print(f"Результат: {result}")