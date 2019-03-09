from flask import Flask, render_template, request, \
    make_response, redirect, jsonify, url_for, \
    flash, session as login_session
import functools
import os
import random
import string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery

from database_setup import Base, Region, Instrument

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///instruments.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

"""Scope the session, other than that,
a thread error will be raised
More on that can be found at:
https://docs.sqlalchemy.org/en/latest
/orm/contextual.html"""

session = scoped_session(DBSession)

# OAuth Credentials
# Notice: Ideally, this should be in a
# .env file that would be transferred among team members
ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
AUTHORIZATION_URL = 'https://accounts.google.com/o/' \
                    'oauth2/v2/auth?access_type=offline&prompt=consent'
AUTHORIZATION_SCOPE = 'openid email profile'
AUTH_REDIRECT_URI = 'http://localhost:8000/gCallback'
BASE_URI = 'http://localhost:8000'
CLIENT_ID = '359568122134-niii8bh1f3l32b466s6qna4867lbq45p.' \
            'apps.googleusercontent.com'
CLIENT_SECRET = 'T1iIGSdpiw9Tj-gPCnKQdyNy'

# Session credentials
AUTH_TOKEN_KEY = 'auth_token'
USER_INFO_KEY = 'user_info'


# =====> UTILITIES <=====

# auto versioning
# This enables css auto versioning,
# so one doesn't have to keep updating the timestamp on the css query string
@app.template_filter('autoversion')
def autoversion_filter(filename):
    # determining fullpath might be project specific
    full_path = os.path.join('app/', filename[1:])
    try:
        timestamp = str(os.path.getmtime(full_path))
    except OSError:
        return filename
    new_filename = "{0}?v={1}".format(filename, timestamp)
    return new_filename


