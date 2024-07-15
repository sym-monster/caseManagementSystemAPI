# -*- coding: utf-8 -*-
# @Author  : Liqiju
# @Time    : 2022/5/1 2:45
# @File    : app.py
# @Software: PyCharm

import pymysql
from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

pymysql.install_as_MySQLdb()

app = Flask(__name__)
# ------------------database----------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sym:100200@117.50.199.3:3306/case_management_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class CaseManagements(db.Model):
    id = db.Column(db.Integer, primary_key=True, comment='自动递增id，唯一键')
    name = db.Column(db.String(80), nullable=False, comment='姓名')
    gender = db.Column(db.String(120), nullable=False, comment='性别')
    time = db.Column(db.String(120), nullable=False, comment='时间')
    region = db.Column(db.String(120), nullable=False, comment='地址')
    telephone = db.Column(db.String(120), nullable=False, comment='电话')
    sensitives = db.Column(db.String(120), nullable=False, comment='过敏原')
    delivery = db.Column(db.String(120), nullable=False, comment='是否初次就诊')
    diagnose = db.Column(db.String(120), nullable=False, comment='诊断')
    desc = db.Column(db.String(120), nullable=False, comment='处方')


# 增加数据
def insert_data(name, gender, time, region, telephone, sensitives, delivery, diagnose, desc):
    with app.app_context():
        caseManagement = CaseManagements(name=name, gender=gender, time=time, region=region, telephone=telephone,
                               sensitives=sensitives,delivery=delivery, diagnose=diagnose, desc=desc)
        db.session.add(caseManagement)
        db.session.commit()


# 查询所有
def select_data_all():
    with app.app_context():
        caseManagement_list = []
        caseManagements = CaseManagements.query.all()
        for c in caseManagements:
            caseManagement_list.append({
                'id': c.id,
                'name': c.name,
                'gender': c.gender,
                'time': c.time,
                'region': c.region,
                'telephone': c.telephone,
                'sensitives': c.sensitives,
                'delivery': c.delivery,
                'diagnose': c.diagnose,
                'desc': c.desc
            })
        return caseManagement_list

def select_data_by_name(name):
    with app.app_context():
        caseManagements = CaseManagements.query.filter(CaseManagements.name == name).all()
        if caseManagements:
            results = []
            for caseManagement in caseManagements:
                results.append({
                    'id': caseManagement.id,
                    'name': caseManagement.name,
                    'gender': caseManagement.gender,
                    'time': caseManagement.time,
                    'region': caseManagement.region,
                    'telephone': caseManagement.telephone,
                    'sensitives': caseManagement.sensitives,
                    'delivery': caseManagement.delivery,
                    'diagnose': caseManagement.diagnose,
                    'desc': caseManagement.desc
                })
            return results
        return None

# 通过id删除数据
def delete_data(id):
    with app.app_context():
        caseManagement = CaseManagements.query.get(id)
        if caseManagement:
            db.session.delete(caseManagement)
            db.session.commit()
            return True
        return False


# 修改数据
def update_data(id, name=None, gender=None, time=None, region=None, telephone=None, sensitives=None, delivery=None, diagnose=None, desc=None):
    with app.app_context():
        caseManagement = CaseManagements.query.get(id)
        if caseManagement:
            if name:
                caseManagement.name = name
            if gender:
                caseManagement.gender = gender
            if time:
                caseManagement.time = time
            if region:
                caseManagement.region = region
            if telephone:
                caseManagement.telephone = telephone
            if sensitives:
                caseManagement.sensitives = sensitives
            if delivery:
                caseManagement.delivery = delivery
            if diagnose:
                caseManagement.diagnose = diagnose
            if desc:
                caseManagement.desc = desc
            db.session.commit()
            return True
        return False


@app.after_request
def after(resp):
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'  # 允许跨域地址
    resp.headers['Access-Control-Allow-Methods'] = '*'  # 请求 ‘*’ 就是全部
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'  # 头部
    resp.headers['Access-Control-Allow-Credentials'] = 'True'
    return resp


CORS(app, resources=r'/*', supports_credentials=True)


@app.route('/api/add', methods=['POST'])
def add():
    response_object = {'status': 'success'}
    post_data = request.get_json()

    name = str(post_data.get('name')).strip()
    gender = str(post_data.get('gender')).strip()
    time = str(post_data.get('time')).strip()
    region = str(post_data.get('region')).strip()
    telephone = str(post_data.get('telephone')).strip()
    sensitives = str(post_data.get('sensitives')).strip()
    delivery = str(post_data.get('delivery')).strip()
    diagnose = str(post_data.get('diagnose')).strip()
    desc = str(post_data.get('desc')).strip()


    insert_data(name, gender, time, region,telephone, sensitives, delivery, diagnose, desc)
    response_object['message'] = '病历添加成功!'
    return jsonify(response_object)


@app.route('/api/delete', methods=['DELETE'])
def delete():
    response_object = {'status': 'success'}
    post_data = request.get_json()

    if not post_data.get('id'):
        response_object['message'] = 'id是必传参数!'
        response_object["status"] = 'fail'
        return jsonify(response_object)

    if delete_data(post_data.get('id')):
        response_object['message'] = '病历已删除!'
    else:
        response_object['message'] = '需要删除的病历不存在!'
        response_object["status"] = 'fail'
    return jsonify(response_object)


@app.route('/api/update', methods=['POST'])
def update():
    response_object = {'status': 'success'}
    post_data = request.get_json()

    if update_data(post_data.get('id'), post_data.get('name'), post_data.get('gender'), post_data.get('time'), post_data.get('region'),
                   post_data.get('telephone'), post_data.get('sensitives'), post_data.get('delivery'), post_data.get('diagnose'), post_data.get('desc')):
        response_object['message'] = '病历已更新!'
    else:
        response_object['message'] = '需要修改的病历不存在!'
        response_object["status"] = 'fail'
    return jsonify(response_object)


@app.route('/api/query', methods=['POST'])
def query():
    response_object = {'status': 'success'}
    post_data = request.get_json()

    if not post_data.get('name'):
        caseManagements = select_data_all()
        response_object['message'] = '查询所有病历成功!'
        response_object['caseManagements'] = caseManagements
    else:
        caseManagement = select_data_by_name(post_data.get('name'))
        if caseManagement:
            response_object['message'] = '查询病历成功!'
            response_object['caseManagements'] = caseManagement
        else:
            response_object['message'] = '需要查询的病历不存在!'
            response_object["status"] = 'fail'
    return jsonify(response_object)

# # 获取所有省份
# @app.route('/api/provinces', methods=['GET'])
# def get_provinces():
#     connection = mysql.connector.connect(**db_config)
#     cursor = connection.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM Province")
#     provinces = cursor.fetchall()
#     cursor.close()
#     connection.close()
#     return jsonify(provinces)

if __name__ == '__main__':
    # 创建表（表创建好后可注释掉）
    with app.app_context():
        db.create_all()  # 创建表（表创建好后可注释掉）
    app.run(debug=True, port=8000)
