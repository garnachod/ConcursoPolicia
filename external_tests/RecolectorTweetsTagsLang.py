from SocialAPI.TwitterAPI.RecolectorTweetsTags import RecolectorTweetsTags


class RecolectorTweetsTagsLang(RecolectorTweetsTags):
    def privateRealizaConsulta(self, query, maxi=0, mini=0):
        if self.authorizator.is_limit_api(self.tipo_id):
            raise Exception('LIMITE')

        try:
            if maxi == 0 and mini == 0:
                retorno = self.twitter.search(q=query, lang="es", count='100', result_type="recent")
            elif maxi == 0 and mini > 0:
                retorno = self.twitter.search(q=query, lang="es", since_id=mini, count='100', result_type="recent")
            elif maxi > 0 and mini == 0:
                retorno = self.twitter.search(q=query, lang="es", max_id=maxi, count='100', result_type="recent")
            else:
                retorno = self.twitter.search(q=query, lang="es", max_id=maxi, since_id=mini, count='100', result_type="recent")

            self.authorizator.add_query_to_key(self.tipo_id)
            # print retorno
            return retorno["statuses"]

        except Exception, e:
            print e
            self.authorizator.add_query_to_key(self.tipo_id)
            if "429" in str(e):
                raise Exception('LIMITE')
            return []