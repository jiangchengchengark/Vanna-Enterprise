from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from userVanna import userVanna
import uuid
import logging
import threading
import json
import os
local_adress=os.getenv('LOCAL_ADRESS')
app = Flask(__name__)
app.secret_key = '1345456'  # 设置一个秘密密钥用于会话加密

# 配置日志记录
logging.basicConfig(level=logging.DEBUG)

# 存储实例的字典
instances = {}

# 存储预训练日志的字典
pre_training_logs = {}

# 预训练信息文件路径
PRE_TRAINED_FILE = 'pre_trained.json'

def load_pre_trained_info():
    if os.path.exists(PRE_TRAINED_FILE):
        with open(PRE_TRAINED_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_pre_trained_info(info):
    with open(PRE_TRAINED_FILE, 'w') as f:
        json.dump(info, f)

@app.before_request
def before_request():
    session['ip'] = request.remote_addr

@app.route('/')
def welcome():
    ip = session.get('ip')
    pre_trained_info = load_pre_trained_info()
    sql_name = session.get('sql_name')
    db_name = session.get('db_name')
    if ip and sql_name and db_name and pre_trained_info.get(ip, {}).get(sql_name, {}).get(db_name, False):
        return redirect(url_for('view_instance'))
    return render_template('welcome.html')

@app.route('/select_db', methods=['POST'])
def select_db():
    sql_name = request.form['sql_name']
    session['sql_name'] = sql_name
    return render_template(f'select_db_{sql_name}.html')

@app.route('/generate', methods=['POST'])
def generate():
    sql_name = session.get('sql_name')
    ip = session.get('ip')
    pre_trained_info = load_pre_trained_info()

    if sql_name == 'mysql':
        host = request.form['host']
        dbname = request.form['dbname']
        user = request.form['user']
        password = request.form['password']
        port = request.form['port']
        instance = userVanna(sql_name, user_id=ip)
        try:
            port = int(port)  # 将端口从字符串转换为整数
        except ValueError:
            return "端口应为 int 类型"
        instance.connect(host=host, dbname=dbname, user=user, password=password, port=port)
        session['db_name'] = dbname
    elif sql_name == 'sqlite':
        adress = request.form['adress']
        port = request.form['port']
        try:
            port = int(port)  # 将端口从字符串转换为整数
        except ValueError:
            return "端口应为 int 类型"
        dbname = request.form['dbname']
        instance = userVanna(sql_name, user_id=ip)
        instance.connect(adress=adress, port=port, dbname=dbname)
        session['db_name'] = dbname
    elif sql_name == 'snowflake':
        account = request.form['account']
        username = request.form['username']
        password = request.form['password']
        database = request.form['database']
        role = request.form['role']
        instance = userVanna(sql_name, user_id=ip)
        instance.connect(account=account, username=username, password=password, database=database, role=role)
        session['db_name'] = database
    
    instance_id = str(uuid.uuid4())  # 使用UUID作为实例的唯一标识
    instances[instance_id] = instance
    session['instance_id'] = instance_id  # 将会话中的实例标识符存储在会话中

    # 检查预训练状态
    if not pre_trained_info.get(ip, {}).get(sql_name, {}).get(session['db_name'], False):
        pre_training_logs[ip] = []
        # 在单独的线程中启动预训练
        threading.Thread(target=pre_train_async, args=(instance, ip, sql_name, session['db_name'])).start()

    port = instance.start_web_server()
    session['port'] = port

    return redirect(url_for('view_instance'))

def pre_train_async(instance, ip, sql_name, db_name):
    try:
        instance.pre_train(log_callback=lambda log: pre_training_logs[ip].append(log))
        pre_trained_info = load_pre_trained_info()
        if ip not in pre_trained_info:
            pre_trained_info[ip] = {}
        if sql_name not in pre_trained_info[ip]:
            pre_trained_info[ip][sql_name] = {}
        pre_trained_info[ip][sql_name][db_name] = True
        save_pre_trained_info(pre_trained_info)
    except Exception as e:
        logging.error(f"预训练过程中发生错误: {e}")

@app.route('/view')
def view_instance():
    instance_id = session.get('instance_id')
    port = session.get('port')
    if instance_id:
        return render_template('view_instance.html', instance_id=instance_id, port=port,local_adress=local_adress)
    else:
        return "No instance generated", 404

@app.route('/check_pre_training')
def check_pre_training():
    ip = session.get('ip')
    sql_name = session.get('sql_name')
    db_name = session.get('db_name')
    pre_trained_info = load_pre_trained_info()
    if ip and sql_name and db_name and pre_trained_info.get(ip, {}).get(sql_name, {}).get(db_name, False):
        return jsonify({'pre_trained': True})
    return jsonify({'pre_trained': False})

@app.route('/get_pre_training_log')
def get_pre_training_log():
    ip = session.get('ip')
    if ip:
        return jsonify({'log': pre_training_logs.get(ip, [])})
    return jsonify({'log': []})

if __name__ == '__main__':
    app.run(use_reloader=False, threaded=True, debug=True, host='0.0.0.0')








