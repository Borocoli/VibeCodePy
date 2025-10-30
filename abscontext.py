class ContextObj:
    def __init__(self, name: str, code_def: str, description: str = "", ident: str = "", references=[], referenced_by=[]):
        self.name = name
        self.code_def = code_def
        self.description = description
        self.ident = ident
        self.references = references
        self.referenced_by = referenced_by

    def is_in_references(self, name: str) -> bool:
        return any(obj.name == name for obj in self.references)

    def is_in_referenced_by(self, name: str) -> bool:
        return any(obj.name == name for obj in self.referenced_by)

    def add_reference(self, obj):
        if not self.is_in_references(obj.name):
            self.references.append(obj)

    def add_referenced_by(self, obj):
        if not self.is_in_referenced_by(obj.name):
            self.referenced_by.append(obj)

class GlobalContext:
    def __init__(self, stack = []):
        self.stack = stack
        self.definitions = {}

    def __getitem__(self, key):
        return self.definitions[key]

    def add_definition(self, obj):
        if isinstance(obj, ContextObj):
            if obj.name in self.definitions.keys():
                raise Exception('A definition with this name already exists')
            self.definitions[obj.name] = obj
            return
        raise Exception('Code definitions must be encapsulated in a ContextObj')

    def add_context(self, name):
        if name in self.definitions:
            if name in self.stack:
                return
            self.stack.append(name)
            return
        raise Exception('Context added must be in the definitions dictionary')
    def del_context(self, name):
        if name in self.stack:
            self.stack.remove(name)
            
    def items(self):
        for name, obj in self.definitions.items():
            yield name, obj.code_def
