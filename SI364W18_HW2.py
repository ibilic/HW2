## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
import requests, json

from flask import Flask, request, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################
class AlbumEntryForm(FlaskForm):
    name = StringField('Enter the name of an album:', validators=[Required()])
    question = RadioField('How much do you like this album? (1 low, 3 high)', validators=[Required()],choices=[('1','1'),('2','2'),('3','3')])
    submit = SubmitField('Submit', validators=[Required()])

@app.route('/album_entry', methods=['GET','POST'])
def album_entry():
    form=AlbumEntryForm()
    return render_template('album_entry.html', form=form)
@app.route('/album_result', methods=["GET","POST"])
def album_answers():
    form = AlbumEntryForm()
    if form.validate_on_submit():
        name = form.name.data
        question = form.question.data
        return render_template('album_data.html',form=form,name=name,question=question)
    flash(form.errors)
    return redirect(url_for('album_entry'))


####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

#-----------------------------ARTIST INFO-------------------------------------------------#
@app.route('/artistinfo',methods=["GET","POST"])
def artinfo():
    try:
        if request.method == "GET":
            entered = request.args['artist']
            return specific_artist(entered)
    except:
        baseurl = "https://itunes.apple.com/search?term=allTrackTerm"
        params_diction = {}
        params_diction["term"] = 'Ilma'
        resp = requests.get(baseurl,params=params_diction)
        text = resp.text
        python_obj = json.loads(text)

        objects = python_obj['results']
        return render_template('artist_info.html', objects=objects)
#-----------------------------ARTIST LINK & specifics-------------------------------------------------#
@app.route('/artistlink')
def artlink():
    return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>')
def specific_artist(artist_name):
    baseurl = "https://itunes.apple.com/search?term=allTrackTerm"
    params_diction = {}
    params_diction["term"] = artist_name
    resp = requests.get(baseurl,params=params_diction)
    text = resp.text
    python_obj = json.loads(text)
    objects = python_obj['results']
    return render_template('specific_artist.html', results=objects)
#-----------------------------ARTIST FORM-------------------------------------------------#
@app.route('/artistform', methods=["GET","POST"])
def artform():
    return render_template('artistform.html')


if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
