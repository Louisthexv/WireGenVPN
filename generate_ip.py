import random


#create function
def generate_random_ip(class_type):
    if class_type == 'A':
        first_octect = random.randint(1, 126)
    elif class_type == 'B':
        first_octect = random.randint(128, 191)
    elif class_type == 'C':
        first_octect = random.randint(192, 223)
    else:
        return "Invalid Class Type"

    last_octec = random.randint(2, 254) # Avoid 0 and 1 for potential server devices
    return f"{first_octect}.0.0.{last_octec}"

    