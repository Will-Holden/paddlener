from . import inf_restful
from flask import Flask, request, jsonify
import json
from werkzeug.utils import secure_filename
from settings import BASE_DIR
from core.ernie import ner
from core.ernie_huodong import huodong_ner
import datetime
import re
import os


# @inf_restful.route("/distinct", methods=['POST'])
# def inf():
#     if request.method == 'POST':
#         data = request.form['content']
#         not_replicate = distinct_task.add(data)
#         if not_replicate:
#             result = {'result': 'true'}
#         else:
#             result = {'result': 'false'}
#         return json.dumps(result, ensure_ascii=False)

@inf_restful.route('/huodong_ner', methods=['POST'])
def huodong_ner_func():
    if request.method == 'POST':
        data = request.form['content']
        tags = huodong_ner(data)
        result = {
            'result': tags
        }
        return json.dumps(result, ensure_ascii=False)


@inf_restful.route("/ner", methods=['POST'])
def ner_func():
    if request.method == 'POST':
        data = request.form['content']
        tags = ner(data)
        result = {
            'result': tags
        }
        return json.dumps(result, ensure_ascii=False)

@inf_restful.route("/status", methods=["GET"])
def info():
    result = {'name': 'server',
              'state': 'running'}
    return json.dumps(result, ensure_ascii=False)
