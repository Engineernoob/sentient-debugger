def greet(name):
    """Simple greeting function"""
    message = f"Hello, {name}!"
    print(message)
    return message

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def describe(self):
        return f"{self.name} is {self.age} years old"

# Main program
if __name__ == "__main__":
    greet("World")
    person = Person("Alice", 30)
    print(person.describe())
