from flask import Flask, jsonify, make_response, abort,request, send_from_directory, redirect, render_template, Response
import db, datetime, csv
from time import time
from io import StringIO

DEBUG = False

app = Flask(__name__, static_url_path='')

@app.route('/', methods=['GET'])
def root():
    return render_template('index.html')

@app.route('/hist/', methods=['GET'])
def history_data():
    return render_template('hist.html')

@app.route('/day/', methods=['GET'])
def show_day_template():
    t = request.args.get('t')
    day_name="Dzisiaj"
    if t is None:
        t = time()
    else:
        try:
            t = int(t)
            day_name = datetime.datetime.fromtimestamp(t).strftime("%d.%m.%Y r.")
        except:
            t = time()
    return render_template('day.html', songs = db.get_day(t), debug=DEBUG, t=t, day_name=day_name)

@app.route('/edit/<int:playid>', methods=['GET'])
def edit_play_object(playid):
    play = db.get_play_id(playid)
    if play is None:
        abort(404)
    ret = request.args.get('ret')
    if(ret is None):
        ret = '/day/'
    return render_template('edit.html', play = play, ret=ret, debug=DEBUG)

@app.route('/stats/', methods=['GET'])
def stats():
    start = request.args.get('startts')
    stop = request.args.get('stopts')
    if(start is None or stop is None):
        start=stop=0
    else:
        try:
            start = int(start)
            stop = int(stop) + 86399
        except:
            start = 0
            stop = 0
    return render_template('stats.html', data=db.get_stats(start,stop), date_start=start, date_stop=stop)

##      db export
@app.route('/download/', methods=['GET'])
def download():
    si = StringIO()
    cw = csv.writer(si)
    cw.writerows(db.generate_all())
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=db_%s.csv" % datetime.datetime.fromtimestamp(time()).strftime("%d_%m_%Y")
    output.headers["Content-type"] = "text/csv"
    return output

##      raport generator

@app.route('/report/', methods=['GET'])
def get_day_report():
    t = request.args.get('t')
    if t is None:
        t = time()
        print("t is None");
    else:
        try:
            t=int(t)
            print("t is orig");
        except:
            t = time()
            print("t is Str");
    content = render_template('report.txt', songs = db.get_day(t), date=t)
    return Response(content, mimetype="text/plain", headers={"Content-disposition":"attachment;filename=report_%s.txt"%datetime.datetime.fromtimestamp(t).strftime("%d_%m_%Y")})

##      api methods

"""@app.route('/api/v1/day/', methods=['GET'])
def current_day():
    return jsonify({'plays':db.get_day(), })

@app.route('/api/v1/day/<int:timestamp>', methods=['GET'])
def day_from_timestamp(timestamp):
    return jsonify({'plays':db.get_day(timestamp)})
"""
"""
@app.route('/api/v1/play/<int:play_id>', methods=['GET'])
def get_play_by_id(plastrftimey_id):
    play = db.get_play_id(play_id)
    if play is None:
        abort(404)
    return jsonify({'play':db.get_play_id(play_id).__dict__})
"""
@app.route('/api/v1/play/', methods=['POST'])
def add_new_play():
    if not request.json or not 'DJ' in request.json or not 'song' in request.json:
        abort(400)
    play = db.Play(DJ=request.json['DJ'], song=request.json['song'])
    play.save()
    return jsonify({'status':play.check()})

@app.route('/api/v1/play/<int:play_id>', methods=['DELETE'])
def del_play_id(play_id):
    play = db.get_play_id(play_id)
    print(1)
    if play is None:
        abort(404)
    print(2)
    play.delete()
    return jsonify({'status':play.check()})

@app.route('/api/v1/play/<int:play_id>', methods=['PUT'])
def pul_play_id(play_id):
    play = db.get_play_id(play_id)
    if play is None:
        abort(404)
    if 'DJ' in request.json and type(request.json['DJ']) != str:
        abort(400)
    if 'song' in request.json and type(request.json['song']) != str:
        abort(400)
    if 'date' in request.json and type(request.json['date']) != int:
        abort(400)
    play.DJ = request.json.get('DJ', play.DJ)
    play.song = request.json.get('song', play.song)
    play.date = request.json.get('date', play.date)
    play.save()
    return jsonify({'status':play.check(), 'play':play.__dict__})

###         static files
@app.route('/static/<path:path>')
def send_static_www(path):
    return send_from_directory('static', path)

### template_tags
@app.template_filter('display')
def display_date_from_timestamp(ts):
    return datetime.datetime.fromtimestamp(ts).strftime("%d.%m.%Y r.")

### other
@app.errorhandler(404)
def not_found(error):
    #return make_response(jsonify({'error': 'Not found'}), 404)
    return make_response('<center style="font-size:60vh;margin-top:20vh;"> 404 </center>')

if __name__ == '__main__':
    app.run(debug=DEBUG,host="localhost", port=int("80"))
