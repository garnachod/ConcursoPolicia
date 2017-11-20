from DBbridge.ConsultasCassandra import ConsultasCassandra
import codecs

if __name__ == '__main__':

    cq = ConsultasCassandra()
    i = 0
    with codecs.open("millon_tweets.txt", "w", "utf-8") as f_out:
        for tweet in cq.getTweetsTextAndLangAndID('es', limit=1000000):
            f_out.write(str(i) + ";")
            f_out.write(str(tweet.id_twitter) + ";")
            text = tweet.status.replace("\n", ". ").replace("\r", ". ").replace(u"\u0085", ". ").replace(u"\u2028", ". ").replace(u"\u2029", ". ").replace(";", ",")
            f_out.write(text + u"\n")
            i += 1

