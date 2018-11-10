from flask import render_template, request, redirect, session, flash, url_for
from model.sample_a import SampleA
from dao.sample_a_dao import SampleADao
import time
from config.helpers import delete_file, recover_image, create_new_default_image
from sample import db, app
from view import session_view

sample_a_dao = SampleADao(db)


@app.route('/createSampleA', methods=['POST', ])
def create_sample_a():
    text_field_a = request.form['text_field_a']
    numeric_field_a = request.form['numeric_field_a']
    date_field_a = request.form['date_field_a']

    sample_a = SampleA(text_field_a, numeric_field_a, date_field_a,)
    sample_a_dao.save_sample_a(sample_a)

    upload_path = app.config['UPLOAD_PATH']
    timestamp: float = time.time()
    image_name = f'{upload_path}/pic{sample_a.id_field_a}-{timestamp}.jpg'

    if 'image_a' in request.files:
        file = request.files['image_a']
        file.save(image_name)
    else:
        create_new_default_image(image_name)

    return redirect(url_for('index'))


@app.route('/editSampleA/<int:id_field_a>')
def edit_sample_a(id_field_a):
    if 'logged_user' not in session or session['logged_user'] is None:
        return redirect(url_for('login', next=url_for('edit_sample_a', id_field_a=id_field_a)))
    sample_a = sample_a_dao.search_by_id_sample_a(id_field_a)
    image_name = recover_image(id_field_a)
    return render_template('edit_sample_a.html', title='Editing Sample A', sample_a=sample_a
                           , image_name=image_name or 'default_pic.jpg')


@app.route('/refreshSampleA', methods=['POST', ])
def refresh_sample_a():
    text_field_a = request.form['text_field_a']
    numeric_field_a = request.form['numeric_field_a']
    date_field_a = request.form['date_field_a']
    sample_a = SampleA(text_field_a, numeric_field_a, date_field_a,
                       id_field_a=request.form['id_field_a'])

    arquivo = request.files['image_a']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    delete_file(sample_a.id_field_a)
    arquivo.save(f'{upload_path}/pic{sample_a.id_field_a}-{timestamp}.jpg')
    sample_a_dao.save_sample_a(sample_a)
    return redirect(url_for('index'))


@app.route('/deleteSampleA/<int:id_field_a>')
def delete_sample_a(id_field_a):
    sample_a_dao.delete_sample_a(id_field_a)
    flash('The example was successfully removed!')
    return redirect(url_for('index'))


@app.route('/newSampleA')
def new_sample_a():
    if 'logged_user' not in session or session['logged_user'] is None:
        return redirect(url_for('login', next=url_for('new_sample_a')))
    return render_template('new_sample_a.html', title='New Sample A')
