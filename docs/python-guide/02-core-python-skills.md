# SECTION 2 — CORE PYTHON SKILLS

---

## PART A — CONCEPT EXPLANATION

### Object-Oriented Programming (OOP)

**OOP** organizes code around **objects** — bundles of data (attributes) and behavior (methods) that model real-world things.

**Mental model:** Think of a class as a blueprint and an object as a house built from that blueprint. You can build many houses from one blueprint, and each house has its own address, color, and contents — but they all share the same structure.

```python
# Blueprint (class)
class Dog:
    def __init__(self, name, breed):
        self.name = name        # attribute (data)
        self.breed = breed      # attribute (data)
    
    def bark(self):             # method (behavior)
        return f"{self.name} says Woof!"

# Objects (instances)
rex = Dog("Rex", "German Shepherd")
luna = Dog("Luna", "Labrador")

print(rex.bark())    # "Rex says Woof!"
print(luna.bark())   # "Luna says Woof!"
```

### The Four Pillars of OOP

**1. Encapsulation** — Bundle data and methods together. Hide internal details.
```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance     # Convention: _ means "internal"
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount
    
    def get_balance(self):
        return self._balance

# Users interact through methods, not raw data
account = BankAccount("Arun", 1000)
account.deposit(500)
print(account.get_balance())   # 1500
# account._balance = -999     ← NOT the intended way (but Python allows it)
```

**2. Inheritance** — Create specialized classes from general ones.
```python
class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound
    
    def speak(self):
        return f"{self.name} says {self.sound}"

class Dog(Animal):
    def __init__(self, name):
        super().__init__(name, "Woof")
    
    def fetch(self):
        return f"{self.name} fetches the ball!"

class Cat(Animal):
    def __init__(self, name):
        super().__init__(name, "Meow")

dog = Dog("Rex")
cat = Cat("Whiskers")
print(dog.speak())      # "Rex says Woof"
print(dog.fetch())      # "Rex fetches the ball!"
print(cat.speak())      # "Whiskers says Meow"
```

**3. Polymorphism** — Different objects respond to the same interface differently.
```python
animals = [Dog("Rex"), Cat("Whiskers"), Dog("Luna")]
for animal in animals:
    print(animal.speak())   # Each calls its own version of speak()
```

**4. Abstraction** — Expose simple interfaces, hide complex implementation.
```python
# You don't need to know HOW a list sorts — you just call .sort()
numbers = [3, 1, 4, 1, 5, 9]
numbers.sort()   # Abstraction: complex sorting algorithm hidden behind one method
```

### When to Use OOP vs Functions

| Situation | Use | Why |
|-----------|-----|-----|
| Stateless transformation | Function | No state to manage |
| Group of related data + operations | Class | Keeps data and behavior together |
| Need multiple instances with same behavior | Class | Each instance has its own state |
| Simple utility (calculate, convert, format) | Function | No need for OOP overhead |
| Plugin/extension system | Class + inheritance | Polymorphism shines here |

**Common mistake:** Don't use OOP for everything. A simple function is better than a class with one method.

```python
# OVERKILL — don't do this
class Adder:
    def add(self, a, b):
        return a + b

# JUST USE A FUNCTION
def add(a, b):
    return a + b
```

### Modules and Packages

A **module** is a `.py` file. A **package** is a directory of modules with an `__init__.py`.

```
myproject/
├── main.py
├── utils/
│   ├── __init__.py
│   ├── math_helpers.py
│   └── string_helpers.py
└── models/
    ├── __init__.py
    └── user.py
```

```python
# utils/math_helpers.py
def clamp(value, minimum, maximum):
    """Restrict value to [minimum, maximum] range."""
    return max(minimum, min(value, maximum))

# main.py
from utils.math_helpers import clamp

result = clamp(150, 0, 100)   # 100
```

**Why modules matter:**
1. **Organization** — group related code together
2. **Reuse** — import and use across projects
3. **Namespace** — avoid name collisions
4. **Testing** — test modules independently

### Virtual Environments

A **virtual environment** is an isolated Python installation for your project. Different projects can have different versions of the same package.

