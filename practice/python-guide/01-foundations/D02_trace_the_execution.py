"""
Exercise 1.D.2 — Trace the Execution
Guide: docs/python-guide/01-foundations.md

For each code block, predict the output WITHOUT running it.
Then run it to verify your prediction.
Write your prediction as a comment before each block.
"""


# Puzzle 1: What does this print?
# Prediction: ___
x = [1, 2, 3]
y = x
y.append(4)
print("Puzzle 1:", x)


# Puzzle 2: What does this print?
# Prediction: ___
def modify(lst):
    lst = [10, 20, 30]

data = [1, 2, 3]
modify(data)
print("Puzzle 2:", data)


# Puzzle 3: What does this print?
# Prediction: ___
result = []
for i in range(3):
    result.append(lambda: i)
print("Puzzle 3:", [f() for f in result])


# Puzzle 4: What does this print?
# Prediction: ___
a = [1, 2, 3]
b = a[:]
b.append(4)
print("Puzzle 4:", a, b)


# TODO: Write explanations for WHY each output is what it is
