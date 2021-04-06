from main import app, path_root
from flask import render_template, request, json, Flask, jsonify
import web_app.routes_scripts.scripts as scenario


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        try:
            scenario.generateProject(request.files['file'])
        except:
            print('Error in generate project')
        return render_template('index.html')

app.run(host='172.18.107.167')
