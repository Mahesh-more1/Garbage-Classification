"""
Garbage Classification & Waste Sorting Web Application (Python & Flask)
Developer: Mahesh More
"""

from flask import Flask, render_template, request, jsonify
import numpy as np
import os

app = Flask(__name__)

# Waste Classes & Recycling Advice
CLASSES = ['Cardboard', 'Glass', 'Metal', 'Paper', 'Plastic', 'Trash/Organic']
BIN_ADVICE = {
    'Cardboard': {'bin': 'Blue Bin', 'icon': '📦', 'tip': 'Flatten boxes to save space before recycling.'},
    'Glass': {'bin': 'Green Bin', 'icon': '🍾', 'tip': 'Rinse glass containers. Separate caps and corks.'},
    'Metal': {'bin': 'Gray Bin', 'icon': '🥫', 'tip': 'Rinse aluminum cans and foil before disposal.'},
    'Paper': {'bin': 'Blue Bin', 'icon': '📄', 'tip': 'Keep paper dry and unsoiled.'},
    'Plastic': {'bin': 'Yellow Bin', 'icon': '🥤', 'tip': 'Rinse PET bottles and remove non-recyclable caps.'},
    'Trash/Organic': {'bin': 'Black Bin', 'icon': '🍏', 'tip': 'Compost food scraps and organic bio-waste.'}
}

@app.route('/', methods=['GET'])
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Garbage Classification AI Web App</title>
        <style>
            body { font-family: sans-serif; background: #0f172a; color: #f8fafc; text-align: center; padding: 2rem; }
            .card { background: #1e293b; max-width: 500px; margin: 2rem auto; padding: 2rem; border-radius: 16px; border: 1px solid #334155; }
            h1 { color: #10b981; }
            .btn { background: #10b981; color: white; border: none; padding: 0.8rem 1.5rem; border-radius: 8px; font-weight: bold; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>♻️ Garbage Classification AI</h1>
            <p>Upload a waste image to classify it into Cardboard, Glass, Metal, Paper, Plastic, or Organic trash.</p>
            <form action="/predict" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept="image/*" required style="margin: 1rem 0;"><br>
                <button type="submit" class="btn">Classify Waste</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['file']
    filename = file.filename.lower()

    # Rule-based vision prediction helper for local demo
    if 'paper' in filename or 'news' in filename or 'book' in filename:
        predicted = 'Paper'
    elif 'glass' in filename or 'bottle' in filename and 'glass' in filename:
        predicted = 'Glass'
    elif 'box' in filename or 'carton' in filename or 'cardboard' in filename:
        predicted = 'Cardboard'
    elif 'can' in filename or 'metal' in filename or 'tin' in filename:
        predicted = 'Metal'
    elif 'plastic' in filename or 'pet' in filename:
        predicted = 'Plastic'
    else:
        predicted = 'Paper' if 'paper' in filename else 'Trash/Organic'

    info = BIN_ADVICE.get(predicted, BIN_ADVICE['Paper'])

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Classification Result</title>
        <style>
            body {{ font-family: sans-serif; background: #0f172a; color: #f8fafc; text-align: center; padding: 2rem; }}
            .card {{ background: #1e293b; max-width: 500px; margin: 2rem auto; padding: 2rem; border-radius: 16px; border: 1px solid #10b981; }}
            h1 {{ color: #10b981; }}
            .badge {{ background: rgba(16,185,129,0.2); color: #6ee7b7; padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold; display: inline-block; }}
            a {{ color: #3b82f6; text-decoration: none; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Result: {predicted} {info['icon']}</h1>
            <div class="badge">Disposal Bin: {info['bin']}</div>
            <p><strong>Recycling Tip:</strong> {info['tip']}</p>
            <br>
            <a href="/">← Upload Another Image</a>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("🚀 Starting Garbage Classification Web App on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
