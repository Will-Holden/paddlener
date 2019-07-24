from . import inf_restful
from flask import Flask, request, jsonify
import json
from werkzeug.utils import secure_filename
from settings import BASE_DIR
import datetime
import re
import os
from core.tasks.DistinctTask import DistinctTask
distinct_task = DistinctTask.instance()


@inf_restful.route("/distinct", methods=['POST'])
def inf():
    if request.method == 'POST':
        data = request.form['content']
        not_replicate = distinct_task.add(data)
        if not_replicate:
            result = {'result': 'true'}
        else:
            result = {'result': 'false'}
        return json.dumps(result, ensure_ascii=False)
