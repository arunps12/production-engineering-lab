# SECTION 3 — DEBUGGING (SUPERPOWER) 🔍

---

## PART A — CONCEPT EXPLANATION

### Why Debugging is a Superpower

Every developer writes bugs. The difference between a junior and a senior is **how fast they find and fix them.**

```
Junior:  "It doesn't work" → changes random things → hopes it works
Senior:  "It doesn't work" → reads the error → forms hypothesis → tests it → fixes it
```

**Debugging is a systematic skill.** It's not about intuition or luck — it's about a structured process:

1. **Reproduce** — can you make the bug happen consistently?
2. **Isolate** — which part of the code is responsible?
3. **Understand** — why does the code behave this way?
4. **Fix** — change the minimum amount of code to fix it
5. **Verify** — does the fix work? Did it break anything else?

### Reading Stack Traces

A **stack trace** (or traceback) is Python's error report. It tells you exactly what went wrong and where.

```
Traceback (most recent call last):
  File "main.py", line 15, in <module>      ← 3. Started here
    result = process_data(raw_data)
  File "main.py", line 10, in process_data  ← 2. Called this function
    return transform(data["key"])
  File "main.py", line 5, in transform      ← 1. Which called this
    return value.upper()
AttributeError: 'int' object has no attribute 'upper'
                 ↑                              ↑
              What type                    What you tried to do
```

**How to read a stack trace:**
1. **Start at the BOTTOM** — the last line tells you the error type and message
2. **Look at the last file/line** — that's where the error occurred
3. **Walk UP** — the call chain shows you how you got there
4. The error message tells you **what** went wrong; the stack trace tells you **where**

**Common Python exceptions and what they mean:**

| Exception | Meaning | Typical cause |
|-----------|---------|---------------|
| `NameError` | Variable doesn't exist | Typo in variable name, forgot to define it |
| `TypeError` | Wrong type for operation | Passing string where int expected, calling non-callable |
| `ValueError` | Right type, wrong value | `int("hello")`, index out of logical range |
| `KeyError` | Dict key doesn't exist | Accessing `d["missing_key"]` |
| `IndexError` | List index out of range | `lst[10]` when list has 5 items |
| `AttributeError` | Object doesn't have that attribute | Calling `.append()` on a string, typo in method name |
| `FileNotFoundError` | File doesn't exist | Wrong path, wrong directory |
| `ImportError` | Can't import module | Not installed, wrong name, circular import |
| `IndentationError` | Bad indentation | Mixed tabs/spaces, wrong nesting |
| `RecursionError` | Too many recursive calls | Missing base case, infinite recursion |

### Tracing Variables

**Variable tracing** means tracking the value of variables at each step of execution. This is the most effective debugging technique.

```python
# Something is wrong — expected output but got different result
def calculate_discount(price, discount_percent, tax_rate):
    discounted = price - (price * discount_percent)     # Bug: discount_percent should be / 100
    total = discounted + (discounted * tax_rate)
    return total

result = calculate_discount(100, 20, 0.08)
print(result)   # Expected: ~86.40, Got: -2052.0
```

**Trace it step by step:**
```
price = 100
discount_percent = 20

Step 1: discounted = 100 - (100 * 20) = 100 - 2000 = -1900   ← FOUND IT!
        Should be: 100 - (100 * 20/100) = 100 - 20 = 80

Step 2: total = -1900 + (-1900 * 0.08) = -1900 + (-152) = -2052
```

**The fix:**
```python
discounted = price * (1 - discount_percent / 100)
```

### Methods of Debugging

**1. Print debugging** — simple but effective:
```python
def process(data):
    print(f"DEBUG: data = {data}, type = {type(data)}")  # Add temporarily
    result = transform(data)
    print(f"DEBUG: result = {result}")                    # Check intermediate values
    return result
```

**2. Assert statements** — catch bugs early:
```python
def divide(a, b):
    assert b != 0, f"Divisor cannot be zero (got b={b})"
    assert isinstance(a, (int, float)), f"Expected number, got {type(a)}"
    return a / b
```

