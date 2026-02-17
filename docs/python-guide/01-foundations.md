# SECTION 1 — FOUNDATIONS

---

## PART A — CONCEPT EXPLANATION

### What is a Variable?

A **variable** is a name that points to a value stored in memory. Think of it as a labeled box.

```python
age = 25        # The label "age" points to the integer 25
name = "Arun"   # The label "name" points to the string "Arun"
pi = 3.14159    # The label "pi" points to a float
```

**Mental model:** Variables in Python don't *contain* values — they *refer* to objects. When you write `x = 10`, Python creates an integer object `10` in memory, then sticks the label `x` on it.

```
x = 10
y = x       # y now points to the SAME object 10
x = 20      # x now points to a NEW object 20; y still points to 10

print(x)    # 20
print(y)    # 10  ← y didn't change
```

### Python's Core Data Types

| Type | Example | Use case |
|------|---------|----------|
| `int` | `42` | Counting, indexing |
| `float` | `3.14` | Measurements, calculations |
| `str` | `"hello"` | Text, messages, labels |
| `bool` | `True`, `False` | Decisions, flags |
| `None` | `None` | "No value", "not set yet" |

```python
# Check the type of anything:
type(42)        # <class 'int'>
type("hello")   # <class 'str'>
type(True)      # <class 'bool'>
type(None)      # <class 'NoneType'>
```

**Common mistake:** Confusing `=` (assignment) with `==` (comparison).
```python
x = 5       # Assigns 5 to x
x == 5      # Asks: "Is x equal to 5?" → True
```

### What is a Loop?

A **loop** repeats a block of code. Python has two types:

**`for` loop** — iterate over a sequence (you know how many times):
```python
for name in ["Alice", "Bob", "Charlie"]:
    print(f"Hello, {name}!")
```

