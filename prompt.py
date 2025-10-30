from abc import ABC, abstractmethod
from .abscontext import ContextObj

class PromptMaker(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def prompt(self, name: str, tip: int, comment: str, pargs: list, kargs: list, description = None, owner_class: ContextObj = None) -> str:
        '''
        Generates the prompt and returns it as a string
        '''
        pass

class BasePromptMaker(PromptMaker):
    def __init__(self):
        super().__init__()
        self.pre_str = ''
        self.what_str = 'In python, create the {tip} named {name}'
        self.owner_class_str = '''of the class {c} with the definition:\n{class_def}\n'''
        self.description_str = '''The {tip} has the following docstring that acts as it's description:\n{description}\n'''
        self.comment_str = '''The {tip} is described by the user as: {comment}.'''
        self.no_comment_str = ''
        self.args_str = '''In one of it's calls, it has'''
        self.positional_args_str = '''the following positional arguments: {args}'''
        self.keyword_args_str = '''the following keyword arguments: {args}'''
        self.no_parameters_str = 'The {tip} is called without arguments in one of it\'s call'
        self.post_str = 'Generate only the python code of the {tip} and nothing else.'
        self.replace = {'f': 'function',
                        'c': 'class',
                        'm': 'method',
                        }



    def pre(self):
        '''
        First info passed into the prompt.
        '''
        return self.pre_str
        pass
    def what(self, tip, name):
        '''
        What code to write.
        tip - what type of code the LLM is requested to write, it takes the following values:
            f - function
            c - class
            m - method
        '''
        return self.what_str.format(tip=tip, name=name)

    def comment(self, comment, tip):
        '''
        How to add to the prompt user comments.
        '''
        return self.comment_str.format(tip=tip, comment=comment)

    def no_comment(self):
        '''
        What to write if there are no user comments.
        '''
        return self.no_comment_str

    def owner_class(self,  owner_class: ContextObj):
        '''
        How to add the method's class to the prompt.
        '''
        return self.owner_class_str.format(c=owner_class.name, class_def = owner_class.code_def)

    def description(self, description, tip):
        '''
        How to add the docstring of the code to the prompt
        '''
        return self.description_str.format(tip=tip, description=description)

    def positional_args(self, pargs):
        '''
        How to add the positional arguments to the prompt
        '''
        return self.positional_args_str.format(args=' , '.join(pargs))

    def keyword_args(self, kargs):
        '''
        How to add the keyword arguments to the prompt
        '''
        return self.keyword_args_str.format(args=' , '.join(kargs))

    def no_parameters(self, tip):
        '''
        What to add to the prompt if there are no parameters 
        '''
        return self.no_parameters_str(tip=tip)
    def post(self, tip):
        '''
        What to add at the end of the prompt
        '''
        return self.post_str.format(tip=tip)

    def prompt(self, name: str, tip: str, comment: str, pargs: list = None, kargs: list = None, description = None, owner_class: ContextObj=None) -> str:
        '''
        Generates the prompt and returns it as a string
        '''
        tip = self.replace[tip]
        prompt = self.pre()
        prompt += self.what(tip, name) + ' '
        if owner_class:
                prompt += self.owner_class(owner_class) + ' '
        else:
            prompt += '. '
        if description:
            prompt += self.description(description, tip) + ' '
        if comment:
            prompt += self.comment(comment, tip) + ' '
        else:
            prompt += self.no_comment() + ' '
        if pargs or kargs:
            prompt += self.args_str + ' '
            if pargs:
                prompt += self.positional_args(pargs)
                if kargs:
                    prompt += ' and '
            if kargs:
                prompt += self.keyword_args(kargs)
        else:
            prompt += self.no_parameters_str.format(tip=tip)
        prompt += '. '
        prompt += self.post(tip)
        return prompt