```
System Python 3.11
├── Project A venv → requests 2.28, flask 2.3
├── Project B venv → requests 2.31, django 4.2
└── Project C venv → requests 2.25, flask 1.1  ← old version, still works
```

**Without venvs:** Installing package X for Project A might break Project B.

```bash
# Create a virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate        # Windows

# Now pip installs go into .venv, not system Python
pip install requests

# Deactivate when done
deactivate
```

**Better approach:** Use `uv` (covered in the Production Engineering curriculum):
```bash
uv init myproject
uv add requests
uv run python main.py    # Automatically uses the project's venv
```

### Error Handling

**Errors are normal.** Production code handles them gracefully instead of crashing.

```python
# Without error handling: program crashes
result = int("not_a_number")   # ValueError!

# With error handling: program continues
try:
    result = int("not_a_number")
except ValueError:
    result = 0
    print("Invalid input, using default")
```

**The try/except/else/finally pattern:**
```python
try:
    # Code that might fail
    file = open("data.txt")
    content = file.read()
except FileNotFoundError:
    # Handle specific error
    print("File not found")
    content = ""
except PermissionError:
    # Handle different error
    print("No permission to read file")
    content = ""
else:
    # Runs ONLY if no exception was raised
    print(f"Read {len(content)} characters")
finally:
    # ALWAYS runs (cleanup)
    if 'file' in locals():
        file.close()
```

**When to catch exceptions:**

| Do | Don't |
|---|---|
| Catch specific exceptions (`ValueError`) | Catch everything (`except:` or `except Exception:`) |
| Handle errors you can recover from | Silently ignore errors (`except: pass`) |
| Let unexpected errors propagate up | Catch errors just to print them and re-crash |
| Use `with` for resource cleanup | Manually open/close files in try/finally |

**Common beginner misunderstandings:**

| Mistake | Reality |
|---------|---------|
| "Never let errors happen" | Errors are expected. Handle them, don't prevent all of them |
| "Wrap everything in try/except" | Only wrap code that *might* fail with errors you can *handle* |
| "`except Exception: pass`" | This hides bugs. You'll spend hours debugging invisible errors |
| "I don't need venvs for small projects" | Some day you'll need two projects with conflicting deps. Start with venvs now |
| "Classes are always better than functions" | Use classes when you have state. Use functions for stateless operations |

---

## PART B — BEGINNER PRACTICE

### Exercise 2.B.1 — Your First Class

```python
class Rectangle:
    """A rectangle with width and height."""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        """Calculate the area."""
        return self.width * self.height
    
    def perimeter(self):
        """Calculate the perimeter."""
        return 2 * (self.width + self.height)
    
    def is_square(self):
        """Check if this rectangle is a square."""
        return self.width == self.height
    
    def __repr__(self):
        """String representation for debugging."""
        return f"Rectangle(width={self.width}, height={self.height})"


# Test it
r1 = Rectangle(5, 3)
r2 = Rectangle(4, 4)

print(r1)                  # Rectangle(width=5, height=3)
print(f"Area: {r1.area()}")           # 15
print(f"Perimeter: {r1.perimeter()}")  # 16
print(f"Is square? {r1.is_square()}")  # False
print(f"r2 is square? {r2.is_square()}")  # True
```

### Exercise 2.B.2 — Class with Validation

```python
class Temperature:
    """Temperature with validation and conversion."""
    
    def __init__(self, celsius):
        if celsius < -273.15:
            raise ValueError(
                f"Temperature {celsius}°C is below absolute zero (-273.15°C)"
            )
        self.celsius = celsius
    
    @property
    def fahrenheit(self):
        """Convert to Fahrenheit."""
        return self.celsius * 9 / 5 + 32
    
    @property
    def kelvin(self):
        """Convert to Kelvin."""
        return self.celsius + 273.15
    
    @classmethod
    def from_fahrenheit(cls, f):
        """Create Temperature from Fahrenheit."""
        return cls((f - 32) * 5 / 9)
    
    @classmethod
    def from_kelvin(cls, k):
        """Create Temperature from Kelvin."""
        return cls(k - 273.15)
    
    def __repr__(self):
        return f"Temperature({self.celsius:.1f}°C)"


# Test
t1 = Temperature(100)
print(f"{t1} = {t1.fahrenheit:.1f}°F = {t1.kelvin:.1f}K")

t2 = Temperature.from_fahrenheit(72)
print(f"72°F = {t2}")

# This should raise an error:
try:
    t3 = Temperature(-300)
except ValueError as e:
    print(f"Error: {e}")
```

