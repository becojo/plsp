from parser import *

class SemanticAnalyser(DepthFirstAdapter):
    def __init__(self):
        super(SemanticAnalyser, self).__init__()

        self.local_scope = {}

    def inAListAtom(self, node):
        atoms = node.getList().getAtom()
        head = atoms[0]

        if isinstance(head, AIdentifierAtom):
            head_text = head.getIdentifier().getText()

            if head_text == 'defn':
                args = atoms[2].getVector().getAtom()

                for arg in args:
                    self.local_scope.add(arg.getIdentifier.getText())



    def outAListAtom(self, node):
        atoms = node.getList().getAtom()
        head = atoms[0]

        if isinstance(head, AIdentifierAtom):
            head_text = head.getIdentifier().getText()

            if head_text == 'defn':
                args = atoms[2].getVector().getAtom()

                for arg in args:
                    self.local_scope.remove(arg.getIdentifier.getText())

    def inAIdentifierAtom(self, node):
        name = node.getIdentifier().getText()

        if name in self.local_scope:
            node.scope = 'local'
