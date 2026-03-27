from iter_input import from_list, from_user_input
from typing import Iterator


def subtract_from_10000(seq_iterator: Iterator):
    """Subtract numbers from 10000 step by step."""
    total = 10000

    for item in seq_iterator:
        try:
            number = float(item)
        except ValueError:
            print(f"Input is not a number: {item}")
            continue

        total -= number
        print(f"Current total: {total}")

        if total < 0:
            print("Got a negative result.")
            break

    return total

def input_menu():
    """Select input type."""
    while True:
        print("""
==== Task 2 Menu ====
1 - Use default list
2 - Input from keyboard
0 - Exit""")
        try:
            choice = int(input("Select option: "))
            if choice in (0, 1, 2):
                return choice
            print("Incorrect input.")
        except ValueError:
            print("Input is not number.")

def task2_main():
    """Main function for task 2."""
    print("""
Task 2. В соответствии с заданием своего варианта
    составить программу для нахождения суммы
    последовательности чисел.
condition:
    Организовать цикл, который принимает целые числа и вычитает их из 10000.
    Окончание – получение отрицательного итога.""")
    while True:
        choice = input_menu()

        if choice == 1:
            numbers = [100, 500, 3000, 4500, 1000]
            print(numbers)
            seq_iter = from_list(numbers)
        elif choice == 2:
            seq_iter = from_user_input()
        else:
            print("Exit.")
            break

        final_total = subtract_from_10000(seq_iter)
        print(f"Final total: {final_total}")