### Exercise 2.B.3 — Inheritance

```python
class Shape:
    """Base class for all shapes."""
    
    def __init__(self, name):
        self.name = name
    
    def area(self):
        raise NotImplementedError("Subclasses must implement area()")
    
    def __repr__(self):
        return f"{self.name}(area={self.area():.2f})"


class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius
    
    def area(self):
        import math
        return math.pi * self.radius ** 2


class Triangle(Shape):
    def __init__(self, base, height):
        super().__init__("Triangle")
        self.base = base
        self.height = height
    
    def area(self):
        return 0.5 * self.base * self.height


class Square(Shape):
    def __init__(self, side):
        super().__init__("Square")
        self.side = side
    
    def area(self):
        return self.side ** 2


# Polymorphism in action
shapes = [Circle(5), Triangle(6, 4), Square(3), Circle(2.5)]

for shape in shapes:
    print(shape)

# Find the largest shape
largest = max(shapes, key=lambda s: s.area())
print(f"\nLargest: {largest}")
```

### Exercise 2.B.4 — Using Modules

```python
# Create this file structure and test imports:
# practice/
# ├── main.py
# ├── calculator/
# │   ├── __init__.py
# │   ├── basic.py       ← add, subtract, multiply, divide
# │   └── advanced.py    ← power, sqrt, factorial
# └── formatter/
#     ├── __init__.py
#     └── display.py     ← format_result

# calculator/basic.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


# calculator/advanced.py
import math

def power(base, exponent):
    return base ** exponent

def sqrt(n):
    if n < 0:
        raise ValueError("Cannot take square root of negative number")
    return math.sqrt(n)

def factorial(n):
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    return math.factorial(n)


# calculator/__init__.py
from calculator.basic import add, subtract, multiply, divide
from calculator.advanced import power, sqrt, factorial


# formatter/display.py
def format_result(operation, result, precision=2):
    return f"  {operation} = {result:.{precision}f}"


# main.py
from calculator import add, multiply, sqrt, factorial
from formatter.display import format_result

print(format_result("2 + 3", add(2, 3)))
print(format_result("7 × 8", multiply(7, 8)))
print(format_result("√144", sqrt(144)))
print(format_result("5!", factorial(5), precision=0))
```

### Exercise 2.B.5 — Error Handling Basics

```python
def safe_divide(a, b):
    """Divide a by b, handling errors gracefully."""
    try:
        result = a / b
    except ZeroDivisionError:
        print(f"Error: Cannot divide {a} by zero")
        return None
    except TypeError as e:
        print(f"Error: Invalid types — {e}")
        return None
    else:
        return result


# Test cases
print(safe_divide(10, 3))       # 3.333...
print(safe_divide(10, 0))       # Error message, None
print(safe_divide("10", 3))     # Error message, None


def safe_int(value, default=0):
    """Convert to int safely, returning default on failure."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


print(safe_int("42"))           # 42
print(safe_int("hello"))       # 0
print(safe_int("hello", -1))  # -1
print(safe_int(None))          # 0
```

### Exercise 2.B.6 — Context Managers (`with` statement)

```python
# Writing files safely with context managers
def write_report(filename, data):
    """Write a report to a file using a context manager."""
    with open(filename, "w") as f:
        f.write("=== Report ===\n\n")
        for key, value in data.items():
            f.write(f"{key}: {value}\n")
        f.write(f"\nTotal items: {len(data)}\n")
    # File is automatically closed here, even if an error occurred


def read_file_safely(filename):
    """Read a file, returning None if it doesn't exist."""
    try:
        with open(filename) as f:
            return f.read()
    except FileNotFoundError:
        print(f"File '{filename}' not found")
        return None
    except PermissionError:
        print(f"No permission to read '{filename}'")
        return None


# Test
data = {"users": 150, "revenue": 45000, "errors": 3}
write_report("/tmp/report.txt", data)
content = read_file_safely("/tmp/report.txt")
if content:
    print(content)

# This should handle missing file gracefully
read_file_safely("/tmp/nonexistent.txt")
```

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 2.C.1 — Data Classes (Modern Python OOP)