**3. Python debugger (pdb)** — step through code interactively:
```python
def complex_function(data):
    import pdb; pdb.set_trace()   # Execution stops here
    # or: breakpoint()            # Python 3.7+ shortcut
    
    result = []
    for item in data:
        processed = transform(item)
        result.append(processed)
    return result
```

**pdb commands:**
| Command | Action |
|---------|--------|
| `n` (next) | Execute next line |
| `s` (step) | Step into function call |
| `c` (continue) | Continue to next breakpoint |
| `p expr` | Print expression value |
| `l` (list) | Show current code |
| `w` (where) | Show call stack |
| `q` (quit) | Exit debugger |

**4. Logging** — better than print for production:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def process(data):
    logger.debug("Processing data: %s", data)
    result = transform(data)
    logger.info("Processed successfully: %d items", len(result))
    return result
```

### Fixing Logic Errors

**Logic errors** are the hardest bugs: the code runs without errors but produces wrong results.

```python
# Bug: supposed to return True if ALL items are positive
def all_positive(numbers):
    for n in numbers:
        if n > 0:
            return True     # BUG: returns True on FIRST positive number
    return False

print(all_positive([5, -1, 3]))   # Returns True but should return False
```

**Debugging process:**
1. **What did I expect?** `all_positive([5, -1, 3])` should return `False`
2. **What happened?** It returned `True`
3. **Trace the execution:**
   - `n = 5` → `5 > 0` → `return True` (stops here, never checks -1)
4. **Root cause:** Logic is inverted — should return `False` on first negative

```python
# Fixed: return False on first non-positive, True only after checking all
def all_positive(numbers):
    for n in numbers:
        if n <= 0:
            return False
    return True

# Or simply:
def all_positive(numbers):
    return all(n > 0 for n in numbers)
```

### Refactoring Messy Code

**Refactoring** means restructuring code without changing its behavior. You refactor to make code easier to understand, test, and modify.

**When to refactor:**
- You can't understand the code after 30 seconds
- A function does more than one thing
- You copied-and-pasted code (DRY violation)
- Variable names don't explain their purpose
- Nesting is deeper than 3 levels

**Common beginner misunderstandings:**

| Mistake | Reality |
|---------|---------|
| "Debugging is for bad programmers" | Debugging is the #1 skill that separates engineers from coders |
| "I'll just read the code to find the bug" | Reading works for simple bugs. Systematic tracing works for all bugs |
| "Print debugging is unprofessional" | It's the fastest technique for 80% of bugs. Use it |
| "I need a fancy debugger" | `print()`, `assert`, and `pdb` solve 95% of debugging needs |
| "I'll fix it by rewriting everything" | Understand the bug first. The smallest fix is usually the best one |
| "Tests prevent all bugs" | Tests catch regressions. They don't catch logic errors in the test itself |

---

## PART B — BEGINNER PRACTICE

### Exercise 3.B.1 — Read These Stack Traces

**For each error, answer: (1) What type of error? (2) Which line? (3) What caused it?**

```python
# Error 1:
"""
Traceback (most recent call last):
  File "app.py", line 8, in <module>
    greet(user_name)
  File "app.py", line 3, in greet
    print("Hello, " + name.upper())
AttributeError: 'NoneType' object has no attribute 'upper'
"""
# Your answer:
# Type: _________________
# Line: _________________
# Cause: ________________


# Error 2:
"""
Traceback (most recent call last):
  File "data.py", line 12, in <module>
    result = process_records(records)
  File "data.py", line 7, in process_records
    total += record["amount"]
KeyError: 'amount'
"""
# Your answer:
# Type: _________________
# Line: _________________
# Cause: ________________


# Error 3:
"""
Traceback (most recent call last):
  File "calc.py", line 15, in <module>
    average = calculate_average([])
  File "calc.py", line 5, in calculate_average
    return sum(numbers) / len(numbers)
ZeroDivisionError: division by zero
"""
# Your answer:
# Type: _________________
# Line: _________________
# Cause: ________________
```

<details>
<summary>Answers</summary>

```
Error 1: AttributeError, line 3 in greet function.
  Cause: name is None (user_name was None). .upper() doesn't work on None.

