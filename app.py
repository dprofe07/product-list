import re
import time
from threading import Thread

from bottle import redirect
from flask import Flask, render_template, request

from data_storage import DataStorage
from list_item import ListItem

app = Flask(__name__)
ds = DataStorage("data.dat")
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<identifier>')
def get_list_at(identifier):
    if identifier not in ds.data:
        ds.data[identifier] = []
    return render_template('view_list.html', identifier=identifier, lst=ds.data[identifier])

@app.route('/<identifier>/edit')
def edit_list_at(identifier):
    if identifier not in ds.data:
        ds.data[identifier] = []
    return render_template('edit_list.html', identifier=identifier, lst=ds.data[identifier])


@app.route('/<identifier>/chk_changed')
def on_chk_change(identifier):
    try:
        id_ = int(request.args.get('id'))
        state = int(request.args.get('state'))
    except ValueError:
        id_ = None
        state = None
    if identifier not in ds.data or id_ is None or state is None:
        return '', 400

    ds.data[identifier][id_].checked = bool(state)
    return ''

#spn_changed?id=${idx}&number=${spnIdx}&value=${value}

@app.route('/<identifier>/spn_changed')
def on_spn_change(identifier):
    try:
        id_ = int(request.args.get('id'))
        number = int(request.args.get('number'))
        value = int(request.args.get('value'))
    except ValueError:
        id_ = None
        value = None
        number = None
    if identifier not in ds.data or id_ is None or value is None or number is None:
        return '', 400

    cnt = -1
    def change(m):
        nonlocal cnt
        cnt += 1
        if cnt == number:
            return f'#({value})'
        return m.group()
    ds.data[identifier][id_].text = re.sub(r'#\(\d+\)', change, ds.data[identifier][id_].text)
    print(ds.data[identifier])
    return ''

@app.route('/<identifier>/save_data', methods=['POST'])
def save_data(identifier):
    data = request.data.decode('utf-8')
    if identifier not in ds.data:
        return '', 400
    res = []
    for i in data.split('\n'):
        if not i:
            continue
        checked = i[0] == '!'
        if checked:
            i = i[1:]
        res.append(ListItem(i, checked))

    ds.data[identifier] = res
    return '', 200


@app.route('/<identifier>/exported')
def exported(identifier):
    if identifier not in ds.data:
        ds.data[identifier] = []
    return render_template('exported_list.html', identifier=identifier, lst=ds.data[identifier])


@app.route('/save')
def save():
    ds.save()
    return redirect('/')

run_autosave = True
def autosave():
    while run_autosave:
        ds.save()
        print(ds.data)
        time.sleep(1)

thr = Thread(target=autosave, daemon=True)
thr.start()

if __name__ == '__main__':
    try:
        app.run('0.0.0.0', 8888, debug=False)
    finally:
        run_autosave = False