# app.py
from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/profile/<gmail>', methods=['POST','GET'])
def profile_maker(gmail):
    try:
        # Run your Python script using subprocess
        result = subprocess.run(['python3', 'prof_maker.py',gmail], capture_output=True, text=True)
        output = result.stdout
        return jsonify({'success': True, 'output': output})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/update', methods=['POST','GET'])
def update_all():
    try:
        # Run your Python script using subprocess
        result = subprocess.run(['python3', 'prac_update.py'], capture_output=True, text=True)
        output = result.stdout
        return jsonify({'success': True, 'output': output})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
