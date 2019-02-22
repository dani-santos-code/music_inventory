from flask import Flask, render_template, request, make_response, redirect, jsonify, url_for, flash, session as login_session
import functools
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from authlib.client import OAuth2Session
import credentials
import google.oauth2.credentials
import googleapiclient.discovery

from database_setup import Base, Region, Instrument, User

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///instruments.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# OAuth Credentials
ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'

AUTHORIZATION_SCOPE ='openid email profile'

AUTH_REDIRECT_URI = 'http://localhost:5000/gCallback'
BASE_URI = 'http://localhost:5000'
CLIENT_ID = '359568122134-niii8bh1f3l32b466s6qna4867lbq45p.apps.googleusercontent.com'
CLIENT_SECRET = 'T1iIGSdpiw9Tj-gPCnKQdyNy'

AUTH_TOKEN_KEY = 'auth_token'
AUTH_STATE_KEY = 'auth_state'
USER_INFO_KEY = 'user_info'

def no_cache(view):
    @functools.wraps(view)
    def no_cache_impl(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return functools.update_wrapper(no_cache_impl, view)

@app.route('/login')
@no_cache
def login():
    oauth_session = OAuth2Session(CLIENT_ID, CLIENT_SECRET, scope=AUTHORIZATION_SCOPE, redirect_uri=AUTH_REDIRECT_URI)
    uri, state = oauth_session.create_authorization_url(AUTHORIZATION_URL)
    login_session[AUTH_STATE_KEY] = state
    login_session.permanent = True
    return redirect(uri, code=302)

@app.route('/logout')
@no_cache
def logout():
    login_session.pop(AUTH_TOKEN_KEY, None)
    login_session.pop(AUTH_STATE_KEY, None)
    login_session.pop(USER_INFO_KEY, None)

    return redirect(BASE_URI, code=302)

@app.route('/gCallback')
@no_cache
def google_auth_redirect():
    state = request.args.get('state', default=None, type=None)
    oauth_session = OAuth2Session(CLIENT_ID, CLIENT_SECRET, scope=AUTHORIZATION_SCOPE, state=state, redirect_uri=AUTH_REDIRECT_URI)
    oauth2_tokens = oauth_session.fetch_access_token(ACCESS_TOKEN_URI, authorization_response=request.url)
    login_session[AUTH_TOKEN_KEY] = oauth2_tokens
    return redirect('{}/dashboard'.format(BASE_URI), code=302)

def is_logged_in():
    return True if AUTH_TOKEN_KEY in login_session else False

@app.route('/dashboard/')
def showDashboard():
    if is_logged_in():
        user_info = get_user_info()
        flash('You have successfully logged in')
        return render_template('dashboard.html')
    if not is_logged_in():
        return redirect(url_for('showRegions'), code=302)

def build_credentials():
    if not is_logged_in():
        raise Exception('User must be logged in')

    oauth2_tokens = login_session[AUTH_TOKEN_KEY]
    return google.oauth2.credentials.Credentials(
        oauth2_tokens['access_token'],
        refresh_token=oauth2_tokens['refresh_token'],
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_uri=ACCESS_TOKEN_URI)

def get_user_info():
    credentials = build_credentials()
    oauth2_client = googleapiclient.discovery.build('oauth2', 'v2', credentials=credentials)
    return oauth2_client.userinfo().get().execute()

@app.route('/')
@app.route('/main/')
def showRegions():
    regions = session.query(Region).all()
    instruments = session.query(Instrument).all()
    users = session.query(User).all()
    # print(users)
    return render_template('main.html', regions=regions, instruments=instruments, users=users)

@app.route('/asia/')
def showAsianInstruments():
    return render_template('asia.html')

@app.route('/africa/')
def showAfricanInstruments():
    return render_template('africa.html')

@app.route('/north_america/')
def showNorthAmericanInstruments():
    return render_template('north_america.html')

@app.route('/south_america')
def showSouthmericanInstruments():
    return render_template('south_america.html')

@app.route('/europe/')
def showEuropeanInstruments():
    return render_template('europe.html')

@app.route('/oceania/')
def showOceaniaInstruments():
    return render_template('oceania.html')

if __name__ == '__main__':
    app.secret_key = '\xf6\xbc\xe3\xfeD\xb5\xf8=\xd1\x80?\x13Hl\x81\x11'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