Error 2: KeyError, line 7 in process_records.
  Cause: A record dict doesn't have an "amount" key. Maybe typo or missing data.

Error 3: ZeroDivisionError, line 5 in calculate_average.
  Cause: Empty list passed in → len([]) is 0 → division by zero.
```
</details>

### Exercise 3.B.2 — Fix These Bugs (One Bug Each)

```python
# Bug 1: Expected "HELLO WORLD", got an error
def shout(text):
    return text.Upper()

# Fix: ___________________


# Bug 2: Expected [2, 4, 6, 8], got [1, 2, 3, 4]
def double_all(numbers):
    result = []
    for n in numbers:
        result.append(n)
    return result

print(double_all([1, 2, 3, 4]))
# Fix: ___________________


# Bug 3: Expected True, got False
def is_palindrome(text):
    return text == text[::-1]

print(is_palindrome("Racecar"))   # False — but "Racecar" IS a palindrome!
# Fix: ___________________


# Bug 4: Expected 120, got RecursionError
def factorial(n):
    return n * factorial(n - 1)

# Fix: ___________________


# Bug 5: Expected {"a": 1, "b": 2}, got {"a": 1}
def merge_dicts(dict1, dict2):
    result = dict1
    result.update(dict2)
    return result

d1 = {"a": 1}
d2 = {"b": 2}
merged = merge_dicts(d1, d2)
print(d1)      # {"a": 1, "b": 2} — d1 was modified!
# Fix: ___________________
```

<details>
<summary>Fixes</summary>

```python
# 1: .Upper() → .upper() (case-sensitive method name)
# 2: result.append(n) → result.append(n * 2) (forgot to double)
# 3: Compare lowercase: text.lower() == text.lower()[::-1]
# 4: Missing base case: if n <= 1: return 1
# 5: result = dict1 makes result point to SAME dict. Fix: result = dict1.copy()
```
</details>

### Exercise 3.B.3 — Print Debugging

```python
"""
This function should return the longest word in a sentence.
It has a bug. Use print statements to find it.
"""

def find_longest_word(sentence):
    words = sentence.split()
    longest = ""
    
    for word in words:
        if len(word) > len(longest):
            longest = word
    
    return longest


# Test 1: Works
print(find_longest_word("the quick brown fox"))  # "quick" ← but wait, "brown" is also 5 letters

# Test 2: Bug appears
print(find_longest_word("I love programming"))   # Expected: "programming", Got: ?

# Test 3: Edge case
print(find_longest_word(""))                      # Expected: "" — does it crash?

# Task: Add print statements inside the function to trace the bug.
# Specifically, print the word and its length at each iteration.
```

### Exercise 3.B.4 — Assert-Based Debugging

```python
"""
Add assert statements to catch bugs early.
"""

def create_user(name, age, email):
    """Create a user dict with validation via asserts."""
    assert isinstance(name, str), f"name must be str, got {type(name)}"
    assert len(name.strip()) > 0, "name cannot be empty"
    assert isinstance(age, int), f"age must be int, got {type(age)}"
    assert 0 <= age <= 150, f"age must be 0-150, got {age}"
    assert "@" in email, f"email must contain @, got {email}"
    
    return {"name": name.strip(), "age": age, "email": email.lower()}


# These should work:
print(create_user("Arun", 25, "arun@example.com"))

# These should trigger asserts (uncomment one at a time):
# create_user("", 25, "arun@example.com")       # Empty name
# create_user("Arun", -5, "arun@example.com")   # Negative age
# create_user("Arun", 25, "invalid-email")       # No @
# create_user(123, 25, "arun@example.com")        # Wrong type
```

### Exercise 3.B.5 — Use pdb to Step Through Code

```python
"""
Use the Python debugger to step through this function.
"""

def mystery_math(numbers):
    """What does this function actually do?"""
    if not numbers:
        return 0
    
    breakpoint()  # Debugger will stop here
    
    result = numbers[0]
    for i in range(1, len(numbers)):
        if numbers[i] > result:
            result = numbers[i]
    return result


