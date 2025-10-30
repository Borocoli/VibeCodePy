from .main import getLine, chat, context, PROMPTER
from .abscontext import ContextObj
import re


def _addM(name, method):
    global context
    ident = context[name].ident
    lines = method.splitlines()
    definition = ident + lines[0].lstrip()
    method = [definition] + [ident + line for line in lines[1:]]
    method = '\n'.join(method)
    context[name].code_def += '\n' +  method


def _getat(self, name):
    global context
    print(f'New Method {name} for class {self.__class__.__name__}')
    line, comment = getLine(name)
    def _catchParams(*args, **kwargs):
        pargs = [type(a).__name__ for a in args]
        pkargs = [str(k) + ' of type ' + type(v).__name__ for k, v in kwargs.items()]
        descr = None
        if '_description' in kwargs:
            descr = kwargs['_description']
            del kwargs['_description']
        prompt = PROMPTER.prompt(name, 'm', comment, pargs, pkargs, description = descr ,owner_class = context[self.__class__.__name__])
        response = chat(prompt)
        print(response)
        _addM(self.__class__.__name__, response)
        tmpname = self.__class__.__name__ + '_' + name
        response = re.sub(f'''def {name}''', f'def {tmpname}', response)
        exec(response.strip(), globals=globals())
        exec(f'''{self.__class__.__name__}.{name} = {tmpname}''', globals = globals())

        return getattr(self, name)(*args, **kwargs)
    return _catchParams
 
    pass


def __getattr__(name):
    global context
    print(f'New Class: {name}')
    line, comment = getLine(name)
    def _catchParams(*args, **kwargs):
        pargs = [type(a).__name__ for a in args]
        if not '_description' in kwargs:
            raise Exception('New classes must have a docstring associated through the _description keyword parameter')
        descr = kwargs['_description']
        del kwargs['_description']
        pkargs = [str(k) + ' of type ' + type(v).__name__ for k, v in kwargs.items()]
        prompt = PROMPTER.prompt(name, 'c', comment, pargs, pkargs, description=descr)
        response = chat(prompt)
        base_def = response.lstrip()
        ident = base_def.split('\n')[1]
        ident = len(ident) - len(ident.lstrip())
        ident = ''.join(ident*[' '])

        print(response)
        exec(response, globals = globals())
        globals()[name].__getattr__ = _getat
        
        tmp_context = ContextObj(name, response, descr, ident=ident)
        context.add_definition(tmp_context)
        return globals()[name](*args, **kwargs)
    return _catchParams


