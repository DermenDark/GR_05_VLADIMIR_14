from typing import Iterable, Iterator

def from_list(seq: Iterable) -> Iterator:
    """Create iterator from list."""
    for item in seq:
        yield item

def from_user_input(prompt: str = "Enter further (Empty input stops): ") -> Iterator:
    """Create iterator from user input. Empty input stops."""
    while True:
        temp = input(prompt)
        if temp == "":
            break
        yield temp