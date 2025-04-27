# Отдельный модуль с математическими операциями
import re

def add(a, b = None):
    # функция сложения обновлена, если 1 аргумент, то ждёт итерируемый объект.
    if b is None:
        res = 0
        for i in a:
            res += i
        return res

    return a + b


def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

#Вспомогательная функция для calc() преобразуем число к float или int, если есть точка то флоат, если нет то инт.
#Не нравился вывод если к примеру было число без точки а инпут 12+12, то вывод 24.0

def _number_checker(num_str):
    if '.' in num_str:
        return float(num_str)
    else:
        return int(num_str)

#Введена новая функция которая будет обрабатыавть пользовательский ввод и выводить результат.
def calculator():

    math_operations = { # ссылки на мат. ф-ции занесены в объект
        '+': add,
        '-': subtract,
        '*': multiply,
        '/': divide
    }


    while True:
        #Пока юзер не введёт правильную строку обновляем запрос.
        user_input = input('Введите математическое выражение: ')
        string_to_match = re.match(r"(^\d+(\.\d+)?)([-+*/])(\d+(\.\d+)?$)", user_input)

        if string_to_match is not None:
            break
        else:
            print('Введено неверное выражение, повторите ввод')

    #Заполняем переменные частями выражения введённого пользователем.(первое число, символ, второе число)
    #Числа приводим к инт или флоат, при помощи вспомогательной функции
    first_num = _number_checker(string_to_match.group(1))
    second_num = _number_checker(string_to_match.group(4))
    math_symbol = string_to_match.group(3)


    #Вызываем нужную нам функцию и выводим результат.
    return math_operations.get(math_symbol)(first_num, second_num)

if __name__ == "__main__":
    print(calculator())


