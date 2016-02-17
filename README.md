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

## Syntax 

<table>
  <tr>
    <th></th>
    <th>Plsp</th>
    <th>Python</th>
  </tr>
  <tr>
    <td>List</td>
    <td><pre><code>[1 2 3]</code></pre></td>
    <td><pre><code>[1, 2, 3]</code></pre></td>
  </tr>
  <tr>
    <td>Dict</td>
    <td><pre><code>{'a' 1 'b' 2 'c' 3}</code></pre></td>
    <td><pre><code>{'a': 1, 'b': 2, 'c': 3}</code></pre></td>
  </tr>
  <tr>
    <td>Lambda</td>
    <td><pre><code>(fn [x] (== x 5)</code></pre></td>
    <td><pre><code>lambda x: x == 5</code></pre></td>
  </tr>
  <tr>
    <td>If</td>
    <td><pre><code>(ife (== password "admin123") 
     (print "Hello admin") 
     (print "Nope"))</code></pre></td>
    <td><pre><code>if password == "admin123":
    print 'Hello admin'
else:
    print 'Nope'</code></pre></td>
  </tr>
  <tr>
    <td>Function</td>
    <td><pre><code>(defn hello [name]
  (print (add "hello " name)))</code></pre></td>
    <td><pre><code>def hello(name):
    print 'hello ' + name</code></pre></td>
  </tr>
</table>
