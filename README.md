# VibeCodePy
Write Python code like it already exists. Automatically creates classes and methods at runtime, powered by vibe coding + AI. No errors, no boilerplate, just flow. (Currently in alpha: class/method creation only.)

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
Set the API key and the URL for the server.
 ``` python
vibe.API = 'your-api-key'
vibe.URL = 'your-url'
```
Connect to the LLM
 ``` python
vibe.connect_llm()
```
To create a class:
 ``` python
obj = vibe.cls('Class_name', descr, attrs = {})
```
* descr - the docstring of the class that also serves as it's description
* attrs - dictionary of the class' attributes, the keys are the attributes and the values will be used to initialize the instance obj
  
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

vibe.API = 'your-api-key'
vibe.URL = 'your-url'
vibe.connect_llm()

descr = '''
    A class to test a string.
    When initialized, an object of this class will print "Received string: {string}"
    It has 2 methods:
    is_long() - checks if the string is longer than 100 characters
    is_Shakespeare() - checks if the string is a famous quote from Shakespeare
'''
n = vibe.cls('Test', descr, attrs = {'string' : 'Et tu Brutus?'})
print(n.__doc__)
print(n.a((1, 2), 2.34e10, 1, 'abcd', 'a, b, c, {2}', {1: 3, 3: 4}, (4, 5))) # Returns the closest element to the string in terms of hash value some parameters might not be hashable
print(n.a)
vibe.save('test_module.py')
```
