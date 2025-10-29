import openai
import traceback
import linecache
import re
import tokenize
import io
from .prompt import BasePromptMaker

LLM = None
TOKENS = 1024
context = {}
MODEL = ''
PROMPTER = BasePromptMaker()

def connect_llm(URL, api='', model = ''):
    '''
    Create connection to LLM
    '''
    global LLM, MODEL
    MODEL = model
    if URL == 'OpenAI':
        LLM = openai.OpenAI(
            api_key = api,
            )
    else:
        LLM = openai.OpenAI(
            api_key = api,
            base_url = URL,
            )
    return

def chat(prompt):
    response = LLM.chat.completions.create(
            model = MODEL,
            messages = [
            {'role': 'user', 'content': prompt},
            ],
            max_tokens = TOKENS,
            )
    result = response.choices[0].message.content
    res = re.search(r"(?<=```python)[\w\W]*?(?=```)", result)
    if res:
        result = res.group()
    return result 

def getLine(name):
    '''
    Extracts the line from the traceback
    Uses 'name' to identify the intended function/class
    Returns the line and the comment
    '''
    frame = traceback.extract_stack()[-3]
    line = linecache.getline(frame.filename, frame.lineno).strip()
       
    tokens = tokenize.generate_tokens(io.StringIO(line).readline)
    comment = ''
    for token in tokens:
        if token.type == tokenize.COMMENT:
            comment = token.string[1:].strip()
            break
    return line, comment

def save(output, mode = 'w'):
    if not mode in ['w', 'a']:
        raise Exception('To save the code to a file, you must access it to write or append to it, set mode as either "w" or "a".')
    with open(output, mode) as f:
        for elem, code in context.items():
            if isinstance(code, list):
                f.write(code[0])
            else:
                f.write(code)
