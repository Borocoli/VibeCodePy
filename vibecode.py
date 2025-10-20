import openai
import traceback
import linecache
import re
import types

API_KEY = ''
URL = ''
MODEL = ''
LLM = None
TOKENS = 1024
V = True
_CONTEXT = {}



def connect_llm():
    '''
    Create connection to LLM
    '''
    global LLM
    if URL == '':
        raise Exception('No url selected, you need to specifiy the url')
    elif URL == 'OpenAI':
        LLM = openai.OpenAI(
            api_key = '',
            )
    else:
        LLM = openai.OpenAI(
            api_key = '',
            base_url = URL,
            )
    return


def _chat(prompt):
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

def _attrCreate(self, name):
    '''
    This function catches the undefined attribute, usually a method, and passes it to the AI to implement it.
    In order to generate a more meaningful definition the comment on the same line is also passed.
    '''
    frame = traceback.extract_stack()[-2]
    line = linecache.getline(frame.filename, frame.lineno).strip()
    if V:
        print('New attribute: ', name, ' at ', line)
    comment = re.search(r'(?<=#)\s*(\w\s*)+', line)
    if comment:
        if V:
            print('   Comment: ', comment[0])
        line = line.removesuffix(comment.group())
    parameters = re.search(f'(?<=(\\w\\.{name}))\\((\\s*[\\w\\W]\\s*,?)+\\)', line)
    if parameters:
        parameters = params = parameters.group()
        params = params[0] + ',' + params[1:]
        params, n = re.subn(r',\s*"[\w\W]*?"', ', string', params)
        params, n = re.subn(r",\s*'[\w\W]*?'", ', string', params)
        params, n = re.subn(r",\s*'''[\w\W]*?'''",  ', string', params)
        params, n = re.subn(r",\s*\{[\w\W]*?\}", ', dict_or_set', params)
        params, n = re.subn(r",\s*\([\w\W]+?\)", ', tuple', params)
        params, n = re.subn(r",\s*\[[\w\W]+?\]", ', list', params)
        params = params.split(',')[1:]
        lparams = len(params)
        if V:
            print('   Parameters: ', params)
            print('   Nr parameters: ', lparams)
        prompt = f''' Create the method {name} for the class {self.__class__.__name__} with the already defined functions : {_CONTEXT[self.__class__.__name__]}. The method has the {lparams} parameters and in the current instance it is called with the parameters: {parameters}. '''
        if comment:
            prompt += f'''The associated comment is: {comment.group()}. '''
        prompt += '''Generate only the python code for the method without anything else. ''' 
        response = _chat(prompt)
        if V:
            print(response)
        tmpname = self.__class__.__name__ + '_' + name
        response = re.sub(f'''def {name}''', f'def {tmpname}', response)
        _CONTEXT[self.__class__.__name__].append(response)
        exec(response.strip(), globals=globals())
        exec(f'''{self.__class__.__name__}.{name} = {tmpname}''', globals = globals())
        return getattr(self, name)
    else:
        self.__dict__[name] = None

def cls(name, description, attrs =  {}):
    prompt = f'''Create a class in python named {name} with the docstring and description {description} that has the following attributes: {list(attrs.keys())}. 
            Generate only the python code without anything else.'''
    result = _chat(prompt)
    if V:
        print(result)
    exec(result, globals= globals())
    exec(f'''{name}.__getattr__ = _attrCreate''', globals = globals())
    _CONTEXT[name] = [result]
    return eval(f'''{name}(**{attrs})''')
