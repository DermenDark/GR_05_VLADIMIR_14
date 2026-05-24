from Task1 import task1_main
from Task2 import task2_main
from Task3 import task3_main
from Task4 import task4_main
from Task5 import task5_main

from validation import validate_input_num

hello_str = '''
This is the program of the 3lab_work

Shirko Vladimir ---- option 14
from g.453505 27.03.2026
'''
menu_str = '''
==== Menu ====
1 - Task1
2 - Task2
3 - Task3
4 - Task4
5 - Task5
:'''
@validate_input_num(lambda x: 1 <= x <= 5, "Incorrect input. Choose 1–5.")
def input_menu():
    return int(input(menu_str))

def main():
    print(hello_str)
    while True:
        n = input_menu()
        print("\n")
        match n:
            case 1: task1_main()
            case 2: task2_main()
            case 3: task3_main()
            case 4: task4_main()
            case 5: task5_main()
            case _:
                print("Incorrect input.")

if __name__ == "__main__":
    main()