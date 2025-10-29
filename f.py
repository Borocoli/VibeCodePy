from .main import getLine, chat, context, PROMPTER


def __getattr__(name):
    global context
    print(f'New function: {name}')
    line, comment = getLine(name)
    def _catchParams(*args, **kwargs):
        pargs = [type(a).__name__ for a in args]
        pkargs = [str(k) + ' of type ' + type(v).__name__ for k, v in kwargs.items()]
        prompt = PROMPTER.prompt(name, 'f', comment, pargs, pkargs)
        response = chat(prompt)
        context[name] = response
        print(response)
        exec(response, globals = globals())
        return globals()[name](*args, **kwargs)
    return _catchParams
