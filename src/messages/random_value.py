import random
import json

MIN_VALUE = 20
MAX_VALUE = 80
STEP = 5

current_value = random.uniform(MIN_VALUE, MAX_VALUE)  # Start with a random value

def smooth_random_value():
    global current_value  # Use the global variable
    change = random.uniform(-STEP, STEP)  # Small smooth change
    new_value = current_value + change
    current_value = max(MIN_VALUE, min(MAX_VALUE, new_value))  # Keep within bounds
    return round(current_value, 4)

def get_random_value_message(timestamp: json):
    
    message = {
        "timestamp": timestamp,
        "value": smooth_random_value(),  
    }
    
    return json.dumps(message).encode('utf8')
