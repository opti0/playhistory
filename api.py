from flask import Flask, jsonify, make_response, abort,request
import db


app = Flask(__name__)

@app.route('/api/v1/day/', methods=['GET'])
def current_day():
    return jsonify({'plays':db.get_day(), })

@app.route('/api/v1/day/<int:timestamp>', methods=['GET'])
def day_from_timestamp(timestamp):
    return jsonify({'plays':db.get_day(timestamp)})

@app.route('/api/v1/play/<int:play_id>', methods=['GET'])
def get_play_by_id(play_id):
    play = db.get_play_id(play_id)
    if play is None:
        abort(404)
    return jsonify({'play':db.get_play_id(play_id).__dict__})

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
    if play is None or not request.json:
        abort(404)
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

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
