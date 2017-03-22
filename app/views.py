from app import app
from flask import render_template, url_for, redirect, flash
from flask import request
from rauth.service import OAuth2Service
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
import json
from database import getExpert, getCoauthor

class SearchForm(Form):
    content = StringField('content', validators = [DataRequired()])

github = OAuth2Service(
    client_id='cafbc0313ef4e4af7677',
    client_secret='e268bc7ac299a5221ce0e0fd3ecf6e163ed01b86',
    name='github',
    authorize_url='https://github.com/login/oauth/authorize',
    access_token_url='https://github.com/login/oauth/access_token',
    base_url='https://api.github.com/')

@app.route('/')
def index():
    print(request.args)
    return render_template('index.html')

@app.route('/login')
def login():
    return redirect(github.get_authorize_url())

@app.route('/welcome', methods = ['GET', 'POST'])
def welcome():
    form = SearchForm()
    if not 'code' in request.args:
        flash('You did not authorize the request')
        return redirect(url_for('index'))

    redirect_uri = url_for('welcome', _external = True)
    data = dict(code=request.args['code'], redirect_uri = redirect_uri)

    session = github.get_auth_session(data = data)

    user = session.get('user').json()
    username = user['login']
    email = user['email']
    
    return render_template('welcome.html', username = username, email = email, form = form)

@app.route('/expert_finding/')
def findExpert():
    domain = request.args.get('domain')
    expert_list = getExpert(domain)
    experts_json = json.dumps(expert_list)
    return experts_json

@app.route('/coauthors/')
def findCoauthors():
    author = request.args.get('author')
    coauthor_list = getCoauthor(author)
    coauthors_json = json.dumps(coauthor_list)
    return coauthors_json

@app.route('/expert_finding/show/')
def showExpert():
    domain = request.args.get('content')
    expert_list = getExpert(domain)
    return render_template('expert.html', search_content = domain, expert_list = expert_list)

@app.route('/coauthors/show/')
def showCoauthors():
    author = request.args.get('author')
    coauthor_list = getCoauthor(author)
    return render_template('coauthors.html', author = author, coauthor_list = coauthor_list)
