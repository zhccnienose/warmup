import pymysql


class SqlDb:

    def __init__(self):
        self.db = None
        self.cursor = None

    # 连接数据库
    def init_db(self):
        self.db = pymysql.connect(host="47.115.212.55",
                                  user="root",
                                  password="123456",
                                  database="west2")

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

    def _check_task_(self, id, user):
        exist_task = '''SELECT ID FROM `task` WHERE USER = %s AND ID = %s LIMIT 0,1'''

        number = self.cursor.execute(exist_task, (user, id))
        return number

    # 更新任务完成状态
    def update_task(self, id, status, user):
        # 所更新的任务存在
        if self._check_task_(id, user) == 1:
            update_task = '''UPDATE `task` SET STATUS = %s WHERE ID= %s AND user = %s '''
            self.cursor.execute(update_task, (status, id, user))
            self.db.commit()
            return True
        else:
            return False

    # 删除任务
    def del_task(self, id, user):

        if self._check_task_(id, user) == 1:
            # 删除任务
            del_task = '''DELETE FROM `task` WHERE ID = %s AND user = %s'''
            self.cursor.execute(del_task, (id, user))
            self.db.commit()
            # 更新任务序号
            update_id = '''UPDATE `task` SET ID = ID-1 WHERE ID > %s AND user = %s '''
            self.cursor.execute(update_id,(id, user))
            self.db.commit()
            return True
        else:
            return False

    # 关闭数据库
    def close_db(self):
        self.cursor.close()
        self.db.close()
