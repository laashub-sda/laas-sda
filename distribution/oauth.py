from datetime import timedelta

from flask import request, g, session, redirect, url_for, Blueprint
from flask_github import GitHub

from .config import app_conf

GITHUB_CLIENT_ID = app_conf["github"]["oauth_app"]["CLIENT_ID"]
GITHUB_CLIENT_SECRET = app_conf["github"]["oauth_app"]["CLIENT_SECRET"]

app = Blueprint('distribution_oauth', __name__,
                url_prefix='/distribution/oauth')

github = GitHub(app)


def condition():
    if session.get('user_id', None) is None:
        return github.authorize()
    else:
        print("session['user_id']: ", session['user_id'])
        return 'Already logged in'


@app.route('/github-callback')
@github.authorized_handler
def authorized(access_token):
    next_url = request.args.get('next') or url_for('index')
    if access_token is None:
        return redirect(next_url)
    print("access_token: ", access_token)

    user = {"access_token": access_token}

    user["github_access_token"] = access_token

    g.user = user
    github_user = github.get('/user')
    user["github_id"] = github_user['id']
    user["github_login"] = github_user['login']

    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=3)
    # app.permanent_session_lifetime = timedelta(minutes=10)
    session['user_id'] = user["id"]
    print("user: ", str(user))
    return redirect(next_url)
