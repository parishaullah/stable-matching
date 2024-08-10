from flask import Flask, render_template, request

from sm import SM
from smi import SMI
from rgs import RGS
from hgs import HGS
from sr import SR

app = Flask(__name__)
app.config['SECRET_KEY'] = '12183222810'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/stableMatching', methods=('GET', 'POST'))
def stableMatching():
    if request.method == 'POST':
        n = int(request.form['num'])
        propose = request.form['propose']
        lPreferences = request.form['lPreferences']
        fPreferences = request.form['fPreferences']
        leadersPropose = False
        if propose == 'Leaders':
            leadersPropose = True
        sm1 = SM(n=n, leadersPropose=leadersPropose)
        result = sm1.algorithm(lPreferences.split(", "), fPreferences.split(", "))
        match = result[0]
        steps = result[1]
        del match[0]
        return render_template('smOutput.html', match=match, leadersPropose=leadersPropose, steps=steps,
                               lPreferences=lPreferences.split(", "), fPreferences=fPreferences.split(", "))
    return render_template('stableMatching.html')


@app.route('/stableMatchingIncomplete', methods=('GET', 'POST'))
def stableMatchingIncomplete():
    if request.method == 'POST':
        n = int(request.form['num'])
        propose = request.form['propose']
        lPreferences = request.form['lPreferences']
        fPreferences = request.form['fPreferences']
        leadersPropose = False
        if propose == 'Leaders':
            leadersPropose = True
        smi1 = SMI(n=n, leadersPropose=leadersPropose)
        result = smi1.algorithm(lPreferences.split(", "), fPreferences.split(", "))
        match = result[0]
        steps = result[1]
        del match[0]
        return render_template('smiOutput.html', match=match, leadersPropose=leadersPropose, steps=steps,
                               lPreferences=lPreferences.split(", "), fPreferences=fPreferences.split(", "))
    return render_template('stableMatchingIncomplete.html')


@app.route('/residentHR', methods=('GET', 'POST'))
def residentHR():
    if request.method == 'POST':
        h = int(request.form['hos'])
        r = int(request.form['res'])
        hPreferences = request.form['hPreferences']
        rPreferences = request.form['rPreferences']
        cap = request.form['cap']
        rgs = RGS(h=h, r=r)
        result = rgs.algorithm(hPreferences.split(", "), rPreferences.split(", "), cap.split())
        match = result[0]
        steps = result[1]
        del match[0]
        return render_template('residentOutput.html', match=match, steps=steps, hPreferences=hPreferences.split(", "),
                               rPreferences=rPreferences.split(", "))
    return render_template('residentHR.html')


@app.route('/hospitalHR', methods=('GET', 'POST'))
def hospitalHR():
    if request.method == 'POST':
        h = int(request.form['hos'])
        r = int(request.form['res'])
        hPreferences = request.form['hPreferences']
        rPreferences = request.form['rPreferences']
        cap = request.form['cap']
        hgs = HGS(h=h, r=r)
        result = hgs.algorithm(hPreferences.split(", "), rPreferences.split(", "), cap.split())
        match = result[0]
        steps = result[1]
        del match[0]
        return render_template('hospitalOutput.html', match=match, steps=steps, hPreferences=hPreferences.split(", "),
                               rPreferences=rPreferences.split(", "))
    return render_template('hospitalHR.html')


@app.route('/stableRoommate', methods=('GET', 'POST'))
def stableRoommate():
    if request.method == 'POST':
        n = int(request.form['num'])
        preferences = request.form['preferences']
        sr = SR(n=n)
        result = sr.algorithm(preferences.split(", "))
        match = result[0]
        steps = result[1]
        solved = result[2]
        del match[0]
        return render_template('srOutput.html', match=match, steps=steps, solved=solved,
                               preferences=preferences.split(", "))
    return render_template('stableRoommate.html')


if __name__ == '__main__':
    app.run()