```python
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Product:
    """Product with automatic __init__, __repr__, __eq__."""
    name: str
    price: float
    quantity: int = 0
    tags: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    @property
    def total_value(self):
        return self.price * self.quantity
    
    def apply_discount(self, percent):
        """Return a new Product with discounted price."""
        discounted = self.price * (1 - percent / 100)
        return Product(
            name=self.name,
            price=round(discounted, 2),
            quantity=self.quantity,
            tags=self.tags.copy(),
        )


# Data classes give you __init__, __repr__, __eq__ for free
p1 = Product("Laptop", 999.99, 5, ["electronics", "sale"])
p2 = Product("Laptop", 999.99, 5, ["electronics", "sale"])

print(p1)                        # Product(name='Laptop', price=999.99, ...)
print(f"Total value: ${p1.total_value:,.2f}")
print(f"p1 == p2: {p1 == p2}")   # True (compares all fields)

p3 = p1.apply_discount(20)
print(f"After 20% off: {p3}")
```

### Exercise 2.C.2 — Magic Methods (Dunder Methods)

```python
class Money:
    """Money with currency, supporting arithmetic operations."""
    
    def __init__(self, amount, currency="USD"):
        self.amount = round(amount, 2)
        self.currency = currency
    
    def __repr__(self):
        return f"Money({self.amount}, '{self.currency}')"
    
    def __str__(self):
        symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
        symbol = symbols.get(self.currency, self.currency + " ")
        return f"{symbol}{self.amount:,.2f}"
    
    def __add__(self, other):
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise ValueError(f"Cannot add {self.currency} and {other.currency}")
            return Money(self.amount + other.amount, self.currency)
        return Money(self.amount + other, self.currency)
    
    def __sub__(self, other):
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise ValueError(f"Cannot subtract {other.currency} from {self.currency}")
            return Money(self.amount - other.amount, self.currency)
        return Money(self.amount - other, self.currency)
    
    def __mul__(self, factor):
        return Money(self.amount * factor, self.currency)
    
    def __eq__(self, other):
        return isinstance(other, Money) and self.amount == other.amount and self.currency == other.currency
    
    def __lt__(self, other):
        if isinstance(other, Money) and self.currency == other.currency:
            return self.amount < other.amount
        raise ValueError("Cannot compare different currencies")
    
    def __bool__(self):
        return self.amount != 0


# Test
price = Money(29.99)
tax = Money(2.40)
total = price + tax
print(f"Price: {price}")           # $29.99
print(f"Tax:   {tax}")             # $2.40
print(f"Total: {total}")           # $32.39
print(f"Double: {total * 2}")      # $64.78
print(f"Equal? {price == Money(29.99)}")  # True

# Error handling
try:
    usd = Money(100, "USD")
    eur = Money(50, "EUR")
    result = usd + eur     # Cannot add different currencies
except ValueError as e:
    print(f"Error: {e}")
```

### Exercise 2.C.3 — Decorators

```python
import time
import functools


# 1. Timer decorator — measures execution time
def timer(func):
    """Measure and print function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {func.__name__}() took {elapsed:.4f}s")
        return result
    return wrapper


# 2. Retry decorator — retry on failure
def retry(max_attempts=3, delay=0.1):
    """Retry a function up to max_attempts times on exception."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"  Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


# 3. Validate types decorator
def validate_types(**type_hints):
    """Validate argument types at runtime."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import inspect
            sig = inspect.signature(func)
            params = list(sig.parameters.keys())
            
            for i, arg in enumerate(args):
                param_name = params[i]
                if param_name in type_hints:
                    expected = type_hints[param_name]
                    if not isinstance(arg, expected):
                        raise TypeError(
                            f"{param_name} must be {expected.__name__}, "
                            f"got {type(arg).__name__}"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Usage
@timer
def slow_sum(n):
    """Sum numbers from 0 to n."""
    return sum(range(n))

result = slow_sum(1_000_000)
print(f"  Result: {result:,}")


@retry(max_attempts=3)
def flaky_operation():
    """Simulates an operation that sometimes fails."""
    import random
    if random.random() < 0.7:
        raise ConnectionError("Server unavailable")
    return "Success!"

try:
    print(flaky_operation())
except ConnectionError:
    print("  All attempts failed")


@validate_types(name=str, age=int)
def create_user(name, age):
    return {"name": name, "age": age}

print(create_user("Arun", 25))

try:
    create_user("Arun", "twenty-five")
except TypeError as e:
    print(f"  Error: {e}")
```

