#!/home/th/python_venv/bin/python
#source python_venv/bin/activate
import random
import string


chars = string.ascii_letters + string.digits + string.punctuation
print(string.ascii_letters)
print(string.digits)
print(string.punctuation,  '\n')
n = len(string.ascii_letters) + 10 + len(string.ascii_letters)
print(n,'^10 =', f"{(n**10):,}")
print(n,'^8 =', f"{(n**8):,}")

n_chars = 10

while 1==1:
  for i in range(10):
    random_string = ''.join(random.choice(chars) for _ in range(n_chars))
    print(random_string)
  char = input("\nPress <return> to repeat, \n  or  <any key> <return> to exit.")
  if char != '':
    exit(0)