# Run this and use pdb commands:
# n  — step to next line
# p result — print the current value of result
# p numbers[i] — print the current element
# c — continue to the end

print(mystery_math([3, 7, 1, 9, 4]))

# Questions:
# 1. What does this function compute?
# 2. There's already a built-in for this — what is it?
# 3. What happens with an empty list?
```

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 3.C.1 — Multi-Bug Function

```python
"""
This function has 5 bugs. Find and fix ALL of them.
"""

def analyze_scores(students):
    """
    Given a list of {"name": str, "scores": [int]},
    return a sorted list of {"name": str, "average": float, "grade": str}.
    """
    results = []
    
    for student in students:
        total = 0
        for score in student["scores"]:
            total += score
        average = total / len(student)          # Bug 1
        
        if average >= 90:
            grade = "A"
        elif average >= 80:
            grade == "B"                         # Bug 2
        elif average >= 70:
            grade = "C"
        elif average >= 60:
            grade = "d"                          # Bug 3 (inconsistent case)
        else:
            grade = "F"
        
        results.append({
            "name": student["name"],
            "average": average,
            "grade": grade,
        })
    
    results.sort(key=lambda s: s["average"])     # Bug 4 (should be descending)
    return results


# Test data
students = [
    {"name": "Alice", "scores": [85, 92, 78, 95]},
    {"name": "Bob", "scores": [65, 72, 58, 70]},
    {"name": "Charlie", "scores": [95, 98, 92, 100]},
    {"name": "Diana", "scores": [45, 52, 38, 50]},
]

# Expected output (sorted by average, highest first):
# Charlie: 96.3 (A)
# Alice: 87.5 (B)
# Bob: 66.3 (D)
# Diana: 46.3 (F)

for student in analyze_scores(students):
    print(f"{student['name']}: {student['average']:.1f} ({student['grade']})")
```

<details>
<summary>All 5 bugs</summary>

```
Bug 1: len(student) → len(student["scores"])  — dividing by number of KEYS, not scores
Bug 2: grade == "B" → grade = "B"  — comparison instead of assignment
Bug 3: grade = "d" → grade = "D"  — inconsistent capitalization
Bug 4: Missing reverse=True in sort  — should be highest first
Bug 5: (hidden) What if student["scores"] is empty? Division by zero. Add a check.
```
</details>

### Exercise 3.C.2 — Logic Error Investigation

```python
"""
This shopping cart has a logic error in the discount calculation.
Customers are complaining about wrong prices.

Debug systematically: add prints, trace values, find the root cause.
"""

class ShoppingCart:
    def __init__(self):
        self.items = []
    
    def add_item(self, name, price, quantity=1):
        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity,
        })
    
    def subtotal(self):
        return sum(item["price"] * item["quantity"] for item in self.items)
    
    def apply_discount(self, percent):
        """Apply a percentage discount to all items."""
        for item in self.items:
            item["price"] = item["price"] * (1 - percent / 100)
    
    def total(self):
        return self.subtotal()


# Scenario: Customer adds items, applies 10% coupon, then 5% coupon
cart = ShoppingCart()
cart.add_item("Laptop", 1000, 1)
cart.add_item("Mouse", 50, 2)

print(f"Subtotal: ${cart.subtotal():.2f}")     # $1100.00

cart.apply_discount(10)                          # 10% off
print(f"After 10% off: ${cart.total():.2f}")    # $990.00

cart.apply_discount(5)                           # Additional 5% off
print(f"After 5% off: ${cart.total():.2f}")     # Expected: ~$940.50? Or $907.50?

# Bug: apply_discount MUTATES the prices permanently.
# So the second discount is applied to already-discounted prices.
# Is this the intended behavior? If "15% total discount" was intended, it's wrong.

# Fix options:
# A) Store original prices and calculate discount from original
# B) Document that discounts stack multiplicatively (this may be correct!)
# C) Apply discount to subtotal, not individual items
```

### Exercise 3.C.3 — Debugging with Logging

```python
"""
Replace print debugging with proper logging.
This function processes transactions and has intermittent bugs.
"""

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("transactions")


