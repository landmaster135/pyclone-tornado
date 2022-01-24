from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import *

tokenizer = Tokenizer()

sentenses = ["AIで自分好みの美少女イラストを作れる「Waifu Labs」の開発者が「AIが俺の嫁を作る方法」を解説 - "]
token_filters = [POSKeepFilter(['名詞']), TokenCountFilter()]
analyzer = Analyzer(token_filters=token_filters)

tokenCountList = []

for sentence in sentenses:
    for k, v in analyzer.analyze(sentence):
        print("=============================================")
        print('%s: %d' % (k, v))
        tokenCountList.append([k, v])
    
print(tokenCountList)
    
#     print("=============================================")
#     print("=============================================")
#     print(sentence)
#     for token in tokenizer.tokenize(sentence):
#         print("    " + str(token))
