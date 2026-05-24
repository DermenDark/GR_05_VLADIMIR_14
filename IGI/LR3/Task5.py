from iter_input import from_user_input

def process_number_list():
    """
    Main business function for Task 5.
    1) Input numbers from user
    2) Validate input
    3) Find first and second negative element indices
    4) Output sublist and sum of elements between them
    """
    seg_iter = from_user_input()
    numbers = []

    for item in seg_iter:
        try:
            if item.lower() == "stop":
                break
            numbers.append(float(item))
        except ValueError:
            print(f"Input is not a number: {item}")
            continue

    if not numbers:
        print("No numbers entered.")
        return

    print(f"Full list: {numbers}")

    # Find indices of first and second negative numbers
    neg_indices = [i for i, x in enumerate(numbers) if x < 0]

    if len(neg_indices) < 1:
        print("No negative numbers found.")
        return
    elif len(neg_indices) == 1:
        print(f"Only one negative number found at index {neg_indices[0]}: {numbers[neg_indices[0]]}")
        return

    first_neg_idx = neg_indices[0]
    second_neg_idx = neg_indices[1]

    start = first_neg_idx + 1
    end = second_neg_idx
    sublist = numbers[start:end]
    sum_between = sum(sublist)

    print(f"Index of first negative element: {first_neg_idx} (value: {numbers[first_neg_idx]})")
    print(f"Index of second negative element: {second_neg_idx} (value: {numbers[second_neg_idx]})")
    print(f"Sublist between first and second negative elements: {sublist}")
    print(f"Sum of elements between first and second negative elements: {sum_between}")

def input_menu_task5():
    """Menu for Task 5."""
    while True:
        print("""
 ==== Task 5 Menu ====
1 - Run
0 - Exit""")
        try:
            choice = int(input("Select option: "))
            if choice in (0, 1):
                return choice
            print("Incorrect input. Choose 0 or 1.")
        except ValueError:
            print("Input is not number.")

def task5_main():
    """Run Task 5 with menu."""
    print("""
Задание 5. В соответствии с заданием своего варианта составить программу
    для обработки вещественных списков.
    Программа должна содержать следующие базовые функции:
        1) ввод элементов списка пользователем;
        2) проверка корректности вводимых данных;
        3) реализация основного задания с выводом результатов;
        4) вывод списка на экран.
condition:
    Найти номер минимального отрицательного 
    элемента списка и сумму элементов списка,
    расположенных между первым и вторым 
    отрицательными элементами""")
    while True:
        choice = input_menu_task5()

        if choice == 0:
            print("Exit.")
            break
        elif choice == 1:
            process_number_list()

if __name__ == "__main__":
    task5_main()