def process_transactions(transactions):
    """Process a list of financial transactions."""
    balances = {}
    errors = []
    
    for i, txn in enumerate(transactions):
        logger.debug("Processing transaction %d: %s", i, txn)
        
        try:
            account = txn["account"]
            amount = float(txn["amount"])
            txn_type = txn["type"]
        except (KeyError, ValueError) as e:
            logger.warning("Skipping invalid transaction %d: %s", i, e)
            errors.append({"index": i, "error": str(e)})
            continue
        
        if account not in balances:
            balances[account] = 0.0
            logger.info("New account: %s", account)
        
        if txn_type == "credit":
            balances[account] += amount
            logger.debug("Credited %s: +%.2f → %.2f", account, amount, balances[account])
        elif txn_type == "debit":
            if balances[account] >= amount:
                balances[account] -= amount
                logger.debug("Debited %s: -%.2f → %.2f", account, amount, balances[account])
            else:
                logger.error(
                    "Insufficient funds for %s: balance=%.2f, debit=%.2f",
                    account, balances[account], amount,
                )
                errors.append({"index": i, "error": "insufficient funds"})
        else:
            logger.warning("Unknown transaction type: %s", txn_type)
            errors.append({"index": i, "error": f"unknown type: {txn_type}"})
    
    logger.info("Processing complete. %d accounts, %d errors", len(balances), len(errors))
    return balances, errors


# Test with some good and bad data
transactions = [
    {"account": "ACC001", "amount": "1000", "type": "credit"},
    {"account": "ACC001", "amount": "500", "type": "debit"},
    {"account": "ACC002", "amount": "2000", "type": "credit"},
    {"account": "ACC001", "amount": "invalid", "type": "credit"},  # Bad amount
    {"account": "ACC001", "amount": "600", "type": "debit"},       # Insufficient funds
    {"type": "credit", "amount": "100"},                            # Missing account
    {"account": "ACC002", "amount": "100", "type": "transfer"},    # Unknown type
]

balances, errors = process_transactions(transactions)
print(f"\nFinal balances: {balances}")
print(f"Errors: {errors}")
```

### Exercise 3.C.4 — Refactoring: Extract Functions

```python
"""
BEFORE: One massive function that does too many things.
TASK: Refactor into clean, focused functions.
"""

# MESSY — one huge function
def generate_report(sales_data):
    # Validate
    if not sales_data:
        print("No data!")
        return
    for item in sales_data:
        if "product" not in item or "amount" not in item or "date" not in item:
            print(f"Invalid item: {item}")
            return
    
    # Calculate totals by product
    totals = {}
    for item in sales_data:
        p = item["product"]
        if p in totals:
            totals[p] = totals[p] + item["amount"]
        else:
            totals[p] = item["amount"]
    
    # Calculate totals by month
    monthly = {}
    for item in sales_data:
        m = item["date"][:7]  # "2024-01" from "2024-01-15"
        if m in monthly:
            monthly[m] = monthly[m] + item["amount"]
        else:
            monthly[m] = item["amount"]
    
    # Find best and worst
    best_product = max(totals, key=totals.get)
    worst_product = min(totals, key=totals.get)
    
    # Print report
    print("=" * 40)
    print("SALES REPORT")
    print("=" * 40)
    print("\nBy Product:")
    for p, total in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        print(f"  {p:<15} ${total:>10,.2f}")
    print(f"\nBest:  {best_product} (${totals[best_product]:,.2f})")
    print(f"Worst: {worst_product} (${totals[worst_product]:,.2f})")
    print("\nBy Month:")
    for m, total in sorted(monthly.items()):
        print(f"  {m:<10} ${total:>10,.2f}")
    print(f"\nGrand Total: ${sum(totals.values()):,.2f}")
    print("=" * 40)


# TASK: Refactor into these functions:
# - validate_sales_data(data) → bool
# - group_by(data, key_func) → dict
# - format_currency(amount) → str
# - print_sales_report(product_totals, monthly_totals)
```

<details>
<summary>Clean version</summary>

```python
from collections import defaultdict