# no_cache prevents browser caching of
# responses from the login/logout endpoints
def no_cache(view):
    @functools.wraps(view)
    def no_cache_impl(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, ' \
                                            'no-cache, ' \
                                            'must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return functools.update_wrapper(no_cache_impl, view)


# =====> LOGIN <=====
@app.route('/login')
@no_cache
def show_login():
    oauth_session = OAuth2Session(CLIENT_ID,
                                  CLIENT_SECRET,
                                  scope=AUTHORIZATION_SCOPE,
                                  redirect_uri=AUTH_REDIRECT_URI)
    uri, state = oauth_session.\
        create_authorization_url(AUTHORIZATION_URL)
    state = "".join(random.choice
                    (string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    login_session.permanent = True
    return redirect(uri, code=302)


# =====> LOGOUT <=====
@app.route('/logout')
@no_cache
def logout():
    state = "".join(random.choice
                    (string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session.pop(AUTH_TOKEN_KEY, None)
    login_session.pop(state, None)
    login_session.pop(USER_INFO_KEY, None)

    return redirect(BASE_URI, code=302)


# =====> GOOGLE AUTH REDIRECT <=====
# Stores the OAuth state parameter in the Flask session using AUTH_STATE_KEY
@app.route('/gCallback')
@no_cache
def google_auth_redirect():
    state = request.args.get('state', default=None, type=None)
    oauth_session = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                                  scope=AUTHORIZATION_SCOPE, state=state,
                                  redirect_uri=AUTH_REDIRECT_URI)
    oauth2_tokens = oauth_session.\
        fetch_access_token(ACCESS_TOKEN_URI,
                           authorization_response=request.url)
    login_session[AUTH_TOKEN_KEY] = oauth2_tokens
    return redirect('{}/dashboard'.format(BASE_URI), code=302)


# =====> GOOGLE USER INFO/CREDENTIALS <=====

# Checks if user is logged in
def is_logged_in():
    return True if AUTH_TOKEN_KEY in login_session else False


# builds user credentials
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


# gets user object
def get_user_info():
    credentials = build_credentials()
    oauth2_client = googleapiclient.\
        discovery.build('oauth2', 'v2',
                        credentials=credentials)
    return oauth2_client.userinfo().get().execute()


# =====> DASHBOARD VIEW <=====

@app.route('/dashboard/')
def show_dashboard():
    if is_logged_in():
        user_info = get_user_info()
        title = "My Instruments"
        instruments = session.query(Instrument).\
            filter_by(user_id=user_info["id"])
        return render_template('dashboard.html',
                               user=user_info,
                               instruments=instruments,
                               title=title)
    if not is_logged_in():
        return redirect(url_for('show_regions'), code=302)


# =====> REGIONS VIEW <=====

# JSON API to view Regions Information
@app.route('/regions/JSON')
def regions_json():
    regions = session.query(Region).all()
    return jsonify(regions=[r.serialize for r in regions])


# Main page: All Regions
@app.route('/')
def show_regions():
    regions = session.query(Region).all()
    title = "Instruments Per Region"
    if is_logged_in():
        user_info = get_user_info()
        return render_template('main.html',
                               regions=regions,
                               user=user_info,
                               title=title)
    else:
        return render_template('main.html',
                               regions=regions,
                               title=title)


# =====> ASIA VIEW <=====

# JSON API endpoint to view Asian Instruments
@app.route('/regions/asia/JSON')
def asia_json():
    region = session.query(Region).filter_by(name="Asia").one()
    asian_instruments = session.query(Instrument).filter_by(region=region)
    return jsonify(asian_instruments=[i.serialize for i in asian_instruments])


# Show all Asian Instruments
@app.route('/asia/')
def show_asian_instruments():
    if is_logged_in():
        user_info = get_user_info()
    else:
        user_info = None
    title = "Asian Instruments"
    region = session.query(Region).filter_by(name="Asia").one()
    asian_instruments = session.query(Instrument).filter_by(region=region)
    return render_template('asia.html', asian_instruments=asian_instruments,
                           user=user_info, title=title)


# =====> AFRICA VIEW <=====

# JSON API endpoint to view African Instruments
@app.route('/regions/africa/JSON')
def africa_json():
    region = session.query(Region).filter_by(name="Africa").one()
    african_instruments = session.query(Instrument).filter_by(region=region)
    return jsonify(african_instruments=[i.serialize
                                        for i in african_instruments])


# Show all African Instruments
@app.route('/africa/')
def show_african_instruments():
    if is_logged_in():
        user_info = get_user_info()
    else:
        user_info = None
    title = "African Instruments"
    region = session.query(Region).filter_by(name="Africa").one()
    african_instruments = session.query(Instrument).filter_by(region=region)
    return render_template('africa.html',
                           african_instruments=african_instruments,
                           user=user_info,
                           title=title)


# =====> NORTH AMERICAN VIEW <=====

# JSON API endpoint to view North American Instruments
@app.route('/regions/north_america/JSON')
def north_america_json():
    region = session.query(Region).filter_by(name="North America").one()
    north_american_instruments = session.\
        query(Instrument).filter_by(region=region)
    return jsonify(north_american_instruments=[i.serialize
                                               for i in
                                               north_american_instruments])


# Show all North American Instruments
@app.route('/north_america/')
def show_north_american_instruments():
    if is_logged_in():
        user_info = get_user_info()
    else:
        user_info = None
    title = "North American Instruments"
    region = session.query(Region).filter_by(name="North America").one()
    north_american_instruments = session.\
        query(Instrument).filter_by(region=region)
    return render_template(
        'north_america.html',
        north_american_instruments=north_american_instruments,
        user=user_info, title=title)


# =====> SOUTH AMERICAN VIEW <=====

# JSON endpoint to view South American Instruments
@app.route('/regions/south_america/JSON')
def south_america_json():
    region = session.query(Region).filter_by(name="South America").one()
    south_american_instruments = session.\
        query(Instrument).filter_by(region=region)
    return jsonify(south_american_instruments=[i.serialize
                                               for i in
                                               south_american_instruments])


# Show all South American Instruments
@app.route('/south_america')
def show_south_american_instruments():
    if is_logged_in():
        user_info = get_user_info()
    else:
        user_info = None
    title = "South American Instruments"
    region = session.query(Region).filter_by(name="South America").one()
    south_american_instruments = session.\
        query(Instrument).filter_by(region=region)
    return render_template(
        'south_america.html',
        south_american_instruments=south_american_instruments,
        user=user_info, title=title)


# =====> EUROPE VIEW <=====

# JSON endpoint to view European Instruments
@app.route('/regions/europe/JSON')
def europe_json():
    region = session.query(Region).filter_by(name="Europe").one()
    european_instruments = session.\
        query(Instrument).filter_by(region=region)
    return jsonify(european_instruments=[i.serialize
                                         for i in
                                         european_instruments])


# Show all European Instruments
@app.route('/europe/')
def show_european_instruments():
    if is_logged_in():
        user_info = get_user_info()
    else:
        user_info = None
    title = "European Instruments"
    region = session.query(Region).filter_by(name="Europe").one()
    european_instruments = session.\
        query(Instrument).filter_by(region=region)
    return render_template('europe.html',
                           european_instruments=european_instruments,
                           user=user_info,
                           title=title)


# =====> OCEANIA VIEW <=====

# JSON endpoint to view Instruments from Oceania
@app.route('/regions/oceania/JSON')
def oceania_json():
    region = session.query(Region).filter_by(name="Oceania").one()
    oceania_instruments = session.\
        query(Instrument).filter_by(region=region)
    return jsonify(oceania_instruments=[i.serialize
                                        for i in
                                        oceania_instruments])


# Show all Instruments from Oceania
@app.route('/oceania/')
def show_oceania_instruments():
    if is_logged_in():
        user_info = get_user_info()
    else:
        user_info = None
    title = "Oceania's Instruments"
    region = session.query(Region).filter_by(name="Oceania").one()
    oceania_instruments = session.\
        query(Instrument).filter_by(region=region)
    return render_template('oceania.html',
                           oceania_instruments=oceania_instruments,
                           user=user_info,
                           title=title)


# =====> INSTRUMENTS DETAILS VIEW <=====

# JSON endpoint to view Instrument details by ID
# TODO: look instrument up by name
@app.route('/details/<int:instrument_id>/JSON')
def instrument_details_json(instrument_id):
    instrument = session.\
        query(Instrument).filter_by(id=instrument_id)
    return jsonify(instrument=[i.serialize
                               for i in instrument])


# Show all the details of a given instrument based on its ID
# TODO: look instrument up by name
@app.route('/details/<int:instrument_id>/')
def show_instrument_details(instrument_id):
    if is_logged_in():
        user_info = get_user_info()
    else:
        user_info = None
    instrument = session.query(Instrument).\
        filter_by(id=instrument_id).all()
    instrument_region = instrument[0].region.name
    if instrument_region == "Oceania":
        title = "{}'s Instruments".format(instrument_region)
    elif instrument_region == "Europe":
        title = "{}an Instruments".format(instrument_region)
    else:
        title = "{}n Instruments".format(instrument_region)
    return render_template('details.html',
                           instrument=instrument,
                           user=user_info,
                           title=title)


# =====> CRUD OPERATIONS - CREATE, UPDATE, DELETE <=====

# Create a new instrument
@app.route('/create', methods=['GET', 'POST'])
def add_new_instrument():
    if not is_logged_in():
        return redirect('/login')
    else:
        user = get_user_info()
    if request.method == 'POST':
        user_info = get_user_info()
        user_id = user_info["id"]
        user_name = user_info["name"]
        region = session.query(Region).\
            filter_by(name=request.form['region']).one()
        new_instrument = Instrument(user_id=user_id, user_name=user_name,
                                    name=request.form['name'],
                                    description=request.form['description'],
                                    picture=request.form['picture'],
                                    region=region,
                                    credit=request.form['credit'])
        session.add(new_instrument)
        session.commit()
        flash('New Instrument {} Successfully Added to {}'
              .format(new_instrument.name, region.name))
        return redirect(url_for('show_regions'))
    else:
        return render_template('newinstrument.html',
                               user=user,
                               title="Add New Instrument")


# Update/Edit an instrument
@app.route('/edit/<int:instrument_id>', methods=['GET', 'POST'])
def edit_instrument(instrument_id):
    if not is_logged_in():
        return redirect('/login')
    edited_instrument = session.\
        query(Instrument).filter_by(id=instrument_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edited_instrument.name = request.form['name']
        if request.form['region']:
            edited_instrument.region = session.\
                query(Region).filter_by(name=request.form['region']).one()
        if request.form['description']:
            edited_instrument.description = request.form['description']
        if request.form['picture']:
            edited_instrument.picture = request.form['picture']
        if request.form['credit']:
            edited_instrument.credit = request.form['credit']
        session.add(edited_instrument)
        session.commit()
        flash('Instrument Successfully Edited')
        return redirect(url_for('show_instrument_details',
                                instrument_id=edited_instrument.id))
    else:
        user = get_user_info()
        return render_template('editinstrument.html',
                               instrument_id=edited_instrument.id,
                               instrument=edited_instrument,
                               user=user,
                               title="Edit Instrument")


# Delete an instrument
@app.route('/delete/<int:instrument_id>', methods=['GET', 'POST'])
def delete_instrument(instrument_id):
    if not is_logged_in():
        return redirect('/login')
    else:
        user = get_user_info()
    instrument_to_delete = session.\
        query(Instrument).filter_by(id=instrument_id).one()
    if request.method == 'POST':
        session.delete(instrument_to_delete)
        session.commit()
        flash('Instrument Successfully Deleted')
        return redirect(url_for('show_dashboard'))
    else:
        return render_template(
            'deleteinstrument.html',
            instrument_to_delete=instrument_to_delete,
            user=user, title="Delete Instrument")


if __name__ == '__main__':
    app.secret_key = '\xf6\xbc\xe3\xfeD\xb5\xf8=\xd1\x80?\x13Hl\x81\x11'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
