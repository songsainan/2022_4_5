import pymysql


class HandleDB:
    def __init__(self, host, port, user, password):
        self.con = pymysql.Connect(host=host,
                                   port=port,
                                   user=user,
                                   password=password,
                                   charset='utf8')

    def find_all(self, sql):
        with self.con.cursor() as cur:
            cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        return res

    # def find_one(self, sql):
    #     cur = self.con.cursor()
    #     cur.execute(sql)
    #     res = cur.fetchone()
    #     cur.close()
    #     return res

    def find_one(self, sql):
        with self.con:
            with self.con.cursor() as cur:
                cur.execute(sql)
                res = cur.fetchone()
                cur.close()
                return res

    def __del__(self):
        self.con.close()
        print('数据库连接已关闭')


if __name__ == '__main__':
    from common.handle_conf import confger

    db = HandleDB(host=confger.get('mysql', 'host'),
                  port=confger.getint('mysql', 'port'),
                  user=confger.get('mysql', 'user'),
                  password=confger.get('mysql', 'password')
                  )
    res = db.find_one('select leave_amount from future.member where mobile_phone = 15144440000')[0]
    amount = float(res)
    print(amount)