### Exercise 2.C.4 — Enum and Type Safety

```python
from enum import Enum, auto


class OrderStatus(Enum):
    PENDING = auto()
    CONFIRMED = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class Order:
    VALID_TRANSITIONS = {
        OrderStatus.PENDING: {OrderStatus.CONFIRMED, OrderStatus.CANCELLED},
        OrderStatus.CONFIRMED: {OrderStatus.SHIPPED, OrderStatus.CANCELLED},
        OrderStatus.SHIPPED: {OrderStatus.DELIVERED},
        OrderStatus.DELIVERED: set(),
        OrderStatus.CANCELLED: set(),
    }
    
    def __init__(self, order_id, priority=Priority.MEDIUM):
        self.order_id = order_id
        self.status = OrderStatus.PENDING
        self.priority = priority
    
    def transition_to(self, new_status):
        allowed = self.VALID_TRANSITIONS[self.status]
        if new_status not in allowed:
            raise ValueError(
                f"Cannot transition from {self.status.name} to {new_status.name}. "
                f"Allowed: {[s.name for s in allowed]}"
            )
        old_status = self.status
        self.status = new_status
        print(f"  Order {self.order_id}: {old_status.name} → {new_status.name}")


# Test valid transitions
order = Order("ORD-001", Priority.HIGH)
order.transition_to(OrderStatus.CONFIRMED)
order.transition_to(OrderStatus.SHIPPED)
order.transition_to(OrderStatus.DELIVERED)

# Test invalid transition
order2 = Order("ORD-002")
try:
    order2.transition_to(OrderStatus.DELIVERED)  # Can't skip steps!
except ValueError as e:
    print(f"  Error: {e}")
```

### Exercise 2.C.5 — Building a Real Module

```python
"""
Task: Build a 'validators' module with reusable validation functions.
This is the kind of utility module real projects have.
"""

# validators.py
import re
from typing import Any


class ValidationError(Exception):
    """Custom exception for validation failures."""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")


def validate_required(value: Any, field_name: str) -> Any:
    """Ensure a value is not None or empty."""
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValidationError(field_name, "is required")
    return value


def validate_email(email: str, field_name: str = "email") -> str:
    """Validate an email address format."""
    validate_required(email, field_name)
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        raise ValidationError(field_name, f"'{email}' is not a valid email")
    return email.lower().strip()


def validate_range(value: float, field_name: str, *, min_val=None, max_val=None) -> float:
    """Validate that a number is within a range."""
    if min_val is not None and value < min_val:
        raise ValidationError(field_name, f"must be at least {min_val}, got {value}")
    if max_val is not None and value > max_val:
        raise ValidationError(field_name, f"must be at most {max_val}, got {value}")
    return value


def validate_length(value: str, field_name: str, *, min_len=None, max_len=None) -> str:
    """Validate string length."""
    if min_len is not None and len(value) < min_len:
        raise ValidationError(field_name, f"must be at least {min_len} characters")
    if max_len is not None and len(value) > max_len:
        raise ValidationError(field_name, f"must be at most {max_len} characters")
    return value


# Usage
def register_user(name, email, age):
    """Register a user with validation."""
    errors = []
    
    try:
        name = validate_required(name, "name")
        name = validate_length(name, "name", min_len=2, max_len=50)
    except ValidationError as e:
        errors.append(str(e))
    
    try:
        email = validate_email(email)
    except ValidationError as e:
        errors.append(str(e))
    
    try:
        age = validate_range(age, "age", min_val=0, max_val=150)
    except ValidationError as e:
        errors.append(str(e))
    
    if errors:
        print("Registration failed:")
        for error in errors:
            print(f"  ✗ {error}")
        return None
    
    user = {"name": name, "email": email, "age": age}
    print(f"  ✓ Registered: {user}")
    return user


# Test
register_user("Arun", "arun@example.com", 25)       # Success
register_user("", "bad-email", 200)                    # Multiple errors
register_user("A", "a@b.com", -5)                      # Validation errors
```

