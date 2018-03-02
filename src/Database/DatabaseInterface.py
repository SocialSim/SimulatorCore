import pymysql.cursors


class DatabaseInterface:

    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                             user='user',
                             password='password',
                             db='githubdb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    def getBaseEventStream(self, eventType):
        result = list()
        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                sql = """SELECT event_base.created_at timestamp, 
                    an_users.login_h userId, an_repos.name_h objectId, 
                    event_base.type eventType FROM actor_link 
                    INNER JOIN event_base ON actor_link.event_id = event_base.id 
                    INNER JOIN an_users ON actor_link.user_id = an_users.id 
                    INNER JOIN an_repos ON actor_link.repo_id = an_repos.id 
                    WHERE event_base.type = %s"""
                cursor.execute(sql, (eventType))
                result = cursor.fetchall()
        finally:
            self.connection.close()
        return result

    def queryDatabase(self, query):
        pass