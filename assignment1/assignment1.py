# Write your code here.

#Task 1
def hello():
    return "Hello!"

#Task 2
def greet(name):
    return f"Hello, {name}!"

#Task 3
def calc(a, b, operation="multiply"):
    try:
        match operation:
            case "add":
                return a + b
            case "subtract":
                return a - b
            case "multiply":
                return a * b
            case "divide":
                return a / b
            case "modulo":
                return a % b
            case "int_divide":
                return a // b
            case "power":
                return a ** b
            case _:
                return "Invalid operation"
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return "You can't multiply those values!"
    
#Task 4
def data_type_conversion(value, to_type):
    try:
        match to_type:
            case "int":
                return int(value)
            case "float":
                return float(value)
            case "str":
                return str(value)
            case "list":
                return list(value)
            case "tuple":
                return tuple(value)
            case "set":
                return set(value)
            case _:
                return "Invalid type"
    except (ValueError, TypeError):
        return f"You can't convert {value} into a {to_type}."
    
#Task 5
def grade(*args):
    try:
        if not args:
            return "No grades provided."
    
        average = sum(args) / len(args)
        
        if average >= 90:
            return "A"
        elif average >= 80:
            return "B"
        elif average >= 70:
            return "C"
        elif average >= 60:
            return "D"
        else:
            return "F"
    except TypeError:
        return 'Invalid data was provided.'
    
#Task 6
def repeat(string, count):
    result = ""
    for i in range(count):
        result += string
    return result

#Task 7
def student_scores(mode, **kwargs):
    if not kwargs:
        return "No student scores provided."
    
    if mode == "best":
        best_student = max(kwargs, key=kwargs.get)
        return best_student
    elif mode == "mean":
        total = sum(kwargs.values())
        count = len(kwargs)
        return total / count
    else:
        return "Invalid mode"
    
#Task 8
def titleize(text):
    little_words = {'and', 'or', 'the', 'a', 'an', 'in', 'with', 'but', 'for', 'at', 'by', 'to', 'of'}
    words = text.split()
    for i, word in enumerate(words):
        if i == 0 or i == len(words):
            words[i] = word.capitalize()
        elif word.lower() not in little_words:
            words[i] = word.capitalize()
        else:
            words[i] = word.lower()

    return ' '.join(words)

#Task 9
def hangman(secret, guess):
    result = ""
    for letter in secret:
        if letter in guess:
            result += letter
        else:
            result += "_"
    return result

#Task 10
def pig_latin(text):
    vowels = "aeiouAEIOU"
    result_words = []

    for word in text.split():
        if word[0] in vowels:
            pig_word = word + "ay"
        else:
            index = 0
            while index < len(word) and word[index] not in vowels:
                if word[index:index+2].lower() == "qu":
                    index += 2
                    break
                index += 1
            pig_word = word[index:] + word[:index] + "ay"
        
        result_words.append(pig_word)

    return ' '.join(result_words)