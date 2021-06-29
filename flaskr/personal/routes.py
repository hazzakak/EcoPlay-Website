from flask import render_template, session

from . import personal
from ..models import User

API_ENDPOINT = 'https://discord.com/api/v8'
CLIENT_ID = '767749360586326026'
CLIENT_SECRET = 'B8JBIE949Ak5DZZ-6DsmD4mG20Rf1U_S'
REDIRECT_URI = 'http://localhost:5000/discord/auth'


@personal.route('/personal-dashboard', methods=['GET', 'POST'])
def pers_dashboard():
    user = None
    if session['userid']:
        user = User.query.filter_by(id=session['userid']).first()
    return render_template('civ_dashboard.html', user=user if user is not None else None,
                           logged_in=session['logged_in'])
