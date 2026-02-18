"""
Exercise 1.D.1 — Fix the Bugs
Guide: docs/python-guide/01-foundations.md

Each function has a bug. Find and fix it.
"""


# Bug 1: Should return the average of a list
def average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)  # What if numbers is empty?


# Bug 2: Should count words in a sentence
def count_words(sentence):
    words = sentence.split(",")  # Wrong delimiter
    return len(words)


# Bug 3: Should check if year is a leap year
def is_leap_year(year):
    return year % 4 == 0  # Incomplete logic


# Bug 4: Should reverse a string without using [::-1]
def reverse_string(text):
    result = ""
    for i in range(len(text)):
        result = result + text[i]  # Not reversing
    return result


# Bug 5: Mutable default argument
def add_item(item, items=[]):
    items.append(item)
    return items


# TODO: Fix each bug and add test cases to verify
