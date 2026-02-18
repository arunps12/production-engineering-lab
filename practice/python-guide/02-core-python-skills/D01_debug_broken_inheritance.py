"""
Exercise 2.D.1 — Debug: Broken Inheritance
Guide: docs/python-guide/02-core-python-skills.md

This code has inheritance bugs. Find and fix them all.
"""


class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def speak(self):
        return f"{self.name} says {self.sound}"


class Dog(Animal):
    def __init__(self, name, breed):
        # BUG: Missing super().__init__() call
        self.breed = breed

    def fetch(self, item):
        return f"{self.name} fetches {item}"


class Puppy(Dog):
    def __init__(self, name, breed):
        super().__init__(name, breed)
        self.energy = 100

    def play(self):
        self.energy -= 10
        return f"{self.name} plays! Energy: {self.energy}"


# TODO: Fix the bugs and verify these all work:
# dog = Dog("Rex", "German Shepherd")
# print(dog.speak())           # Should work
# print(dog.fetch("ball"))     # Should work
# puppy = Puppy("Max", "Labrador")
# print(puppy.speak())         # Should work
# print(puppy.play())          # Should work
