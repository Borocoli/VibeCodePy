from .main import getLine, chat, context
import re


def _addM(name, method):
    global context
    ident = context[name][1]
    lines = method.splitlines()
    definition = ident + lines[0].lstrip()
    method = [definition] + [ident + line for line in lines[1:]]
    method = '\n'.join(method)
    context[name][0] += '\n' +  method
    print(context[name][0])


def _getat(self, name):
    global context
    print(f'New Method {name} for class {self.__class__.__name__}')
    line, comment = getLine(name)
    def _catchParams(*args, **kwargs):
        pargs = [type(a).__name__ for a in args]
        pkargs = [str(k) + ' of type ' + type(v).__name__ for k, v in kwargs.items()]
        prompt = f''' In python create the method named {name} of the class defined as:
            {context[self.__class__.__name__][0]}
            The method is described by the user as: {comment}. In one of it's calls, it has parameters: {' , '.join(pargs)} and the keyword parameters: {' , '.join(pkargs)}. Generate only the python code and nothing else'''
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
        prompt = f''' In python create the class named {name} with the docstring:
            {descr}
            Which is described by the user as: {comment}. In one of it's calls, it has parameters: {' , '.join(pargs)} and the keyword parameters: {' , '.join(pkargs)}. Generate only the python code and nothing else'''
        response = chat(prompt)
        base_def = response.lstrip()
        ident = base_def.split('\n')[1]
        ident = len(ident) - len(ident.lstrip())
        ident = ''.join(ident*[' '])

        context[name] = [response, ident]
        print(response)
        exec(response, globals = globals())
        globals()[name].__getattr__ = _getat
        return globals()[name](*args, **kwargs)
    return _catchParams


