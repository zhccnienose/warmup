import pymysql


class SqlDb:

    def __init__(self):
        self.db = None
        self.cursor = None

    # 连接数据库
    def init_db(self):
        self.db = pymysql.connect(host="47.115.212.55",
                                  user="root",
                                  password="root",
                                  database="west2")

        # self.db = pymysql.connect(host="localhost",
        #                           user="root",
        #                           password="C310257813.",
        #                           database="warmup")

        return self.db

    # 存储用户信息
    def ins_db_user(self, username, password):
        ins_user = '''INSERT INTO `user` (`username`,`password`) VALUES('{}','{}')'''.format(username, password)
        self.cursor.execute(ins_user)
        self.db.commit()

    # 获取用户信息
    def sel_db_user(self, username):
        sel_user = "SELECT * FROM `user` WHERE userNAME = '{}'".format(username)
        self.cursor.execute(sel_user)
        return self.cursor.fetchone()

    def check_user(self, username, password):
        user = self.sel_db_user(username)
        if user is None:
            return False
        else:
            if password == user[1]:
                return True

    # 添加任务
    def ins_task(self, data_task):
        id = self.cursor.execute(
            '''SELECT * FROM `task` WHERE user = '{}' '''.format(data_task['user'])
        )
        print(id)
        ins_task = ('''INSERT INTO `task` 
                    (`ID`, `user`,`TITLE`,`CONTENT`,`START_TIME`,`END_TIME`,`STATUS`) 
                    VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')'''
                    % (id + 1, data_task['user'],
                       data_task['title'], data_task['content'],
                       data_task['start_time'], data_task['end_time'],
                       data_task['status']))
        self.cursor.execute(ins_task)
        self.db.commit()

    # 获取任务信息
    def sel_task(self, user, status):
        sel_task = '''SELECT ID, title, content, start_time, end_time, status  FROM `task` 
                            WHERE user = '{}' AND STATUS = '{}' '''.format(user, status)
        tot = self.cursor.execute(sel_task)
        data = self.cursor.fetchall()

        tname = ('tid', 'title', 'content', 'start_time', 'end_time', 'status')
        data_task = {}
        item = []
        for i in range(1, tot + 1):
            item.append(dict(zip(tname, data[i - 1])))

        data_task.update({"item": item, "total": tot})
        # print(data_task)

        return data_task

    # 更新任务完成状态
    def update_task(self, id, status, user):
        update_task = '''UPDATE `task` SET STATUS = '{}' WHERE ID= '{}' AND user = '{}' '''.format(status, id, user)
        self.cursor.execute(update_task)
        self.db.commit()

    # 删除任务
    def del_task(self, id, user):
        # 删除任务
        del_task = '''DELETE FROM `task` WHERE ID = '{}' AND user = '{}' '''.format(id, user)
        self.cursor.execute(del_task)
        self.db.commit()
        # 更新任务序号
        update_id = '''UPDATE `task` SET ID = ID-1 WHERE ID > '{}' AND user = '{}' '''.format(id, user)
        self.cursor.execute(update_id)
        self.db.commit()

    # 关闭数据库
    def close_db(self):
        self.cursor.close()
        self.db.close()
