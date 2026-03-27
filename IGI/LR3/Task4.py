
def get_words(text: str):
    """Convert text to list of words, remove commas and dots."""
    return text.replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ").split()


def count_short_words(words, limit=7):
    """Count words shorter than limit."""
    return sum(1 for w in words if len(w) < limit)


def longest_word_ending_a(words):
    """Find shortest word with 'a'."""
    max_length = max(len(w) for w in words)
    longest_a = ""
    for w in words:
        if w.endswith("a") and len(w) < max_length:
            if len(w) > len(longest_a):
                longest_a = w
    return longest_a

def words_sorted_by_length(words):
    """Return words sorted by length descending."""
    words_copy = words.copy()
    sorted_words = []

    while words_copy:
        max_len = max(len(w) for w in words_copy)
        for w in list(words_copy):
            if len(w) == max_len:
                sorted_words.append(w)
                words_copy.remove(w)
    return sorted_words


def input_text():
    """Input text from user or use default."""
    text = input("Enter text (or press Enter to use default):\n")
    if not text:
        text = '''
So she was considering in her own mind, as well as she could, for the hot 
day made her feel very sleepy and stupid, whether the pleasure of making a 
daisy-chain would be worth the trouble of getting up and picking the daisies, 
when suddenly a White Rabbit with pink eyes ran close by her.'''
    return text

def input_menu_task4():
    """Menu for Task 4. Run specific analysis or exit."""
    while True:
        print("""
 ==== Task 4 Menu ====
    1 - Count words shorter than 7 characters
    2 - Find shortest word with 'a'
    3 - Show all words sorted by length descending
    0 - Exit""")
        try:
            choice = int(input(": "))
            if choice in (0, 1, 2, 3):
                return choice
            print("Incorrect input.")
        except ValueError:
            print("Input is not number.")

def task4_main():
    """Run Task 4 with menu for individual analysis."""
    print('''
Задание 4. Не использовать регулярные выражения. 
    Дана строка текста, в которой слова разделены пробелами и запятыми.
    В соответствии с заданием своего варианта составьте программу
    для анализа строки, инициализированной в коде программы.
condition:
    а) определить число слов, длина которых меньше 7 символов;
    б) найти самое короткое слово, заканчивающееся на букву 'a';
    в) вывести все слова в порядке убывания их длин.''') 
    while True:
        choice = input_menu_task4()

        if choice == 0:
            print("Exit.")
            break

        text = input_text()
        words = get_words(text)

        if choice == 1:
            count = count_short_words(words)
            print(f"Number of words shorter than 7 characters: {count}")

        elif choice == 2:
            longest_a = longest_word_ending_a(words)
            print(f"Shortest word with 'a': {longest_a}")

        elif choice == 3:
            sorted_words = words_sorted_by_length(words)
            print(f"Words sorted by length descending: {sorted_words}")


if __name__ == "__main__":
    task4_main()