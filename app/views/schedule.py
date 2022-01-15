import datetime
from datetime import date

from flask import Blueprint, render_template, url_for, redirect, flash, session
from flask_login import current_user, login_required

from service.event import get_today_events, get_all_events, get_tomorrow_events, get_events_by_weekday
from service.subject import get_subjects

bp = Blueprint('schedule', __name__, url_prefix='/schedule')


@bp.route('/', methods=['GET'])
@login_required
def index_page():
    return redirect(url_for('schedule.today_page'))


@bp.route('/today', methods=['GET'])
@login_required
def today_page():
    events = list(get_today_events(current_user))
    events.sort(key=lambda x: x.start_time)
    return render_template('schedule/today.html',
                           weekday=date.today().strftime('%A'),
                           weekday_num=date.today().weekday(),
                           date=date.today().strftime('%d %B'),
                           events=events,
                           subjects=get_subjects(current_user))


@bp.route('/tomorrow')
@login_required
def tomorrow_page():
    events = list(get_tomorrow_events(current_user))
    events.sort(key=lambda x: x.start_time)
    tomorrow = date.today() + datetime.timedelta(days=1)
    return render_template('schedule/tomorrow.html',
                           weekday=tomorrow.strftime('%A'),
                           weekday_num=tomorrow.weekday(),
                           date=tomorrow.strftime('%d %B'),
                           events=events,
                           subjects=get_subjects(current_user))


@bp.route('/week', methods=['GET'])
@login_required
def week_page():
    events = []
    for weekday in range(7):
        events.append(sorted(get_events_by_weekday(current_user, weekday), key=lambda x: x.start_time))
    print(events)
    return render_template('schedule/week.html',
                           events=events,
                           rows=max([len(row) for row in events]),
                           subjects=get_subjects(current_user))


@bp.route('/subjects', methods=['GET'])
@login_required
def subjects_page():
    return render_template('schedule/subjects.html')