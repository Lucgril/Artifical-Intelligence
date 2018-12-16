import nltk
from nltk.corpus import stopwords


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
        stop_words = set(stopwords.words('english'))
        tokens = nltk.word_tokenize(sentence)
        tokens_filtered = []

        for t in tokens:
            if t not in stop_words:
                tokens_filtered.append(t)

        print(tokens_filtered)

        tagged = nltk.pos_tag(tokens_filtered)
        self._result = self._chunker.cp(tagged)

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