**`while` loop** — repeat as long as a condition is true (you don't know how many times):
```python
count = 0
while count < 5:
    print(count)
    count += 1
```

**Mental model:** A `for` loop is like going through a checklist. A `while` loop is like "keep stirring until the sauce thickens" — you don't know exactly when it'll be done.

**Common mistake:** Infinite loops with `while`:
```python
# DANGER — this never stops:
x = 1
while x > 0:
    print(x)
    x += 1      # x keeps growing, always > 0
```

### What is a Function?

A **function** is a reusable block of code with a name, inputs (parameters), and an output (return value).

```python
def calculate_area(width, height):
    """Calculate the area of a rectangle."""
    return width * height

result = calculate_area(5, 3)   # result = 15
```

**Why functions matter:**
1. **Reuse** — write once, call many times
2. **Abstraction** — hide complexity behind a name
3. **Testing** — test one function at a time
4. **Readability** — `calculate_area(5, 3)` is clearer than `5 * 3` in context

**Mental model:** A function is a machine. You put ingredients in (parameters), it does work, and gives you a product back (return value). If it doesn't `return` anything, it returns `None` by default.

### Collections: Lists, Dicts, Sets

**List** — ordered, mutable sequence:
```python
fruits = ["apple", "banana", "cherry"]
fruits.append("date")           # Add to end
fruits[0]                       # "apple" (0-indexed)
len(fruits)                     # 4
```

**Dictionary** — key-value pairs (like a real dictionary: word → definition):
```python
person = {
    "name": "Arun",
    "age": 25,
    "skills": ["Python", "Docker"],
}
person["name"]                  # "Arun"
person["role"] = "Engineer"     # Add new key
"age" in person                 # True
```

**Set** — unordered collection of unique elements:
```python
tags = {"python", "docker", "python"}   # Duplicates removed
len(tags)                               # 2
tags.add("linux")
"python" in tags                        # True (fast lookup)
```

**When to use what:**

| Use case | Collection | Why |
|----------|-----------|-----|
| Ordered items, may have duplicates | `list` | Preserves order, allows repeats |
| Look up values by a key | `dict` | O(1) lookup by key |
| Track unique items, fast membership test | `set` | No duplicates, O(1) `in` check |
| Data that should never change | `tuple` | Immutable sequence |

### Writing Clean, Readable Code

**Clean code** is code that another developer (or future you) can understand in 30 seconds.

**Rules:**
1. **Meaningful names** — `user_count` not `uc`, `calculate_tax` not `calc`
2. **One function, one job** — if a function does 3 things, split it into 3 functions
3. **No magic numbers** — `if age >= 18` not `if age >= VOTING_AGE` (wait, the other way)

```python
# BAD: What does this do?
def p(d, r):
    return d * (1 + r/100)

# GOOD: Self-documenting
def apply_discount(price, discount_percent):
    """Apply a percentage discount to a price."""
    return price * (1 - discount_percent / 100)
```

**Common beginner misunderstandings:**

| Mistake | Reality |
|---------|---------|
| "Comments explain bad code" | Clean code doesn't need comments. Comments explain *why*, not *what* |
| "Short variable names are faster" | `x` saves you 1 second typing, costs you 10 minutes reading |
| "It works, so it's fine" | If nobody can maintain it, it's technical debt |
| "I'll clean it up later" | You won't. Write it clean the first time |

---

## PART B — BEGINNER PRACTICE

### Exercise 1.B.1 — Variables and Types

```python
# Create variables of each type and print their type
name = "Your Name"
age = 25
height = 5.9
is_student = True
favorite_color = None

print(f"name: {name} (type: {type(name).__name__})")
print(f"age: {age} (type: {type(age).__name__})")
print(f"height: {height} (type: {type(height).__name__})")
print(f"is_student: {is_student} (type: {type(is_student).__name__})")
print(f"favorite_color: {favorite_color} (type: {type(favorite_color).__name__})")
```

**Expected output:**
```
name: Your Name (type: str)
age: 25 (type: int)
height: 5.9 (type: float)
is_student: True (type: bool)
favorite_color: None (type: NoneType)
```

### Exercise 1.B.2 — String Operations

```python
# Practice common string operations
message = "  Hello, Python World!  "

print(message.strip())          # Remove whitespace
print(message.lower())          # Lowercase
print(message.upper())          # Uppercase
print(message.replace("World", "Engineer"))
print(message.split(","))       # Split into list
print(len(message.strip()))     # Length without whitespace

# f-strings (formatted string literals) — the modern way
name = "Arun"
language = "Python"
print(f"{name} is learning {language}")
print(f"2 + 3 = {2 + 3}")
print(f"{'centered':^20}")      # Center-align in 20 chars
```

### Exercise 1.B.3 — Number Operations

```python
# Integer arithmetic
a, b = 17, 5

print(f"{a} + {b} = {a + b}")      # Addition: 22
print(f"{a} - {b} = {a - b}")      # Subtraction: 12
print(f"{a} * {b} = {a * b}")      # Multiplication: 85
print(f"{a} / {b} = {a / b}")      # True division: 3.4
print(f"{a} // {b} = {a // b}")    # Floor division: 3
print(f"{a} % {b} = {a % b}")      # Modulo (remainder): 2
print(f"{a} ** {b} = {a ** b}")    # Exponentiation: 1419857

# Useful built-ins
numbers = [10, 45, 3, 78, 22]
print(f"min: {min(numbers)}")       # 3
print(f"max: {max(numbers)}")       # 78
print(f"sum: {sum(numbers)}")       # 158
print(f"sorted: {sorted(numbers)}") # [3, 10, 22, 45, 78]
```

### Exercise 1.B.4 — Conditionals

```python
# if / elif / else
temperature = 35

if temperature > 40:
    status = "extreme heat"
elif temperature > 30:
    status = "hot"
elif temperature > 20:
    status = "warm"
elif temperature > 10:
    status = "cool"
else:
    status = "cold"

print(f"{temperature}°C is {status}")

# Ternary (inline if)
age = 20
label = "adult" if age >= 18 else "minor"
print(f"Age {age}: {label}")
```

### Exercise 1.B.5 — `for` Loops

```python
# Loop through a list
fruits = ["apple", "banana", "cherry", "date"]
for fruit in fruits:
    print(f"I like {fruit}")

# Loop with index using enumerate
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")

# Loop through a range
for i in range(5):
    print(f"Count: {i}")        # 0, 1, 2, 3, 4

# Loop through a string
for char in "Python":
    print(char, end=" ")        # P y t h o n
print()

# Nested loops
for row in range(3):
    for col in range(4):
        print(f"({row},{col})", end=" ")
    print()
```

### Exercise 1.B.6 — `while` Loops

```python
# Countdown
count = 5
while count > 0:
    print(f"T-minus {count}...")
    count -= 1
print("Liftoff! 🚀")

# Input validation loop (simulated)
attempts = 0
max_attempts = 3
password = "secret"

# Simulating user input:
guesses = ["wrong", "nope", "secret"]
for guess in guesses:
    attempts += 1
    if guess == password:
        print(f"Access granted after {attempts} attempt(s)")
        break
    print(f"Wrong password. Attempt {attempts}/{max_attempts}")
    if attempts >= max_attempts:
        print("Account locked!")
        break
```

### Exercise 1.B.7 — Functions: Basics

```python
# Simple function
def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}!"

print(greet("Arun"))
print(greet("World"))


# Function with default parameter
def power(base, exponent=2):
    """Raise base to exponent (default: squared)."""
    return base ** exponent

print(power(5))       # 25 (5²)
print(power(2, 10))   # 1024 (2¹⁰)


# Function that returns multiple values
def min_max(numbers):
    """Return the min and max of a list."""
    return min(numbers), max(numbers)

low, high = min_max([3, 1, 4, 1, 5, 9])
print(f"Min: {low}, Max: {high}")
```

### Exercise 1.B.8 — Functions: Practice Problems

```python
# 1. Write a function that checks if a number is even
def is_even(n):
    return n % 2 == 0

assert is_even(4) == True
assert is_even(7) == False
print("✓ is_even works")


# 2. Write a function that reverses a string
def reverse_string(s):
    return s[::-1]

assert reverse_string("hello") == "olleh"
assert reverse_string("Python") == "nohtyP"
print("✓ reverse_string works")


# 3. Write a function that counts vowels
def count_vowels(text):
    vowels = set("aeiouAEIOU")
    return sum(1 for char in text if char in vowels)

assert count_vowels("hello") == 2
assert count_vowels("Python") == 1
assert count_vowels("aeiou") == 5
print("✓ count_vowels works")


# 4. Write a function that removes duplicates (preserving order)
def remove_duplicates(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

assert remove_duplicates([1, 2, 2, 3, 1, 4]) == [1, 2, 3, 4]
print("✓ remove_duplicates works")
```

### Exercise 1.B.9 — Lists: Deep Practice

```python
# Creating and modifying lists
numbers = [1, 2, 3, 4, 5]

# Add elements
numbers.append(6)          # [1, 2, 3, 4, 5, 6]
numbers.insert(0, 0)       # [0, 1, 2, 3, 4, 5, 6]
numbers.extend([7, 8])     # [0, 1, 2, 3, 4, 5, 6, 7, 8]

# Remove elements
numbers.pop()              # Removes and returns last: 8
numbers.pop(0)             # Removes and returns index 0: 0
numbers.remove(5)          # Removes first occurrence of 5

# Slicing — [start:stop:step]
letters = ['a', 'b', 'c', 'd', 'e', 'f']
print(letters[1:4])        # ['b', 'c', 'd']  (index 1 to 3)
print(letters[:3])         # ['a', 'b', 'c']  (first 3)
print(letters[-2:])        # ['e', 'f']       (last 2)
print(letters[::2])        # ['a', 'c', 'e']  (every 2nd)
print(letters[::-1])       # ['f', 'e', 'd', 'c', 'b', 'a']  (reversed)

# List comprehension — concise way to create lists
squares = [x**2 for x in range(10)]
print(squares)             # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

evens = [x for x in range(20) if x % 2 == 0]
print(evens)               # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Filtering with comprehension
words = ["hello", "world", "hi", "python", "go"]
long_words = [w for w in words if len(w) > 3]
print(long_words)          # ['hello', 'world', 'python']
```

### Exercise 1.B.10 — Dictionaries: Deep Practice

```python
# Creating dictionaries
student = {
    "name": "Alice",
    "age": 22,
    "grades": {"math": 95, "physics": 88, "cs": 92},
}

# Access values
print(student["name"])                  # "Alice"
print(student["grades"]["cs"])          # 92

# Safe access with .get() — returns None if key missing
print(student.get("email"))            # None
print(student.get("email", "N/A"))     # "N/A" (with default)

# Iterate
for key, value in student.items():
    print(f"  {key}: {value}")

# Dictionary comprehension
names = ["alice", "bob", "charlie"]
name_lengths = {name: len(name) for name in names}
print(name_lengths)     # {'alice': 5, 'bob': 3, 'charlie': 7}

# Counting occurrences
text = "hello world hello python hello"
word_counts = {}
for word in text.split():
    word_counts[word] = word_counts.get(word, 0) + 1
print(word_counts)      # {'hello': 3, 'world': 1, 'python': 1}

# Same thing with collections.Counter (standard library)
from collections import Counter
print(Counter(text.split()))
```

### Exercise 1.B.11 — Sets: Deep Practice

```python
# Creating sets
a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}

# Set operations
print(f"Union:        {a | b}")        # {1, 2, 3, 4, 5, 6, 7, 8}
print(f"Intersection: {a & b}")        # {4, 5}
print(f"Difference:   {a - b}")        # {1, 2, 3}
print(f"Symmetric:    {a ^ b}")        # {1, 2, 3, 6, 7, 8}

# Membership test (very fast for sets)
print(3 in a)       # True
print(9 in a)       # False

# Remove duplicates from a list
data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique = list(set(data))
print(unique)       # [1, 2, 3, 4] (order may vary)

# Practical use: find common tags
user1_tags = {"python", "docker", "linux", "git"}
user2_tags = {"python", "javascript", "docker", "react"}
common = user1_tags & user2_tags
print(f"Common interests: {common}")   # {'docker', 'python'}
```

### Exercise 1.B.12 — Putting It All Together

```python
"""
Mini-project: Student Grade Analyzer

Given a list of students with their grades,
write functions to analyze the data.
"""

students = [
    {"name": "Alice", "grades": [85, 92, 78, 95]},
    {"name": "Bob", "grades": [70, 65, 82, 73]},
    {"name": "Charlie", "grades": [95, 98, 92, 97]},
    {"name": "Diana", "grades": [60, 55, 72, 68]},
    {"name": "Eve", "grades": [88, 91, 87, 93]},
]


def calculate_average(grades):
    """Calculate the average of a list of grades."""
    return sum(grades) / len(grades)


def get_letter_grade(average):
    """Convert a numeric average to a letter grade."""
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    return "F"


def analyze_students(students):
    """Analyze and print a report for all students."""
    print(f"{'Name':<12} {'Average':>8} {'Grade':>6}")
    print("-" * 28)
    
    averages = []
    for student in students:
        avg = calculate_average(student["grades"])
        grade = get_letter_grade(avg)
        averages.append(avg)
        print(f"{student['name']:<12} {avg:>8.1f} {grade:>6}")
    
    print("-" * 28)
    class_avg = sum(averages) / len(averages)
    print(f"{'Class avg':<12} {class_avg:>8.1f} {get_letter_grade(class_avg):>6}")
    
    # Find top student
    top = max(students, key=lambda s: calculate_average(s["grades"]))
    print(f"\nTop student: {top['name']} ({calculate_average(top['grades']):.1f})")


analyze_students(students)
```

**Expected output:**
```
Name          Average  Grade
----------------------------
Alice            87.5      B
Bob              72.5      C
Charlie          95.5      A
Diana            63.8      D
Eve              89.8      B
----------------------------
Class avg        81.8      B

Top student: Charlie (95.5)
```

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 1.C.1 — String Formatting Mastery

```python
# f-strings: the standard way
name, score = "Arun", 95.678

# Basic formatting
print(f"Name: {name}, Score: {score}")

# Number formatting
print(f"2 decimals:  {score:.2f}")        # 95.68
print(f"Percentage:  {score/100:.1%}")     # 95.7%
print(f"Padded:      {score:>10.2f}")      # "     95.68"
print(f"With commas: {1234567:,}")         # 1,234,567

# Alignment
for item, price in [("Coffee", 4.50), ("Sandwich", 8.99), ("Cake", 12.00)]:
    print(f"  {item:<12} ${price:>6.2f}")

# Debug mode (Python 3.8+)
x = 42
print(f"{x = }")              # x = 42
print(f"{x * 2 = }")          # x * 2 = 84
print(f"{type(x) = }")        # type(x) = <class 'int'>
```

### Exercise 1.C.2 — Advanced List Operations

```python
# zip — combine two lists element-wise
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

for name, score in zip(names, scores):
    print(f"{name}: {score}")

# Create a dict from two lists
grade_book = dict(zip(names, scores))
print(grade_book)   # {'Alice': 85, 'Bob': 92, 'Charlie': 78}

# map — apply a function to every element
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)      # [2, 4, 6, 8, 10]

# filter — keep elements that match a condition
evens = list(filter(lambda x: x % 2 == 0, range(20)))
print(evens)

# sorted with key function
words = ["banana", "Apple", "cherry", "date"]
print(sorted(words))                          # Case-sensitive
print(sorted(words, key=str.lower))           # Case-insensitive
print(sorted(words, key=len))                 # By length
print(sorted(words, key=len, reverse=True))   # Longest first

# any / all
numbers = [2, 4, 6, 8, 10]
print(all(n % 2 == 0 for n in numbers))    # True — all are even
print(any(n > 9 for n in numbers))          # True — at least one > 9
```

### Exercise 1.C.3 — Nested Data Structures

```python
"""
Work with complex nested data — a common pattern in real applications.
"""

# API-like response data
company = {
    "name": "TechCorp",
    "departments": [
        {
            "name": "Engineering",
            "employees": [
                {"name": "Alice", "role": "Senior Dev", "salary": 120000},
                {"name": "Bob", "role": "Junior Dev", "salary": 75000},
                {"name": "Charlie", "role": "DevOps", "salary": 110000},
            ],
        },
        {
            "name": "Marketing",
            "employees": [
                {"name": "Diana", "role": "Manager", "salary": 95000},
                {"name": "Eve", "role": "Analyst", "salary": 70000},
            ],
        },
    ],
}


# 1. Find all employee names
all_names = [
    emp["name"]
    for dept in company["departments"]
    for emp in dept["employees"]
]
print(f"All employees: {all_names}")


# 2. Total salary per department
for dept in company["departments"]:
    total = sum(emp["salary"] for emp in dept["employees"])
    avg = total / len(dept["employees"])
    print(f"{dept['name']}: total=${total:,}, avg=${avg:,.0f}")


# 3. Find highest paid employee
all_employees = [
    emp
    for dept in company["departments"]
    for emp in dept["employees"]
]
top_earner = max(all_employees, key=lambda e: e["salary"])
print(f"Highest paid: {top_earner['name']} (${top_earner['salary']:,})")
```

### Exercise 1.C.4 — Generators and Iterators

```python
# Generator function — produces values lazily (one at a time)
def fibonacci(limit):
    """Generate Fibonacci numbers up to limit."""
    a, b = 0, 1
    while a < limit:
        yield a
        a, b = b, a + b

# Use it
for num in fibonacci(100):
    print(num, end=" ")
print()
# 0 1 1 2 3 5 8 13 21 34 55 89

# Generator expression — like list comprehension but lazy
squares_gen = (x**2 for x in range(1000000))  # Uses almost no memory
first_ten = [next(squares_gen) for _ in range(10)]
print(first_ten)   # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]


# Practical: process large file line by line
def grep(pattern, filename):
    """Yield lines from a file that contain the pattern."""
    with open(filename) as f:
        for line_num, line in enumerate(f, 1):
            if pattern in line:
                yield line_num, line.rstrip()
```

### Exercise 1.C.5 — Unpacking and Advanced Assignment

```python
# Tuple unpacking
point = (3, 7)
x, y = point
print(f"x={x}, y={y}")

# Star unpacking
first, *middle, last = [1, 2, 3, 4, 5]
print(f"first={first}, middle={middle}, last={last}")
# first=1, middle=[2, 3, 4], last=5

# Swap without temp variable
a, b = 1, 2
a, b = b, a
print(f"a={a}, b={b}")   # a=2, b=1

# Dictionary unpacking
defaults = {"color": "blue", "size": "medium", "quantity": 1}
overrides = {"size": "large", "quantity": 5}
merged = {**defaults, **overrides}
print(merged)  # {'color': 'blue', 'size': 'large', 'quantity': 5}

# Walrus operator (:=) — assign and use in one expression
import random
data = [random.randint(1, 100) for _ in range(20)]
# Find first value > 90
if (big := next((x for x in data if x > 90), None)) is not None:
    print(f"Found big number: {big}")
else:
    print("No number > 90 found")
```

### Exercise 1.C.6 — Writing Clean Functions

```python
"""
Refactoring exercise: take messy code and make it clean.
"""

# MESSY VERSION — what NOT to do
def process(d):
    r = []
    for i in d:
        if i['a'] > 0:
            v = i['a'] * i['b']
            if v > 100:
                r.append({'n': i['n'], 'v': v, 't': 'high'})
            else:
                r.append({'n': i['n'], 'v': v, 't': 'low'})
    return r


# CLEAN VERSION — self-documenting
def classify_value(value, threshold=100):
    """Classify a value as 'high' or 'low' based on threshold."""
    return "high" if value > threshold else "low"


def calculate_product(item):
    """Calculate the product of quantity and price."""
    return item["quantity"] * item["price"]


def process_orders(orders, value_threshold=100):
    """
    Process orders and classify them by total value.
    
    Only includes orders with positive quantities.
    Returns list of dicts with name, value, and tier.
    """
    results = []
    for order in orders:
        if order["quantity"] <= 0:
            continue
        
        total_value = calculate_product(order)
        tier = classify_value(total_value, value_threshold)
        
        results.append({
            "name": order["name"],
            "value": total_value,
            "tier": tier,
        })
    
    return results


# Test both versions produce same results
test_data_messy = [
    {"n": "Widget", "a": 5, "b": 30},
    {"n": "Gadget", "a": 2, "b": 80},
    {"n": "Broken", "a": 0, "b": 50},
]

test_data_clean = [
    {"name": "Widget", "quantity": 5, "price": 30},
    {"name": "Gadget", "quantity": 2, "price": 80},
    {"name": "Broken", "quantity": 0, "price": 50},
]

print("Messy:", process(test_data_messy))
print("Clean:", process_orders(test_data_clean))
```

---

## PART D — ADVANCED DEBUG LAB

### Exercise 1.D.1 — Fix the Bugs

Each function has a bug. Find and fix it.

```python
# Bug 1: Off-by-one error
def get_last_n_items(lst, n):
    """Return the last n items from a list."""
    return lst[len(lst) - n:]  # Is this right? What if n > len(lst)?

# Test:
assert get_last_n_items([1, 2, 3, 4, 5], 3) == [3, 4, 5]
assert get_last_n_items([1, 2, 3], 5) == [1, 2, 3]    # Edge case!


# Bug 2: Mutable default argument
def add_item(item, items=[]):    # ← THE BUG IS HERE
    """Add an item to a list."""
    items.append(item)
    return items

# This looks correct but:
result1 = add_item("apple")
result2 = add_item("banana")
print(result1)    # Expected: ["apple"]        Actual: ["apple", "banana"] 😱
print(result2)    # Expected: ["banana"]        Actual: ["apple", "banana"] 😱

# Fix: use None as default
def add_item_fixed(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items


# Bug 3: Modifying list while iterating
def remove_evens(numbers):
    """Remove even numbers from a list."""
    for n in numbers:          # ← Modifying while iterating
        if n % 2 == 0:
            numbers.remove(n)
    return numbers

# This skips elements!
print(remove_evens([1, 2, 3, 4, 5, 6]))   # Expected: [1, 3, 5]  Actual: [1, 3, 5]? Maybe not!

# Fix: create a new list
def remove_evens_fixed(numbers):
    return [n for n in numbers if n % 2 != 0]


# Bug 4: Integer vs string comparison
def find_max_value(data):
    """Find the maximum value in a dict."""
    max_key = None
    max_val = float("-inf")
    for key, val in data.items():
        if val > max_val:       # What if val is a string "100"?
            max_val = val
            max_key = key
    return max_key, max_val

# Test with mixed types:
test = {"a": 10, "b": "100", "c": 50}
# This will crash or give wrong results — need type checking
```

### Exercise 1.D.2 — Trace the Execution

**Without running the code**, predict the output:

```python
# Puzzle 1
x = [1, 2, 3]
y = x
y.append(4)
print(x)
# Your answer: ___________
# Why: ___________________


# Puzzle 2
def modify(lst):
    lst = lst + [4]
    return lst

original = [1, 2, 3]
result = modify(original)
print(original)
print(result)
# Your answers: original = ___________
#               result   = ___________
# Why: ___________________


# Puzzle 3
def mystery(n, result=[]):
    result.append(n)
    return result

print(mystery(1))
print(mystery(2))
print(mystery(3))
# Your answers: ___________
# Why: ___________________


# Puzzle 4
items = [1, 2, 3, 4, 5]
for i in range(len(items)):
    items[i] *= 2
print(items)
# vs
items2 = [1, 2, 3, 4, 5]
for item in items2:
    item *= 2
print(items2)
# Are these the same? Why / why not?
```

<details>
<summary>Answers</summary>

```
Puzzle 1: [1, 2, 3, 4]
  → y = x makes y point to the SAME list. Appending via y modifies it.

Puzzle 2: original = [1, 2, 3], result = [1, 2, 3, 4]
  → lst + [4] creates a NEW list. The original is not modified.

Puzzle 3: [1], [1, 2], [1, 2, 3]
  → Mutable default argument. Same list is reused across calls.

Puzzle 4: [2, 4, 6, 8, 10] vs [1, 2, 3, 4, 5]
  → items[i] *= 2 modifies the list. for item in items2 creates a
    local variable; item *= 2 reassigns the local, not the list element.
```
</details>

### Exercise 1.D.3 — Refactor This Messy Code

```python
"""
TASK: This function works but is terrible. Refactor it.

Requirements:
- Same behavior, cleaner code
- Meaningful variable names
- No nesting deeper than 2 levels
- Add docstring
"""

def f(data):
    res = {}
    for d in data:
        if d['type'] == 'income':
            if d['category'] in res:
                res[d['category']] = res[d['category']] + d['amount']
            else:
                res[d['category']] = d['amount']
        else:
            if d['type'] == 'expense':
                if d['category'] in res:
                    res[d['category']] = res[d['category']] - d['amount']
                else:
                    res[d['category']] = -d['amount']
    return res

# Test data
transactions = [
    {"type": "income", "category": "salary", "amount": 5000},
    {"type": "expense", "category": "rent", "amount": 1500},
    {"type": "income", "category": "freelance", "amount": 800},
    {"type": "expense", "category": "food", "amount": 300},
    {"type": "income", "category": "salary", "amount": 5000},
    {"type": "expense", "category": "rent", "amount": 1500},
]

print(f(transactions))
```

<details>
<summary>Clean version</summary>

```python
from collections import defaultdict

def calculate_balances(transactions):
    """
    Calculate net balance per category from a list of transactions.
    
    Income adds to the balance, expenses subtract from it.
    Returns a dict of {category: net_balance}.
    """
    balances = defaultdict(float)
    
    for txn in transactions:
        amount = txn["amount"]
        if txn["type"] == "expense":
            amount = -amount
        
        balances[txn["category"]] += amount
    
    return dict(balances)
```
</details>

---

## PART E — PRODUCTION SIMULATION

### Scenario: Build a Command-Line Expense Tracker

**Task:** Build a complete, working expense tracker that runs in the terminal. This simulates writing a small real-world tool.

**Requirements:**
- Add expenses with a category and amount
- List all expenses, optionally filtered by category
- Show a summary: total spent, breakdown by category
- Data stored in a list (in-memory for now)
- Clean code: descriptive names, docstrings, functions that do one thing

```python
# expense_tracker.py

"""
Simple expense tracker — Version 1.0

Demonstrates: variables, loops, functions, lists, dicts, clean code.
"""

from datetime import datetime


def create_expense(amount, category, description=""):
    """Create an expense record."""
    return {
        "amount": round(float(amount), 2),
        "category": category.lower().strip(),
        "description": description,
        "date": datetime.now().isoformat(),
    }


def add_expense(expenses, amount, category, description=""):
    """Add a new expense to the list."""
    expense = create_expense(amount, category, description)
    expenses.append(expense)
    return expense


def get_total(expenses):
    """Calculate total of all expenses."""
    return sum(e["amount"] for e in expenses)


def get_by_category(expenses, category):
    """Filter expenses by category."""
    return [e for e in expenses if e["category"] == category.lower().strip()]


def get_summary(expenses):
    """Get spending summary grouped by category."""
    summary = {}
    for expense in expenses:
        cat = expense["category"]
        summary[cat] = summary.get(cat, 0) + expense["amount"]
    return dict(sorted(summary.items(), key=lambda x: x[1], reverse=True))


def format_currency(amount):
    """Format a number as currency."""
    return f"${amount:,.2f}"


def print_expenses(expenses):
    """Print a formatted table of expenses."""
    if not expenses:
        print("  No expenses found.")
        return
    
    print(f"  {'Date':<12} {'Category':<12} {'Amount':>10} {'Description'}")
    print(f"  {'-'*12} {'-'*12} {'-'*10} {'-'*20}")
    
    for exp in expenses:
        date_short = exp["date"][:10]
        print(
            f"  {date_short:<12} "
            f"{exp['category']:<12} "
            f"{format_currency(exp['amount']):>10} "
            f"{exp['description']}"
        )
    
    total = get_total(expenses)
    print(f"\n  Total: {format_currency(total)}")


def print_summary(expenses):
    """Print spending summary by category."""
    summary = get_summary(expenses)
    total = get_total(expenses)
    
    print(f"\n  Spending Summary")
    print(f"  {'Category':<15} {'Amount':>10} {'Percent':>8}")
    print(f"  {'-'*15} {'-'*10} {'-'*8}")
    
    for category, amount in summary.items():
        pct = (amount / total * 100) if total > 0 else 0
        print(f"  {category:<15} {format_currency(amount):>10} {pct:>7.1f}%")
    
    print(f"  {'-'*35}")
    print(f"  {'TOTAL':<15} {format_currency(total):>10}")


# --- Demo usage ---
if __name__ == "__main__":
    expenses = []
    
    # Add some expenses
    add_expense(expenses, 1500, "Rent", "Monthly rent")
    add_expense(expenses, 85.50, "Food", "Groceries")
    add_expense(expenses, 12.99, "Food", "Coffee beans")
    add_expense(expenses, 49.99, "Transport", "Monthly bus pass")
    add_expense(expenses, 120, "Utilities", "Electricity")
    add_expense(expenses, 45, "Food", "Restaurant dinner")
    add_expense(expenses, 9.99, "Entertainment", "Streaming service")
    add_expense(expenses, 200, "Savings", "Emergency fund")
    
    print("\n=== All Expenses ===")
    print_expenses(expenses)
    
    print("\n=== Food Only ===")
    print_expenses(get_by_category(expenses, "food"))
    
    print_summary(expenses)
```

**Run it:**
```bash
python expense_tracker.py
```

**Acceptance Criteria:**
- [ ] All functions have docstrings
- [ ] No function is longer than 15 lines
- [ ] Variable names are descriptive (no single letters except loop counters)
- [ ] The code runs without errors
- [ ] Output is neatly formatted and aligned
- [ ] Functions can be tested independently (no global state)

---

## Key Takeaways

1. **Variables are labels, not boxes.** They point to objects in memory. Two variables can point to the same object.
2. **Lists are ordered and mutable.** Use them when order matters. Use list comprehensions for clean transformations.
3. **Dicts are for lookup.** When you need to find something by key, use a dictionary. `.get()` is safer than `[]`.
4. **Sets are for uniqueness and fast membership tests.** Use them when you need to check "is X in this collection?"
5. **Functions should do one thing.** If you can't describe it in one sentence, it's doing too much.
6. **Clean code saves time.** Spending 2 extra minutes naming things well saves 20 minutes debugging later.

---

*Next: [Section 2 — Core Python Skills](02-core-python-skills.md)*
