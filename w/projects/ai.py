import pathlib
import textwrap

import google.generativeai as gencai

# Used to securely store your API key
#from IPython.display import display
#from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def main():
  genai.configure(api_key='AIzaSyBUdjeBbvThPHaFVYyTmcppzUyNxOfTPgw')
  for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
      print(m.name)
  model = genai.GenerativeModel('gemini-pro')
  response = model.generate_content("What is the meaning of life?")
  print(response)
  print('done')

main()
PATH=”$PATH:/usr/bin/python”
sudo ln -s /usr/bin/python3.12 /usr/bin/python