---

## PART D — ADVANCED DEBUG LAB

### Exercise 2.D.1 — Debug: Broken Inheritance

```python
"""
BUG: The employee payroll system gives wrong results.
Find and fix the bugs.
"""

class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary
    
    def calculate_pay(self):
        return self.base_salary


class Manager(Employee):
    def __init__(self, name, base_salary, bonus_percent):
        # BUG 1: Forgot to call super().__init__()
        self.bonus_percent = bonus_percent
    
    def calculate_pay(self):
        # BUG 2: This will crash because self.base_salary doesn't exist
        bonus = self.base_salary * self.bonus_percent / 100
        return self.base_salary + bonus


class Intern(Employee):
    def __init__(self, name, stipend):
        super().__init__(name, stipend)
    
    def calculate_pay(self):
        # BUG 3: Calling parent's method but also adding stipend again
        return super().calculate_pay() + self.base_salary


# Test — this will crash or give wrong results
try:
    emp = Employee("Alice", 5000)
    mgr = Manager("Bob", 8000, 15)
    intern = Intern("Charlie", 1500)
    
    for person in [emp, mgr, intern]:
        print(f"{person.name}: ${person.calculate_pay():,.2f}")
except AttributeError as e:
    print(f"BUG FOUND: {e}")
```

<details>
<summary>Fixed version</summary>

```python
class Manager(Employee):
    def __init__(self, name, base_salary, bonus_percent):
        super().__init__(name, base_salary)  # Fix 1: Call super
        self.bonus_percent = bonus_percent
    
    def calculate_pay(self):
        bonus = self.base_salary * self.bonus_percent / 100
        return self.base_salary + bonus

class Intern(Employee):
    def __init__(self, name, stipend):
        super().__init__(name, stipend)
    
    def calculate_pay(self):
        return self.base_salary  # Fix 3: Just return stipend, don't double it
```
</details>

### Exercise 2.D.2 — Debug: Scope and Closure Bugs

```python
"""
Predict the output, then run to verify.
"""

# Puzzle 1: Variable scope
x = "global"

def outer():
    x = "outer"
    def inner():
        print(f"inner sees: {x}")
    inner()
    print(f"outer sees: {x}")

outer()
print(f"global sees: {x}")


# Puzzle 2: Late binding closure bug
def create_multipliers():
    multipliers = []
    for i in range(5):
        multipliers.append(lambda x: x * i)   # BUG: i is captured by reference
    return multipliers

mults = create_multipliers()
print([m(10) for m in mults])
# Expected: [0, 10, 20, 30, 40]
# Actual:   [40, 40, 40, 40, 40] — ALL use i=4!

# Fix: capture i by value using default argument
def create_multipliers_fixed():
    multipliers = []
    for i in range(5):
        multipliers.append(lambda x, i=i: x * i)   # i=i captures current value
    return multipliers

mults_fixed = create_multipliers_fixed()
print([m(10) for m in mults_fixed])   # [0, 10, 20, 30, 40] ✓
```

### Exercise 2.D.3 — Debug: Exception Handling Gone Wrong

