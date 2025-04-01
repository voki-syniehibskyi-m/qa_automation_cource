# Основной скрипт для запуска калькулятора
from calculator.calculator.basic_calc import BasicCalc, CalcWithMemory

def main():
    calc = CalcWithMemory()
    print(calc.add(1, 2))

if __name__ == "__main__":
    main()

