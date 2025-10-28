from .main import getLine, chat, context


def __getattr__(name):
    global context
    print(f'New function: {name}')
    line, comment = getLine(name)
    def _catchParams(*args, **kwargs):
        pargs = [type(a).__name__ for a in args]
        pkargs = [str(k) + ' of type ' + type(v).__name__ for k, v in kwargs.items()]
        prompt = f''' In python create the function named {name} described by the user as: {comment}. In one of it's calls, it has parameters: {' , '.join(pargs)} and the keyword parameters: {' , '.join(pkargs)}. Generate only the python code for the function and nothing else.'''
        response = chat(prompt)
        context[name] = response
        print(response)
        exec(response, globals = globals())
        return globals()[name](*args, **kwargs)
    return _catchParams
