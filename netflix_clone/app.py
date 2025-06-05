from flask import Flask, request, session, redirect, url_for, render_template_string, send_from_directory
import pyotp
import os

app = Flask(__name__)
app.secret_key = 'replace-with-a-secure-secret-key'

# In-memory user store
users = {
    'user1': {
        'password': 'password',
        '2fa_secret': pyotp.random_base32(),
    }
}

login_form = '''
<form action="/login" method="post">
  Username: <input type="text" name="username"><br>
  Password: <input type="password" name="password"><br>
  <input type="submit" value="Login">
</form>
'''

otp_form = '''
<p>Scan this QR Code with Google Authenticator if you have not already:</p>
<img src="https://chart.googleapis.com/chart?cht=qr&chs=200x200&chl={{ uri }}" alt="QR Code">
<form action="/verify" method="post">
  Enter 2FA Code: <input type="text" name="token"><br>
  <input type="submit" value="Verify">
</form>
'''

home_template = '''
<h1>Welcome {{ user }}</h1>
<ul>
{% for video in videos %}
<li><a href="/videos/{{ video }}">{{ video }}</a></li>
{% endfor %}
</ul>
'''

@app.route('/', methods=['GET'])
def index():
    if 'username' in session:
        videos = os.listdir(os.path.join('static', 'videos'))
        return render_template_string(home_template, user=session['username'], videos=videos)
    return login_form

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = users.get(username)
    if user and user['password'] == password:
        session['pre_2fa_user'] = username
        uri = pyotp.totp.TOTP(user['2fa_secret']).provisioning_uri(name=username, issuer_name="NetflixClone")
        return render_template_string(otp_form, uri=uri)
    return 'Invalid credentials', 401

@app.route('/verify', methods=['POST'])
def verify():
    username = session.get('pre_2fa_user')
    if not username:
        return redirect(url_for('index'))
    token = request.form['token']
    totp = pyotp.TOTP(users[username]['2fa_secret'])
    if totp.verify(token):
        session.pop('pre_2fa_user')
        session['username'] = username
        return redirect(url_for('index'))
    return 'Invalid token', 401

@app.route('/videos/<path:filename>')
def videos(filename):
    return send_from_directory(os.path.join('static', 'videos'), filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
