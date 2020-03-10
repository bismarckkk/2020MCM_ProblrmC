from wordcloud import WordCloud


class wc:
    def __init__(self):
        self.fre = {}
        self.number = 0

    def additem(self, words, theat):
        stop = ['I', 'i', 'and', 'to', 'with', 'for', 'is', 'was', 'in', 'the', 'a', 'on', 'at', 'as', 'do', 'did',
                "I'm", 'are', 'into', 'be', 'by', 'that', 'this', 'it', "It's", 'of', 'been', 'The', 'A', 'an',
                'my', 'me', 'br', 'not', 'you', 'these', 'had', 'return', 'like', 'so', 'have', 'him', 'her', 'since',
                "i'm", 'am', "doesn't", "didn't", 'few', 'got', 'also', 'give', 'think', 'had', 'how', 'his', 'from',
                'when', "it's", 'his', 'she', 'if', 'If', 'NOT', 'away', 'after', 'ago', 'us']
        words = str(words)
        for ch in '!"#$%&()*+,-./:;<=>?@[\\]^_‘{|}~':
            words = words.replace(ch, " ")
        words = words.split(' ')
        temp = {}
        if self.number != 0:
            for key in self.fre:
                temp[key] = self.fre[key] * self.number
        for word in words:
            if not(word in stop):
                if word in temp.keys():
                    temp[word] += theat
                else:
                    temp[word] = theat
        self.number = 0
        for n in temp.values():
            self.number += n
        for key in temp:
            temp[key] /= self.number
        self.fre = temp

    def make(self):
        out = WordCloud(max_words=200,
                        max_font_size=100,
                        width=1500,
                        height=900,
                        background_color='white')
        out.generate_from_frequencies(self.fre)
        return out
