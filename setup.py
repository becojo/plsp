from setuptools import setup

setup(name='plsp',
      version='0.1',
      description='Lisp compiled to Python',
      url='http://github.com/becojo/plsp',
      author='Becojo',
      author_email='benoit@bcj.io',
      license='GPLv3',
      packages=['plsp'],
      zip_safe=False,
      scripts=['bin/plsp']
      install_requires=['BytecodeAssembler==0.6'])
