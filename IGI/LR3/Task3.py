def task3_funk(analyse_str:str):
    """
    Main function for task 3.
    Count commas and spaces in user input string.
    """
    count_coma = 0
    count_space = 0
    whitespace_chars = {' ', '\t', '\n', '\r', '\v', '\f'}

    for el in analyse_str:
        if el in whitespace_chars:
            count_space += 1
        elif el == ",":
            count_coma += 1

    return count_coma, count_space

def input_menu_task3():
    """Menu for Task 3. Choose to run or exit."""
    while True:
        print("""         
==== Task 3 Menu ====
1 - Run
0 - Exit""")
        try:
            choice = int(input("Select option: "))
            if choice in (0, 1):
                return choice
            print("Incorrect input.")
        except ValueError:
            print("Input is not number.")

def task3_main():
    """Run Task 3 with menu."""
    print('''
Task 3. Не использовать регулярные выражения.
    В соответствии с заданием своего варианта
    составить программу для анализа текста,
    вводимого с клавиатуры.
condition:
    В строке, вводимой с клавиатуры, подсчитать количество про-
    бельных символов и запятых.''')
    while True:
        choice = input_menu_task3()

        if choice == 0:
            print("Exit.")
            break

        elif choice == 1:
            analyse_str = input("Input your string: ")
            count_coma, count_space = task3_funk(analyse_str)
            print(f"count_coma: {count_coma}")
            print(f"count_space: {count_space}")