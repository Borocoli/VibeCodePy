# VibeCodePy
Write Python code like it already exists. Automatically creates functions, classes and methods at runtime, powered by vibe coding + AI. No errors, no boilerplate, just flow. (Currently in alpha)

## Warning
This project is designed to integrate with LLMs to generate and execute Python code at runtime. The code you write may trigger dynamic, AI-generated code to be created and executed — potentially including malicious or unintended behavior.
* **No LLM is included in this package.** You must provide your own LLM
* **Never run vibecodepy with untrusted or unverified LLMs**, especially those connected to the internet or open to arbitrary prompts.
* **Generated code is executed immediately** — it could contain infinite loops, harmful operations, or data leaks.
* **Do not use this in production, on sensitive data, or in environments where code integrity is critical.**
* This project is **experimental** and intended solely for learning, prototyping, and creative coding.


## Usage
Make sure you have the openai library installed:
```
pip install openai
```

Import the module.
 ``` python
import vibecode as vibe
```
Connect to the LLM
 ``` python
vibe.connect_llm('your-url')
```
Or if you have an API key
 ``` python
vibe.connect_llm('your-url', 'your-api-key', 'model')
```
To create a function:
 ``` python
obj = vibe.f.Function_name(parameters) # Description of the function
```
To create a class:
 ``` python
obj = vibe.c.Class_name(_description=descr, attrs) # Optional comment for more control over the description
```
* descr - the docstring of the class that also serves as it's description
* attrs - class' attributes
  
After the class is created, you can call it's methods, even if they don't exist yet:
 ``` python
obj.unknown_method(parameters) # Use the comment on the same line to explain what it should do
```
To save the generated code use:
``` python
vibe.save(output.py) #Creates / Overwrites output.py
```
Or 
``` python
vibe.save(output.py, 'a') #Appends to output.py
```
### Full Example
``` python
import vibecode as vibe

vibe.connect_llm('your-url')

result_func = vibe.f.closest_hash(1, list(range(10))) # Finds the element from the second parameter, iterable, that has the closest hash value to the first parameter
print(result_func)

descr = '''
    A class to test a string.
    When initialized, an object of this class will print "Received string: {string}"
    It has 2 methods:
    is_long() - checks if the string is longer than 100 characters
    is_Shakespeare() - checks if the string is a famous quote from Shakespeare
'''

n = vibe.c.Test(_description=descr, 'Et tu Brutus?')
print(n.__doc__)
print(n.a((1, 2), 2.34e10, 1, 'abcd', 'a, b, c, {2}', {1: 3, 3: 4}, (4, 5))) # Returns the closest element to the string in terms of hash value some parameters might not be hashable
print(n.a)
vibe.save('module.py', 'w')

```

## Limitations
* In generated classes, the __getattr__ method should not be overwritten/used
* Function and method description is limited to the comment on the same line
* When calling a class for the first time, you must provide the _description parameter, after that it should not be used anymore for creating new objects of that class
* Creation of methods is only available for classes generated using this module