```python
"""
This code has bad exception handling patterns. Find and fix them.
"""

import json

# BAD 1: Bare except silences all errors including KeyboardInterrupt
def bad_parse(data):
    try:
        return json.loads(data)
    except:                    # ← NEVER do this
        return None

# BAD 2: Catching too broadly
def bad_read(filename):
    try:
        with open(filename) as f:
            data = json.loads(f.read())
            result = data["key"] / data["divisor"]
            return result
    except Exception as e:     # ← Which error? File? JSON? Key? Division?
        print(f"Something went wrong: {e}")
        return None

# BAD 3: Swallowing the exception
def bad_process(items):
    results = []
    for item in items:
        try:
            results.append(item["value"] * 2)
        except Exception:
            pass               # ← Silently skipping bad data
    return results


# FIXED VERSIONS:

def good_parse(data):
    """Parse JSON with specific error handling."""
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return None


def good_read(filename):
    """Read and process a JSON file with granular error handling."""
    try:
        with open(filename) as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None
    
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {filename}: {e}")
        return None
    
    try:
        return data["key"] / data["divisor"]
    except KeyError as e:
        print(f"Missing required field: {e}")
        return None
    except ZeroDivisionError:
        print("Divisor is zero")
        return None


def good_process(items):
    """Process items, logging bad data instead of silently skipping."""
    results = []
    errors = []
    for i, item in enumerate(items):
        try:
            results.append(item["value"] * 2)
        except (KeyError, TypeError) as e:
            errors.append(f"Item {i}: {e}")
    
    if errors:
        print(f"Processed with {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
    
    return results
```

---

## PART E — PRODUCTION SIMULATION

### Scenario: Build a Task Manager Library

**Task:** Build a reusable task manager module that demonstrates OOP, modules, error handling, and clean code.

