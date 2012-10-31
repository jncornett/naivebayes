from math import log, exp
from collections import defaultdict
import re

WORDS = re.compile(r'\b\w+\b')

class SpamFilter(object):
    def __init__(self, training_data=None, data=None):
        self.data = data or {0:defaultdict(int), 1:defaultdict(int)}
        self.counts = 0
        if training_data: self.train(training_data)

    def train(self, training_data):
        for category, message in training_data:
            cur_dict = self.data[int(category)]
            words = WORDS.findall(message.lower())
            for word in words:
                cur_dict[word] += 1
            self.counts += len(words)

    def score(self, category, message):
        logprobs = []
        for word in WORDS.findall(message.lower()):
            k, kc = self.data[category].get(word, 1), self.data[not category].get(word, 1)
            p = k / float(k + kc)
            logprobs.append(log(1 - p) - log(p))
        
        try:
            return 1 / (1 + exp(sum(logprobs)))
        except OverflowError:
            return 0.0

if __name__ == '__main__':
    training_data = [
        [0, "Spammy spammy spam message about viagra and stuff"],
        [1, "A very serious message about work and stuff"],
        [0, "More viagra, and a little bit of porn"],
        [1, "Some one is trying to sell me some serious spam"]
        ]

    filter = SpamFilter(training_data)

    messages = zip(*training_data)[1]

    for message in messages:
        print "Message:"
        print message
        print "Spam probability:", filter.score(0, message)
        print
