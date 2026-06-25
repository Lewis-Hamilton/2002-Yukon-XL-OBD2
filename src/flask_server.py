import os
import threading

def start_flask(data_store, data_lock):
    from flask import Flask, request, jsonify
    import logging

    flask_app = Flask('flask_server', static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))

    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    flask_app.logger.setLevel(logging.ERROR)

    @flask_app.route('/')
    def index():
        return flask_app.send_static_file('controls.html')

    @flask_app.route('/set', methods=['POST'])
    def set_value():
        key = request.json.get('key')
        val = request.json.get('value')
        with data_lock:
            data_store[key] = val
        return jsonify({"ok": True})

    @flask_app.route('/state', methods=['GET'])
    def get_state():
        with data_lock:
            return jsonify(data_store.copy())

    flask_thread = threading.Thread(
        target=lambda: flask_app.run(host='0.0.0.0', port=5000, use_reloader=False),
        daemon=True
    )
    flask_thread.start()