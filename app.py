from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from config.config import Config
from work_sql import SqlDb

# 应用对象
app = Flask(__name__)
jwt = JWTManager(app=app)

app.config.from_object(Config)


# 用户注册
@app.route('/user/register/', methods=['POST'])
def register():
    # 初始化数据库对象
    sql = SqlDb()
    sql.db = sql.init_db()
    sql.cursor = sql.db.cursor()

    # 获取用户信息
    username = request.args.get('username')
    password = request.args.get('password')
    # print(username, password)
    # print(sql.sel_db(username))

    # 存储用户信息
    if sql.sel_db_user(username) is None:
        sql.ins_db_user(username, password)
        # 关闭数据库
        sql.close_db()
        return jsonify({"code": 200, "msg": "success"})
    else:
        # 关闭数据库
        sql.close_db()
        return jsonify({"code": 400, "msg": "用户已存在"}), 400


@app.route('/user/login/', methods=['POST'])
def login():
    # 初始化数据库对象
    sql = SqlDb()
    sql.db = sql.init_db()
    sql.cursor = sql.db.cursor()
    # 获取用户信息
    username = request.args.get('username')
    password = request.args.get('password')

    # 获取token
    if sql.check_user(username, password):
        access_token = create_access_token(identity=username)
        # 关闭数据库
        sql.close_db()
        return jsonify({"code": 200, "msg": "success", "username": username, "token": access_token}), 200
    else:
        # 关闭数据库
        sql.close_db()
        return jsonify({"code": 401, "msg": "Failed"}), 401


@app.route('/task', methods=['POST'])
@jwt_required()
def create_task():
    # 初始化数据库对象
    sql = SqlDb()
    sql.db = sql.init_db()
    sql.cursor = sql.db.cursor()
    # 获取任务信息
    title = request.args.get('title')
    content = request.args.get('content')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    status = request.args.get('status')

    # 从token获取用户
    current_user = get_jwt_identity()

    sql.ins_task(dict(title=title, content=content, start_time=start_time, end_time=end_time, status=status,
                      user=current_user))
    # 关闭数据库
    sql.close_db()
    return jsonify({"code": 200, "msg": "success"}), 200


@app.route('/task', methods=['GET'])
@jwt_required()
def get_task():
    # 初始化数据库对象
    sql = SqlDb()
    sql.db = sql.init_db()
    sql.cursor = sql.db.cursor()

    status = request.args.get('status')
    current_user = get_jwt_identity()

    data = sql.sel_task(current_user, status)

    # 关闭数据库
    sql.close_db()

    return jsonify({"code": 200, "msg": "success", "data": data}), 200


@app.route('/task/<id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    # 初始化数据库对象
    sql = SqlDb()
    sql.db = sql.init_db()
    sql.cursor = sql.db.cursor()

    status = request.form.get('status')
    current_user = get_jwt_identity()

    if sql.update_task(id, status, current_user):
        # 关闭数据库
        sql.close_db()
        return jsonify({"code": 200, "msg": "success"}), 200
    else:
        # 关闭数据库连接
        sql.close_db()
        return jsonify({"code": 400, "msg": "the task isnot found"}), 400


@app.route('/task/<id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    # 初始化数据库对象
    sql = SqlDb()
    sql.db = sql.init_db()
    sql.cursor = sql.db.cursor()

    current_user = get_jwt_identity()
    if sql.del_task(id, current_user):
        # 关闭数据库
        sql.close_db()
        return jsonify({"code": 200, "msg": "sucess"}), 200
    else:
        sql.close_db()
        return jsonify({"code": 400, "msg": "the task isnot found"}), 400


@app.route("/")
def hello():
    return "Hello world"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