```python
# task_manager.py
"""
Task Manager — A production-quality task management library.

Demonstrates: OOP, enums, error handling, clean architecture.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Optional


class TaskStatus(Enum):
    TODO = auto()
    IN_PROGRESS = auto()
    DONE = auto()
    CANCELLED = auto()


class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

    def __lt__(self, other):
        return self.value < other.value


class TaskError(Exception):
    """Base exception for task operations."""
    pass


class TaskNotFoundError(TaskError):
    """Raised when a task is not found."""
    pass


class InvalidTransitionError(TaskError):
    """Raised when a status transition is not allowed."""
    pass


@dataclass
class Task:
    """A single task with status tracking."""
    title: str
    task_id: int = 0
    description: str = ""
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.TODO
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    tags: list[str] = field(default_factory=list)

    ALLOWED_TRANSITIONS = {
        TaskStatus.TODO: {TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED},
        TaskStatus.IN_PROGRESS: {TaskStatus.DONE, TaskStatus.TODO, TaskStatus.CANCELLED},
        TaskStatus.DONE: {TaskStatus.TODO},  # Re-open
        TaskStatus.CANCELLED: {TaskStatus.TODO},  # Re-open
    }

    def transition_to(self, new_status: TaskStatus):
        """Move task to a new status if the transition is valid."""
        allowed = self.ALLOWED_TRANSITIONS[self.status]
        if new_status not in allowed:
            raise InvalidTransitionError(
                f"Cannot move from {self.status.name} to {new_status.name}. "
                f"Allowed: {[s.name for s in allowed]}"
            )
        self.status = new_status
        if new_status == TaskStatus.DONE:
            self.completed_at = datetime.now().isoformat()


class TaskManager:
    """Manage a collection of tasks."""

    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def add(self, title: str, priority: TaskPriority = TaskPriority.MEDIUM,
            description: str = "", tags: list[str] = None) -> Task:
        """Add a new task and return it."""
        task = Task(
            task_id=self._next_id,
            title=title,
            priority=priority,
            description=description,
            tags=tags or [],
        )
        self._tasks[task.task_id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Task:
        """Get a task by ID."""
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task #{task_id} not found")
        return self._tasks[task_id]

    def complete(self, task_id: int) -> Task:
        """Mark a task as done."""
        task = self.get(task_id)
        if task.status == TaskStatus.TODO:
            task.transition_to(TaskStatus.IN_PROGRESS)
        task.transition_to(TaskStatus.DONE)
        return task

    def cancel(self, task_id: int) -> Task:
        """Cancel a task."""
        task = self.get(task_id)
        task.transition_to(TaskStatus.CANCELLED)
        return task

    def list_tasks(self, status: Optional[TaskStatus] = None,
                   priority: Optional[TaskPriority] = None) -> list[Task]:
        """List tasks, optionally filtered by status or priority."""
        tasks = list(self._tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        return sorted(tasks, key=lambda t: t.priority, reverse=True)

    def summary(self) -> dict:
        """Get a summary of tasks by status."""
        summary = {status.name: 0 for status in TaskStatus}
        for task in self._tasks.values():
            summary[task.status.name] += 1
        summary["TOTAL"] = len(self._tasks)
        return summary

    def print_board(self):
        """Print a Kanban-style board."""
        print("\n" + "=" * 60)
        print("  TASK BOARD")
        print("=" * 60)
        
        for status in TaskStatus:
            tasks = [t for t in self._tasks.values() if t.status == status]
            print(f"\n  [{status.name}] ({len(tasks)} tasks)")
            print(f"  {'-' * 40}")
            if not tasks:
                print("    (empty)")
            for task in sorted(tasks, key=lambda t: t.priority, reverse=True):
                priority_icon = {
                    TaskPriority.LOW: "○",
                    TaskPriority.MEDIUM: "●",
                    TaskPriority.HIGH: "▲",
                    TaskPriority.URGENT: "🔴",
                }[task.priority]
                tag_str = f" [{', '.join(task.tags)}]" if task.tags else ""
                print(f"    {priority_icon} #{task.task_id} {task.title}{tag_str}")
        
        print(f"\n{'=' * 60}")
        summary = self.summary()
        print(f"  Total: {summary['TOTAL']} | "
              f"Todo: {summary['TODO']} | "
              f"In Progress: {summary['IN_PROGRESS']} | "
              f"Done: {summary['DONE']} | "
              f"Cancelled: {summary['CANCELLED']}")
        print("=" * 60)


# --- Demo ---
if __name__ == "__main__":
    mgr = TaskManager()
    
    # Add tasks
    mgr.add("Set up project with uv", TaskPriority.HIGH, tags=["setup"])
    mgr.add("Write health endpoint", TaskPriority.HIGH, tags=["api"])
    mgr.add("Add Prometheus metrics", TaskPriority.MEDIUM, tags=["monitoring"])
    mgr.add("Write unit tests", TaskPriority.MEDIUM, tags=["testing"])
    mgr.add("Create Dockerfile", TaskPriority.MEDIUM, tags=["docker"])
    mgr.add("Set up CI/CD pipeline", TaskPriority.LOW, tags=["ci"])
    mgr.add("Write documentation", TaskPriority.LOW, tags=["docs"])
    
    # Work through tasks
    mgr.complete(1)  # Set up project
    mgr.complete(2)  # Health endpoint
    
    task3 = mgr.get(3)
    task3.transition_to(TaskStatus.IN_PROGRESS)
    
    mgr.cancel(7)   # Skip docs for now
    
    # Print board
    mgr.print_board()
    
    # Error handling demo
    print()
    try:
        mgr.get(999)
    except TaskNotFoundError as e:
        print(f"Expected error: {e}")
    
    try:
        mgr.complete(1)  # Already done → should transition TODO back
    except InvalidTransitionError as e:
        print(f"Expected error: {e}")
```

**Acceptance Criteria:**
- [ ] All classes have docstrings
- [ ] Custom exceptions with meaningful messages
- [ ] Enum for status and priority (no magic strings)
- [ ] State machine with valid transitions
- [ ] Filtering and sorting work correctly
- [ ] Error cases handled (not found, invalid transition)
- [ ] Code runs without errors
- [ ] No function longer than 20 lines

---

## Key Takeaways

1. **Use classes when you have state + behavior.** Use functions for stateless operations.
2. **Dataclasses reduce boilerplate.** Use them for data-heavy classes instead of writing `__init__` manually.
3. **Modules organize code.** One file per concept, group related files in packages.
4. **Virtual environments isolate dependencies.** Always use one. Better yet, use `uv`.
5. **Handle errors specifically.** Catch the exact exception you expect. Never bare `except:`.
6. **Decorators add behavior without modifying functions.** Use them for cross-cutting concerns (timing, retry, validation).

---

*Next: [Section 3 — Debugging (Superpower)](03-debugging.md)*
