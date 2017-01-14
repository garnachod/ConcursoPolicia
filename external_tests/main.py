from RecolectorTweetsTagsLang import RecolectorTweetsTagsLang
from FileTweetsWriter import FileTweetsWriter

if __name__ == '__main__':
    writer = FileTweetsWriter("tweets.txt")
    fetcher = RecolectorTweetsTagsLang([writer])

    fetcher.recolecta("consulta")
