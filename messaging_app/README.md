# 0x00. Python - Variable Annotations

tags: Python Back-end

## Resources

## Objectives

## Tasks

### 0. Basic annotations - add

- Write a type-annotated function add that takes a float a and a float b as arguments and returns their sum as a float.

```bash
bob@dylan:~$ cat 0-main.py
#!/usr/bin/env python3
add = __import__('0-add').add

print(add(1.11, 2.22) == 1.11 + 2.22)
print(add.__annotations__)

bob@dylan:~$ ./0-main.py
True
{'a':  <class 'float'>, 'b': <class 'float'>, 'return': <class 'float'>}
```

Repo:

GitHub repository: alx-backend-python
Directory: 0x00-python_variable_annotations
File: 0-add.py
