# plsp

_Lisp for Python_


## Install

```
git clone https://github.com/becojo/plsp
cd plsp
python setup.py install
```

## Usage
### Execute

```
plsp file.plsp
```

### Compile

Plsp compiles to Python bytecode. To send the output to a file, use the `--output` argument.

```
plsp --output file.pyc file.plsp
```

You can then run it directly using Python

```
python file.pyc
```

Or import it a Python script

```python
>>> import file
```


## Hello World Module

```lisp
(defn main []
  (print "Hello World!"))

(ife (== __name__ "__main__")
     (main)
     None)
```