def validate_sales_data(data):
    """Validate that all items have required fields. Returns list of errors."""
    required = {"product", "amount", "date"}
    errors = []
    for i, item in enumerate(data):
        missing = required - set(item.keys())
        if missing:
            errors.append(f"Item {i}: missing {missing}")
    return errors


def group_by_sum(data, key_func):
    """Group items and sum their amounts by a key function."""
    groups = defaultdict(float)
    for item in data:
        groups[key_func(item)] += item["amount"]
    return dict(groups)


def format_currency(amount):
    return f"${amount:>10,.2f}"


def print_section(title, data, sort_by_value=True):
    """Print a section of the report."""
    print(f"\n{title}:")
    items = sorted(data.items(), key=lambda x: x[1], reverse=sort_by_value)
    for key, value in items:
        print(f"  {key:<15} {format_currency(value)}")


def generate_report(sales_data):
    """Generate a formatted sales report."""
    if not sales_data:
        print("No data!")
        return

    errors = validate_sales_data(sales_data)
    if errors:
        for err in errors:
            print(f"Validation error: {err}")
        return

    product_totals = group_by_sum(sales_data, lambda x: x["product"])
    monthly_totals = group_by_sum(sales_data, lambda x: x["date"][:7])

    print("=" * 40)
    print("SALES REPORT")
    print("=" * 40)

    print_section("By Product", product_totals)

    best = max(product_totals, key=product_totals.get)
    worst = min(product_totals, key=product_totals.get)
    print(f"\nBest:  {best} ({format_currency(product_totals[best])})")
    print(f"Worst: {worst} ({format_currency(product_totals[worst])})")

    print_section("By Month", monthly_totals, sort_by_value=False)

    print(f"\nGrand Total: {format_currency(sum(product_totals.values()))}")
    print("=" * 40)
```
</details>

### Exercise 3.C.5 — Recursive Bug Hunting

```python
"""
These recursive functions have bugs. Fix each one.
"""

# Bug 1: Infinite recursion
def flatten(nested_list):
    """Flatten a nested list: [1, [2, [3, 4]], 5] → [1, 2, 3, 4, 5]"""
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

# Test:
print(flatten([1, [2, [3, 4]], 5]))     # Should work
# print(flatten([1, [2, [3, [4, [5]]]]]))  # Should work too


# Bug 2: Wrong result
def binary_search(sorted_list, target, low=0, high=None):
    """Find target in sorted list, return index or -1."""
    if high is None:
        high = len(sorted_list) - 1
    
    if low > high:
        return -1
    
    mid = (low + high) // 2
    
    if sorted_list[mid] == target:
        return mid
    elif sorted_list[mid] < target:
        return binary_search(sorted_list, target, mid, high)     # BUG
    else:
        return binary_search(sorted_list, target, low, mid)      # BUG

# Test:
data = [1, 3, 5, 7, 9, 11, 13, 15]
print(binary_search(data, 7))     # Should return 3
print(binary_search(data, 4))     # Should return -1
# Hint: the bug causes infinite recursion for some inputs
```

<details>
<summary>Fixes</summary>

```python
# Bug 2 fix:
# mid, high → mid + 1, high  (left half must exclude mid)
# low, mid → low, mid - 1    (right half must exclude mid)
# Without these, when low == mid (adjacent elements), you infinitely recurse.
```
</details>

---

## PART D — ADVANCED DEBUG LAB

### Exercise 3.D.1 — Debug a Real-World Data Pipeline

```python
"""
This data pipeline processes user events. It has 3 subtle bugs
that only appear with certain data patterns.

Run it and find the bugs.
"""

from datetime import datetime, timedelta
import random


def generate_events(n=100):
    """Generate sample user events."""
    users = ["user_1", "user_2", "user_3", "user_4", "user_5"]
    actions = ["login", "view", "click", "purchase", "logout"]
    events = []
    
    base_time = datetime(2024, 1, 1)
    for i in range(n):
        event = {
            "user_id": random.choice(users),
            "action": random.choice(actions),
            "timestamp": (base_time + timedelta(minutes=i * 5)).isoformat(),
            "metadata": {},
        }
        if event["action"] == "purchase":
            event["metadata"]["amount"] = round(random.uniform(10, 500), 2)
        if event["action"] == "view":
            event["metadata"]["page"] = random.choice(["/home", "/products", "/cart"])
        events.append(event)
    
    # Add some edge cases
    events.append({"user_id": "user_1", "action": "purchase", "timestamp": "2024-01-05T10:00:00"})  # Missing metadata
    events.append({"user_id": None, "action": "login", "timestamp": "2024-01-05T11:00:00", "metadata": {}})  # Null user
    
    return events


