import os
import re

class ProfanityFilter(object):

    PROFANITY_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                "profanity_words.txt")

    def __init__(self, ignorecase=True, insidewords=True,replacement="@!~*$%"):

        self.replacement = replacement
        self.ignorecase = ignorecase
        self.inside_words = insidewords
        #Get profanity words

        if os.path.exists(Profanity Filter.PROFANITY_FILE_PATH):
            with open(ProfanityFilter.PROFANITY_FILE_PATH, "r") as prof:
                self.profanity_words = [w.strip("\n") for w in prof.readlines()]
        else:
            print("Missing profanity file")

    def replace_text(self, text_message):

        regex_inside = {
            True: r'(%s)',
            False: r'\b(%s)\b'
        }
        regex_pattern = (regex_inside[self.inside_words] %
                                    '|'.join(self.profanity_words))
        r = re.compile(regex_pattern, re.IGNORECASE if self.ignorecase else 0)
        return r.sub(self.replacement, text_message)
