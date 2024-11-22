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
  print('Old (cats_dogs.html)  / new (cats_dogs_humans.tmp)  differences')

  e = input("Press enter to exit, \n or any key to continue\n and create new  tmp.html")
  if e == '':
    print('New file not created')
    exit(0)

  with open("cats_dogs_humans.tmp", "r") as infile, open('tmp.html', 'w') as outfile:
      # Iterate through each line in the file
      isContent = False
      englist_line_count = 0
      greek_line_count = 0
      for line in infile:
        new_line = line
        text = line.strip()
        if '<!-- -->' in line:
          isContent= True
        if isContent:
           if len(text) > 0 and text[0] != '<' and text[0] != '[':
             if len(text) > 0 and text[0] !='<':
               lang = language(text)
               if 'greek' in lang:
                 greek_line_count += 1
                 #new_line = to_str(greek_line_count)+ 'g'+ line
               elif 'english' in lang:
                 englist_line_count += 1
                 new_line = to_str(englist_line_count)+ line
        outfile.write(new_line)
      print('done', englist_line_count, greek_line_count)

def language(text):
  for char in text:
      if 'a' <= char <= 'z' or 'A' <= char <= 'Z':
        return 'english'
      elif char in 'αβγδεζηθικλμνξοπρστυφχψω':
        return 'greek'
  return '??'

def to_str(num):
    return str(num).rjust(3)

main()

