import requests
from datetime import datetime, timedelta
from flask import jsonify, render_template, request, redirect, flash
from app import app, db, celery
from .models import Results, Tasks, NSQD
from .forms import WebsiteForm

nsqd = NSQD('nsqd:4151')

@celery.task
def get_link(id):
    task = Tasks.query.get(id)
    task.task_status = 'PENDING'
    db.session.commit()
    address = task.address
    if not (address.startswith('http') or address.startswith('https')):
        address = 'http://' + address
    nsqd.send('parsed_data', json.dumps({"address": address, "id": str(id)}))

@celery.task
def parse_website_text(_id):
    task = Tasks.query.get(_id)
    task.task_status = 'PENDING'
    db.session.commit()
    address = task.address
    if not (address.startswith('http') and  address.startswith('https')):
        address = 'http://' + address
    with app.app_context():
        res = requests.get(address) 
        words_count=0
        if res.ok:
            words = res.text.split()
            words_count = words.count("Python")
            
        result = Results(address=address, words_count=words_count, http_status_code=res.status_code)
        task = Tasks.query.get(_id)
        task.task_status = 'FINISHED'
        db.session.add(result)
        db.session.commit()


@app.route('/', methods=['POST', 'GET'])
@app.route('/add_website', methods=['POST', 'GET'])
def website():
    website_form = WebsiteForm()
    if request.method == 'POST':
        if website_form.validate_on_submit():
            address = request.form.get('address')
            task = Tasks(address=address, timestamp=datetime.now(), task_status='NOT_STARTED')
            db.session.add(task)
            db.session.commit()
            parse_website_text.delay(task._id)
            return redirect('/')
        error = "Form was not validated"
        return render_template('error.html',form=website_form,error = error)
    return render_template('add_website.html', form=website_form)


@app.route('/results')
def get_results():
    results = Results.query.all()
    for i in results:
        if not i.address or i.address == "https" or i.address == "http":
            print("Address is emtpy: %s" % i.address)
        if i.http_status_code != 200:
            print("Status code is different. {} - code: {}".format(i.address, i.http_status_code))
        if i.words_count == 0:
            print("Words count is zero. Check it out: {} count is: {}".format(i.address, i.words_count))
    return render_template('results.html', results=results)