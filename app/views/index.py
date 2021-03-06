from flask import Blueprint, render_template, redirect, url_for, current_app
from flask_login import current_user

bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def index_page():
    if current_user.is_authenticated:
        return redirect(url_for('schedule.today_page'))
    if current_app.config['DEMO_MODE']:
        return render_template('index-demo.html')
    return render_template('index.html')
