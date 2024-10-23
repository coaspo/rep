def main():
  print('start')
  with open("cats and humans.html", "r") as infile, open('cats and humans2.html', 'w') as outfile:
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
           if len(text) > 0 and text[0] != '<':
             if len(text) > 0 and text[0] !='<':
               lang = language(text)
               if 'greek' in lang:
                 greek_line_count += 1
                 new_line = to_str(greek_line_count)+ line
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