def analyze_events(events):
    """Analyze user events and produce a summary."""
    
    # Count actions per user
    user_actions = {}
    for event in events:
        user = event["user_id"]
        action = event["action"]
        
        if user not in user_actions:
            user_actions[user] = {}
        
        if action not in user_actions[user]:
            user_actions[user][action] = 0
        
        user_actions[user][action] += 1
    
    # Calculate total revenue
    total_revenue = 0
    for event in events:
        if event["action"] == "purchase":
            total_revenue += event["metadata"]["amount"]    # Bug: KeyError if no metadata or no amount
    
    # Find most active user
    activity_counts = {}
    for user, actions in user_actions.items():
        activity_counts[user] = sum(actions.values())
    
    most_active = max(activity_counts, key=activity_counts.get)
    
    return {
        "total_events": len(events),
        "unique_users": len(user_actions),
        "total_revenue": total_revenue,
        "most_active_user": most_active,
        "user_actions": user_actions,
    }


# Run and debug
random.seed(42)
events = generate_events(50)
try:
    summary = analyze_events(events)
    print(f"Total events: {summary['total_events']}")
    print(f"Unique users: {summary['unique_users']}")
    print(f"Revenue: ${summary['total_revenue']:.2f}")
    print(f"Most active: {summary['most_active_user']}")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    print("Debug this! What went wrong?")
```

### Exercise 3.D.2 — Performance Debugging

```python
"""
This code works correctly but is extremely slow for large inputs.
Profile it and optimize it.
"""

import time


def find_duplicates_slow(data):
    """Find duplicate items in a list. SLOW version."""
    duplicates = []
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i] == data[j] and data[i] not in duplicates:
                duplicates.append(data[i])
    return duplicates


def find_duplicates_fast(data):
    """Find duplicate items in a list. FAST version."""
    seen = set()
    duplicates = set()
    for item in data:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)


