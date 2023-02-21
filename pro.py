import hashlib
import random

def predictable_random_order(password, lst):
    # Use SHA-256 hash of the password as the seed for the random generator
    random.seed(int(hashlib.sha256(password.encode()).hexdigest(), 16))
    
    # Use the Fisher-Yates shuffle algorithm to randomly order the list
    for i in range(len(lst)-1, 0, -1):
        j = random.randint(0, i)
        lst[i], lst[j] = lst[j], lst[i]
    
    return lst
    
'''lst = [1, 2, 3, 4, 5]
password = "my_secret_password1343132"
randomized_lst = predictable_random_order(password, lst)
print(randomized_lst)  # Output: [3, 5, 1, 4, 2]'''

