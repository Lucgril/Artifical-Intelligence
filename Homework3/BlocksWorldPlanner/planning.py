import nltk
from pyswip import Prolog


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
        # stop_words = set(stopwords.words('english'))
        tokens = nltk.word_tokenize(sentence)
        # tokens_filtered = []

        # for t in tokens:
        #   if t not in stop_words:
        #      tokens_filtered.append(t)

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

    def is_knowledge(self):
        for subtree in self._result.subtrees():
            if subtree.label() == "knowledge":
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
        p_name = None
        name = None
        adj = None

        for token in obj:
            if token[1] == "JJ":
                adj = token[0]
            elif token[1] == "NN":
                p_name = token[0]
            elif token[1] == "NNP":
                name = token[0]

        if adj and name:
            prolog.assertz(adj + "(" + name + ")")

        if name and p_name:
            prolog.assertz(p_name + "(" + name + ")")

    def add_assertion(self):
        obj1 = None
        obj2 = None
        sent = None
        adj = None

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
                            if leaf[1] == "IN":
                                sent = leaf[0]
                            elif leaf[1] == "JJ":
                                adj = leaf[0]

        if sent and obj1 and obj2:
            prolog.assertz(sent + "(" + obj1 + "," + obj2 + ")")

        if adj and obj1:
            prolog.assertz(adj + "(" + obj1 + ")")

    def add_query(self):
        obj1 = None
        obj2 = None
        sent = None
        adj = None

        for subtree in self._result:
            if subtree.label() == "verb_at_the_beginning":
                for object in subtree.subtrees():
                    if object.label() == "object":
                        #result = self.query_object(object)

                        #if result:
                        for leaf in object:
                            if leaf[1] == "NNP" or (leaf[1] == "NN" and (leaf[0] == "table" or (leaf[0] == "block" and obj1 is not None))):
                                if obj1 is None:
                                    obj1 = leaf[0]
                                else:
                                    obj2 = leaf[0]
                            elif leaf[1] == "JJ":
                                adj = leaf[0]
                        #else:
                            #return False

                for rest in subtree.subtrees():
                    if rest.label() != "object":
                        for leaf in rest:
                            if len(leaf) > 1:
                                if leaf[1] == "IN":
                                    sent = leaf[0]
                                elif leaf[1] == "VBD":
                                    adj = leaf[0]
                                elif leaf[1] == "JJ":
                                    adj = leaf[0]

        if sent and obj1 and obj2:
            try:
                return bool(list(prolog.query(sent + "(" + obj1 + "," + obj2 + ")")))
            except Exception:
                return False
        elif obj1 and adj:
            try:
                return bool(list(prolog.query(adj + "(" + obj1 + ")")))
            except Exception:
                return False
        elif obj1 and obj2:
            if obj2 == "block":
                try:
                    return bool(list(prolog.query(obj2 + "(" + obj1 + ")")))
                except Exception:
                    return False

    def query_object(self, object):
        obj = None
        sent = None
        adj = None

        for token in object:
            if token[1] == "JJ":
                adj = token[0]
            elif token[1] == "NN":
                sent = token[0]
            elif token[1] == "NNP":
                obj = token[0]

        if adj and obj:
            try:
                return bool(list(prolog.query(adj + "(" + obj + ")")))
            except Exception:
                return False
        elif sent and obj:
            try:
                return bool(list(prolog.query(sent + "(" + obj + ")")))
            except Exception:
                return False

    def add_command(self):
        obj1 = None
        obj2 = None
        verb = None

        for subtree in self._result:
            if subtree.label() == "verb_at_the_beginning":
                for object in subtree.subtrees():
                    if object.label() == "object":
                        for leaf in object:
                            if leaf[1] == "NNP" or (leaf[1] == "NN" and (leaf[0] == "table")):
                                if obj1 is None:
                                    obj1 = leaf[0]
                                else:
                                    obj2 = leaf[0]

                for rest in subtree.subtrees():
                    if rest.label() != "object":
                        for leaf in rest:
                            if len(leaf) > 1:
                                if leaf[1] == "IN":
                                    verb = leaf[0]

        if verb and obj1 and obj2:
            return verb + "(" + obj1 + "," + obj2 + ")"
        else:
            return None


if __name__ == "__main__":

    planning = Planning()
    prolog = Prolog()
    prolog.consult("rules.pl")

    while True:

        print('Enter your command:')
        command = input()

        planning.process(command)
        objects = planning.get_objects()

        if planning.is_knowledge():
            for object in objects:
                planning.add_object(object)
            planning.add_assertion()
        elif planning.is_query():
            result = planning.add_query()
            if result is None:
                print("False. Your sentence may be not correct")
            else:
                print("The answer is: " + str(result))
        else:
            if planning.is_command():
                result = planning.add_command()

                if result is not None:
                    print('GOAL: ' + result)
                    res = True
                    try:
                        list(prolog.query("do([" + result + "])"))
                        if bool(list(prolog.query(result))):
                            print("Goal reached!")
                        else:
                            print("Please require a correct action.")
                            res = False
                    except Exception:
                        print("Sorry, I am unable to satisfy your request.")
                else:
                    print("Your sentence does not seem to be correct.")
            else:
                print("Your sentence does not seem to be correct.")
