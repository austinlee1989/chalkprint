import pymysql

def local_db_connect(query):
    mysql_cn = pymysql.connect(host='127.0.0.1',
                               port=3306, user='root', passwd='fnwl5r',
                               db='chalkprint')
    return pd.read_sql(query, con=mysql_cn)
