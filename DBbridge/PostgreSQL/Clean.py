from ConexionSQL import ConexionSQL


def clean_api_count():
    conSql = ConexionSQL()
    conn = conSql.getConexion()
    cur = conSql.getCursor()

    query = ('DELETE FROM tokens_count '
    		 'WHERE tiempo < current_timestamp - interval \'15 minutes\''
            ';'
        )
    cur.execute(query)

    query = 'VACUUM FULL tokens_count'
    old_isolation_level = conn.isolation_level
    conn.set_isolation_level(0)
    query = "VACUUM FULL"
    cur.execute(query)
    conn.set_isolation_level(old_isolation_level)

    conn.commit()

    query = 'SELECT count(id) from tokens_count'
    cur.execute(query)
    print "quedan %d tokens_count"%cur.fetchone()[0]

if __name__ == '__main__':
    clean_api_count()