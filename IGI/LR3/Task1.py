import math
from validation import validate_input_num

stripe = "-"*65
task_description = '''
Task 1. В соответствии с заданием своего варианта составить программу
    для вычисления значения функции c помощью разложения функции в степенной ряд.
    Задать точность вычислений eps.
    x – значение аргумента, 
    F(x) – значение функции, 
    n – количество просуммированных членов ряда, 
    Math F(x) – значение функции.
'''

task_menu = '''
 ==== Task 1 Menu ====
1 - Run
0 - Exit
 '''


@validate_input_num(lambda x: abs(x) < 1, "ERROR: x must be less than 1.")
def input_x():
    """Input x from user. x must be |x| < 1."""
    return float(input("Input x: "))


@validate_input_num(lambda eps: 0 < eps < 1, "ERROR: eps must be between 0 and 1.")
def input_eps():
    """Input eps from user. eps must be 0 < eps < 1."""
    return float(input("Input eps: "))


def input_data():
    """Get x and eps from user."""
    x = input_x()
    eps = input_eps()
    return x, eps


def match_F(x):
    """Calculate exact value of ln(1 - x)."""
    res_match = math.log((1-x))
    return res_match


def row_F(x, eps, exempl_res):
    """Calculate ln(1 - x) using series. Stop when error < eps or 500 steps."""
    res = 0.0
    i = 1
    while abs(exempl_res - res) > eps and i <= 500:
        res -= (x**i) / i
        i += 1

    if i > 500:
        print("Iterations more than 500.")
    return res, i - 1

def input_menu():
    x, eps = input_data()
    ex_res = match_F(x)
    res_F, n = row_F(x, eps, ex_res)

    print(stripe+"\n|x\t|n\t|F(x)\t\t\t|MatchF(x)\t  |eps\t|\n"+stripe)
    print(x, end="\t")
    print(n, end="\t")
    print(f"|{res_F:.12f}", end="\t")
    print(f"|{ex_res:.12f}   ", end="")
    print(eps)
    print(stripe)

def task1_main():
    """Run task 1: input, calculate, print result."""
    print(task_description)
    while True:
        print(task_menu)
        try:
            choice = int(input("Select option: "))
        except ValueError:
            print("Input is not a number.")
            continue

        match choice:
            case 0:
                print("Exit.")
                break
            case 1:
                input_menu()
            case _:
                print("Incorrect input.")

if __name__ == "__main__":
    task1_main()