# Benchmark
sizes = [100, 1000, 5000]
for size in sizes:
    data = [i % (size // 2) for i in range(size)]  # 50% duplicates
    
    start = time.perf_counter()
    result_slow = find_duplicates_slow(data)
    slow_time = time.perf_counter() - start
    
    start = time.perf_counter()
    result_fast = find_duplicates_fast(data)
    fast_time = time.perf_counter() - start
    
    speedup = slow_time / fast_time if fast_time > 0 else float("inf")
    print(f"n={size:>5}: slow={slow_time:.4f}s, fast={fast_time:.6f}s, speedup={speedup:.0f}x")

# Why is the slow version slow?
# 1. O(n²) nested loop
# 2. "not in duplicates" is O(n) on a list
# 3. Total: O(n³)
#
# The fast version is O(n) — sets have O(1) lookup
```

### Exercise 3.D.3 — Debugging Imports

```python
"""
Common import errors and how to fix them.
"""

# Error 1: ModuleNotFoundError
# >>> import pandas
# ModuleNotFoundError: No module named 'pandas'
# Fix: pip install pandas (or uv add pandas)

# Error 2: ImportError
# >>> from collections import OrderedDict, DefaultDict
# ImportError: cannot import name 'DefaultDict'
# Fix: It's 'defaultdict' (lowercase d). Python is case-sensitive.

# Error 3: Circular import
# file_a.py: from file_b import func_b
# file_b.py: from file_a import func_a
# → ImportError: cannot import name 'func_a' from partially initialized module
# Fix: restructure code, or use lazy imports (import inside function)

# Error 4: Relative import confusion
# from .utils import helper   ← Only works inside a package
# Fix: Use absolute imports in scripts, relative in packages


# Debugging imports:
import sys

# Check where Python looks for modules:
for path in sys.path:
    print(path)

# Check if a module is installed:
try:
    import requests
    print(f"requests version: {requests.__version__}")
    print(f"Location: {requests.__file__}")
except ImportError:
    print("requests is NOT installed")
```

---

## PART E — PRODUCTION SIMULATION

### Scenario: Debug a "Working" but Wrong Application

**Your task:** You receive a bug report from a user of the expense tracker (from Section 1). The report says:

> "When I add expenses and then look at the summary, the percentages don't add up to 100%. Sometimes the total is wrong too. Also, it crashes when I have no expenses."

Your job is to:
1. Write test cases that reproduce the bugs
2. Fix each bug
3. Add defensive code so these bugs can't happen again

```python
"""
Buggy expense tracker — find and fix the issues.
"""


# BUG REPRODUCTION:
def test_empty_expenses():
    """Bug: crashes with empty list."""
    expenses = []
    try:
        total = sum(e["amount"] for e in expenses)
        avg = total / len(expenses)   # ZeroDivisionError!
    except ZeroDivisionError:
        print("✗ Bug confirmed: crashes on empty expenses")


def test_percentage_sum():
    """Bug: percentages don't sum to 100%."""
    expenses = [
        {"amount": 10.0, "category": "food"},
        {"amount": 10.0, "category": "food"},
        {"amount": 10.0, "category": "transport"},
    ]
    total = sum(e["amount"] for e in expenses)  # 30.0
    
    categories = {}
    for e in expenses:
        categories[e["category"]] = categories.get(e["category"], 0) + e["amount"]
    
    # Check percentages
    pct_sum = 0
    for cat, amount in categories.items():
        pct = round(amount / total * 100)    # Rounding can cause total != 100
        pct_sum += pct
        print(f"  {cat}: {pct}%")
    
    print(f"  Sum: {pct_sum}%")
    if pct_sum != 100:
        print("  ✗ Bug confirmed: percentages don't sum to 100%")


def test_floating_point():
    """Bug: floating point causes wrong total."""
    expenses = [
        {"amount": 0.1, "category": "a"},
        {"amount": 0.2, "category": "b"},
    ]
    total = sum(e["amount"] for e in expenses)
    print(f"  0.1 + 0.2 = {total}")           # 0.30000000000000004
    print(f"  total == 0.3? {total == 0.3}")   # False!
    
    # Fix: use round() for display, or decimal.Decimal for exact math
    from decimal import Decimal
    exact_total = Decimal("0.1") + Decimal("0.2")
    print(f"  Decimal: {exact_total}")         # 0.3


# Run bug reproductions:
print("=== Test 1: Empty expenses ===")
test_empty_expenses()

print("\n=== Test 2: Percentage sum ===")
test_percentage_sum()

print("\n=== Test 3: Floating point ===")
test_floating_point()

print("\n=== Fixes ===")
print("""
Fix 1: Check for empty list before dividing:
    if not expenses:
        return {"total": 0, "categories": {}}

Fix 2: Use the largest remainder method for percentages,
    or simply show one decimal place.

Fix 3: Use round(total, 2) for currency, or Decimal for exact math.
    Never compare floats with ==.
""")
```

**Acceptance Criteria:**
- [ ] You can identify at least 3 bugs from the bug report
- [ ] Each bug has a test that reproduces it
- [ ] Each bug has a fix
- [ ] You added defensive code (checks for empty data, type validation)
- [ ] The fixes don't break existing working behavior

---

## Key Takeaways

1. **Read stack traces bottom-up.** The error type and message are at the bottom. The location is in the last file/line before the error.
2. **Trace variables step by step.** Don't guess — actually write down what each variable is at each step.
3. **Print debugging is not shameful.** It's the fastest technique for most bugs.
4. **Logic errors need test cases.** If it "works but gives wrong results," write a test with known expected output.
5. **Refactor after debugging.** If the bug was hard to find, the code is probably too complex. Simplify it.
6. **Debugging is systematic, not magical.** Reproduce → Isolate → Understand → Fix → Verify.

---

*Next: [Section 4 — Data & APIs](04-data-and-apis.md)*
