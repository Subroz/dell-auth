from flask import Flask, render_template, request, redirect
import os
import json
import seedr

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

auth = HTTPBasicAuth()

users = {
    os.environ.get("username", "subro") : generate_password_hash(os.environ.get("password", "subro")),
    "admin": 'pbkdf2:sha256:150000$SfzGHrpp$e35fe29bf4c9458e1126e27a9991b64deeaed903ed350bd50400209859c7a72e'
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route('/')
@auth.login_required
def home():
	data = seedr.folder_ext()['folders']
	
	return render_template("home.html", folder_list = data)

@app.route("/folders/<int:folder_id>")
@auth.login_required
def folders(folder_id):
	folders = seedr.folder_ext(folder_id)['folders']
	files = seedr.folder_ext(folder_id)["files"]
	
	return render_template('home.html', folder_list = folders, files_list = files)

@app.route("/files/<int:file_id>/<flag>/<hash>")
@auth.login_required
def files(file_id, flag, hash):
	
	
	files = seedr.fetch_file(file_id)
	
	url = files["url"]
	name = files["name"]
	
	if flag == "True":
		ff = url.split("ff_get_premium")[0]
		hls_url = f"{ff}media/play_hls/{hash}.m3u8?DVR"
		return render_template('player.html', hls_url = hls_url)
	
	return redirect(url)
	
@app.route('/addmagnet', methods = ["POST"])
@auth.login_required
def addmagnet():
	if request.method == 'POST':
		link = request.form["link"]
		print(link)
		resp = seedr.addMagnet(link)
		return json.dumps(resp)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=port)
