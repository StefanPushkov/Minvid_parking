import sqlite3

from flask import Flask, render_template, url_for, request, abort, jsonify, send_from_directory

import configs.heimdallr as config

app = Flask(__name__)


def get_full_image_path(name):
    return '/media/' + name


ALLOWED_METHODS = ['new', 'old', 'initial']


@app.route('/', methods=['GET'])
def heimdall():
    return render_template('heimdallr.html', jquery=url_for('static', filename='jquery.min.js'))


@app.route('/photos', methods=['GET'])
def photos():
    req_method = request.args.get('method')
    if req_method and req_method in ALLOWED_METHODS:
        conn = sqlite3.connect(config.DB_PATH)
        cur = conn.cursor()

        sql = ""
        if req_method == 'initial':
            sql = """SELECT rowid, * FROM shots
                      ORDER BY rowid DESC
                      LIMIT {};""".format(config.PAGINATE_BY)

        if req_method == 'new':
            last_id = request.args.get('last_id')
            if not last_id:
                return abort(400)

            sql = """SELECT rowid, * FROM shots
                      WHERE rowid > {}
                      ORDER BY rowid DESC;""".format(last_id)

        if req_method == 'old':
            last_id = request.args.get('last_id')
            if not last_id:
                return abort(400)

            sql = """SELECT rowid, * FROM shots
                      WHERE rowid < {}
                      ORDER BY rowid DESC
                      LIMIT {};""".format(last_id, config.PAGINATE_BY)

        cur.execute(sql)
        response = [{'rowid': rowid, 'plateno': plateno, 'full_image': get_full_image_path(full_image)} for
                    rowid, plateno, full_image in cur.fetchall()]
        return jsonify(response)
    else:
        return abort(400)


@app.route('/media/<path:filename>')
def serve_photos(filename):
    return send_from_directory(config.IMAGE_ROOT_FOLDER + '/', filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='105000')
