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


# 通过id查询
def select_data_by_id(id):
    with app.app_context():
        caseManagement = CaseManagements.query.get(id)
        if caseManagement:
            return {
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
            }
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
def update_data(id, title=None, author=None, read_status=None):
    with app.app_context():
        caseManagement = CaseManagements.query.get(id)
        if caseManagement:
            if title:
                caseManagement.title = title
            if author:
                caseManagement.author = author
            if read_status is not None:
                caseManagement.read_status = read_status
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
    response_object['message'] = '图书添加成功!'
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
        response_object['message'] = '图书被删除!'
    else:
        response_object['message'] = '需要删除的图书不存在!'
        response_object["status"] = 'fail'
    return jsonify(response_object)


@app.route('/api/update', methods=['POST'])
def update():
    response_object = {'status': 'success'}
    post_data = request.get_json()

    if not post_data.get('id'):
        response_object['message'] = 'id是必传参数!'
        response_object["status"] = 'fail'
        return jsonify(response_object)

    if not post_data.get('title'):
        response_object['message'] = 'title是必传参数!'
        response_object["status"] = 'fail'
        return jsonify(response_object)

    if not post_data.get('author'):
        response_object['message'] = 'author是必传参数!'
        response_object["status"] = 'fail'
        return jsonify(response_object)

    if post_data.get('read_status') not in [0, 1]:
        response_object['message'] = '阅读状态只能为0和1!'
        response_object["status"] = 'fail'
        return jsonify(response_object)

    if update_data(post_data.get('id'), post_data.get('title'), post_data.get('author'), post_data.get('read_status')):
        response_object['message'] = '图书已更新!'
    else:
        response_object['message'] = '需要修改的书籍id不存在!'
        response_object["status"] = 'fail'
    return jsonify(response_object)


@app.route('/api/query', methods=['POST'])
def query():
    response_object = {'status': 'success'}
    post_data = request.get_json()

    if not post_data.get('id'):
        caseManagements = select_data_all()
        response_object['message'] = '查询所有书籍成功!'
        response_object['caseManagements'] = caseManagements
    else:
        caseManagement = select_data_by_id(post_data.get('id'))
        if caseManagement:
            response_object['message'] = '查询书籍成功!'
            response_object['caseManagements'] = caseManagement
        else:
            response_object['message'] = '需要查询的图书不存在!'
            response_object["status"] = 'fail'
    return jsonify(response_object)


if __name__ == '__main__':
 # 创建表（表创建好后可注释掉）
    app.run(debug=True, port=8000)
