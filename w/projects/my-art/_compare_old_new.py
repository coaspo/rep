def main():
  print('start')

  import re
  with open("cats_dogs.html", 'r+') as file:
    content = file.read()
    content = re.sub(r'\n\s{0,2}\d{1,3}', '\n', content)
    file.seek(0)  # Go back to the beginning of the file
    file.write(content)
    file.truncate()  # Remove any extra data from the old file
  print('Removed line numbers in Old (cats_dogs.html)')

  import difflib
  with open("cats_dogs.html") as f1, open("cats_dogs_humans.tmp") as f2:
      diff = difflib.unified_diff(f1.readlines(), f2.readlines())

  for line in diff:
      print(line)
  print('Above are old (cats_dogs.html)  / new (cats_dogs_humans.tmp)  differences')

main()
