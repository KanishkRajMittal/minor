# app.py
from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/profile/<gmail>', methods=['POST','GET'])
def execute_script(gmail):
    try:
        # Run your Python script using subprocess
        result = subprocess.run(['python3', '/home/kanishk/Desktop/upload/prof_maker.py',gmail], capture_output=True, text=True)
        output = result.stdout
        return jsonify({'success': True, 'output': output})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
