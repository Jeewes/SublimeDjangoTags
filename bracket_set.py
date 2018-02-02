class BracketSet(object):
    """
    Base class for rotatable set of brackets.
    """
    brackets = []

    def __init__(self):
        self.index = 0

    @property
    def openers(self):
        """Get array of opening brackets"""
        return [pair[0] for pair in self.brackets]

    @property
    def closers(self):
        """Get array of closing brackets"""
        return [pair[1] for pair in self.brackets]

    def _find_from_text(self, brackets, text, find_func='find'):
        for bracket in sorted(brackets, key=len, reverse=True):
            index = getattr(text, find_func)(bracket)
            if index >= 0:
                return index, bracket
        return -1, ""

    def find_opener_from_text(self, text):
        """
        Find opening bracket from given text.

        Return:
            Int, String: Index of the substr and matched bracket,
            -1 and "" if no match
        """
        return self._find_from_text(self.openers, text, 'rfind')

    def find_closer_from_text(self, text):
        """
        Find closing bracket from given text.

        Return:
            Int, String: Index of the substr and matched bracket,
            -1 and "" if no match
        """
        return self._find_from_text(self.closers, text)

    def __getitem__(self, key):
        return self.brackets[key]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.brackets):
            raise StopIteration
        else:
            self.index += 1
            return self.brackets[self.index - 1]

    def __len__(self):
        return len(self.brackets)
