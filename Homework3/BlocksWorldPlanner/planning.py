import nltk
from nltk.corpus import stopwords
#import pyswip


class Planning:

    def __init__(self):
        # Define a chunk "grammar", i.e. chunking rules
        self._grammar = r"""
            object: {<DT>?<JJ>?<NN><NNP>?|<NNP>}
            verb_at_the_beginning: {^<VB.?><.+>+}
            knowledge: {<object><VB.?>|<EX><VB.?><DT>?<object>}
            knowledge_assertion: {<knowledge><IN>?<DT>?<object>|<knowledge><JJ>}
        """
        self._chunker = nltk.RegexpParser(self._grammar)
        self._result = None

    def process(self, sentence):
        #stop_words = set(stopwords.words('english'))
        tokens = nltk.word_tokenize(sentence)
        #tokens_filtered = []

        #for t in tokens:
         #   if t not in stop_words:
          #      tokens_filtered.append(t)

        print(tokens)

        tagged = nltk.pos_tag(tokens)
        self._result = self._chunker.parse(tagged)

    def is_query(self):
        for subtree in self._result.subtrees():
            if subtree.label() == "verb_at_the_beginning" and subtree.leaves()[-1][0] == "?":
                return True
        return False

    def is_command(self):
        for subtree in self._result.subtrees():
            if subtree.label() == "verb_at_the_beginning" and subtree.leaves()[-1][0] != "?":
                return True
        return False

    def is_assertion(self):
        for subtree in self._result.subtrees():
            if subtree.label() == "knowledge_assertion":
                return True
        return False

    def get_objects(self):
        objects = []
        for subtree in self._result.subtrees():
            obj = []
            for leave in subtree.leaves():
                obj.append(leave)
            objects.append(obj)
        return objects

    def add_object(self, obj):
        p_noun = None
        noun = None
        adj = None

        for token in obj:
            if token[1] == "JJ":
                adj = token[0]
            elif token[1] == "NN":
                noun = token[0]
            elif token[1] == "NNP":
                p_noun = token[0]

        if adj and noun:
            #prolog.assertz(adj + "(" + noun + ")")
            print("si")

        if p_noun and noun:
            #prolog.assertz(p_noun + "(" + noun + ")")
            print("no")

    def add_assertion(self):
        obj1 = None
        obj2 = None
        sent = None
        adj = None
        print(self._result)
        for subtree in self._result:
            if subtree.label() == "knowledge_assertion":
                for knowledge in subtree.subtrees():
                    if knowledge.label() == "knowledge":
                        for object in knowledge.subtrees():
                            if object.label() == "object":
                                for leaf in object.leaves():
                                    if leaf[1] == "NNP":
                                        if obj1 is None:
                                            obj1 = leaf[0]
                                        else:
                                            obj2 = leaf[0]
                                    elif leaf[1] == "NN":
                                        obj2 = leaf[0]

                for object in subtree.subtrees():
                    if knowledge.label() == "object":
                        for leaf in object.leaves():
                            if leaf[1] == "NNP":
                                if leaf[0] is not obj1:
                                    obj2 = leaf[0]
                            elif leaf[1] == "NN":
                                if leaf[0] is not obj1:
                                    obj2 = leaf[0]

                for rest in subtree.subtrees():
                    if rest.label() != "knowledge" and rest.label() != "object":
                        for leaf in rest.leaves():
                            print("leaf" + str(rest))
                            if leaf[1] == "IN":
                                sent = leaf[0]
                            elif leaf[1] == "JJ":
                                adj = leaf[0]

        if sent and obj1 and obj2:
            print("ciao")
            # prolog.assertz(sent + "(" + obj1 + "," + "obj2" + ")")


        if adj and obj1:
            print("si")
            # prolog.assertz(adj + "(" + noun + ")")



        print(obj1)
        print(obj2)
        print(sent)
        print(adj)

    def add_query(self):
        obj1 = None
        obj2 = None
        sent = None
        adj = None
        print(self._result)
        for subtree in self._result:
            if subtree.label() == "verb_at_the_beginning":
                for object in subtree.subtrees():
                    if object.label() == "object":
                        for leaf in object.leaves():
                            print("leaf" + str(leaf))
                            if leaf[1] == "NNP":
                                if obj1 is None:
                                    obj1 = leaf[0]
                                else:
                                    obj2 = leaf[0]
                            elif leaf[1] == "NN":
                                obj2 = leaf[0]

                for rest in subtree.subtrees():
                    if rest.label() != "object":
                        for leaf in rest.leaves():
                            print("leaf2" + str(leaf))
                            if leaf[1] == "IN":
                                sent = leaf[0]
                            elif leaf[1] == "VBD":
                                adj = leaf[0]
                            elif leaf[1] == "JJ":
                                adj = leaf[0]

        if sent and obj1 and obj2:
            try:
                print("ciao")
                #return bool(list(prolog.query(sent + "(" + obj1 + "," + obj2 + ")")))
            except Exception:
                return False
        elif obj1 and adj:
            try:
                print("ciao")
                #return bool(list(prolog.query(adj + "(" + obj1 + ")")))
            except Exception:
                return False
        elif obj1 and obj2:
            if obj2 == "block":
                try:
                    print("ciao")
                    #return bool(list(prolog.query(obj2 + "(" + obj1 + ")")))
                except Exception:
                    return False

        print(obj1)
        print(obj2)
        print(sent)
        print(adj)

prova = Planning()
#prolog = pyswip.Prolog()
#prolog.consult("rules.pl")

prova.process("is B a red block")
prova.add_query()
