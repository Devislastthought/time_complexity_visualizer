"""
Time Complexity Visualizer
---------------------------
A tiny Flask server with one endpoint: /analyze

Example:
  http://localhost:8000/analyze?algo=linear_search&step=10&n_max=1000

What it does:
  1. Reads algo, step, n_max from the URL.
  2. Runs the chosen algorithm on lists of increasing size (0, step,
     2*step, ... up to n_max), counting how many steps it takes each time.
  3. Plots "list size" vs "steps taken" using matplotlib and saves the
     chart as a PNG file locally (inside static/).
  4. Reads that PNG back, base64-encodes it, and returns everything as JSON.
"""

import os
import base64
import time
import json

import matplotlib
matplotlib.use("Agg")  # so matplotlib doesn't try to open a GUI window
import matplotlib.pyplot as plt

from flask import Flask, request, jsonify

from algorithms import ALGORITHMS, make_random_list
from models import Analysis, SessionLocal, init_db

app = Flask(__name__)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

# Create the database table (if it doesn't exist yet) as soon as the app starts.
init_db()


@app.route("/analyze")
def analyze():
    # --- 1. Read and validate query parameters ---
    algo = request.args.get("algo")
    step = request.args.get("step", type=int)
    n_max = request.args.get("n_max", type=int)

    if algo is None or step is None or n_max is None:
        return jsonify({
            "error": "Missing parameter. Required: algo, step, n_max."
        }), 400

    if algo not in ALGORITHMS:
        return jsonify({
            "error": f"Unknown algo '{algo}'. Choose from: {list(ALGORITHMS.keys())}"
        }), 400

    if step <= 0 or n_max <= 0:
        return jsonify({"error": "step and n_max must be positive numbers."}), 400

    algo_function = ALGORITHMS[algo]

    # --- 2. Run the algorithm for n = 0, step, 2*step, ... up to n_max ---
    # We measure REAL running time (a stopwatch), not a theoretical step
    # count. This is why the resulting chart looks "noisy" or wavy instead
    # of a perfectly smooth curve — real timing is affected by whatever
    # else the computer happens to be doing at that exact moment.
    sizes = []
    steps_taken = []

    n = 0
    while n <= n_max:
        arr = make_random_list(n)

        start_time = time.perf_counter()
        algo_function(arr)
        elapsed_seconds = time.perf_counter() - start_time

        sizes.append(n)
        steps_taken.append(elapsed_seconds)

        n += step

    # --- 3. Plot the results and save as a PNG file ---
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, steps_taken, marker="o")
    plt.title("Algorithm Time Complexity Visualiser")
    plt.xlabel("Input Size")
    plt.ylabel("Running Time (seconds)")
    plt.grid(True)

    filename = f"{algo}_{int(time.time())}.png"
    filepath = os.path.join(STATIC_DIR, filename)
    plt.savefig(filepath)
    plt.close()

    # --- 4. Read the saved image back and base64-encode it ---
    with open(filepath, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    # --- 5. Send everything back as JSON ---
    return jsonify({
        "algo": algo,
        "step": step,
        "n_max": n_max,
        "sizes": sizes,
        "steps_taken": steps_taken,
        "image_path": filepath,
        "image_base64": encoded_image,
    })


@app.route("/save_analysis", methods=["POST"])
def save_analysis():
    """
    Saves an analysis result to the database using SQLAlchemy
    (no raw SQL written anywhere here).

    Expects a JSON body shaped like the response from /analyze, e.g.:
    {
        "algo": "linear_search",
        "step": 10,
        "n_max": 100,
        "sizes": [0, 10, 20, ...],
        "steps_taken": [0, 10, 20, ...],
        "image_base64": "iVBORw0KG..."
    }
    """
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Request body must be JSON."}), 400

    required_fields = ["algo", "step", "n_max", "sizes", "steps_taken", "image_base64"]
    missing = [field for field in required_fields if field not in data]
    if missing:
        return jsonify({"error": f"Missing field(s): {missing}"}), 400

    # Build a database row (a Python object) — SQLAlchemy turns this
    # into the correct SQL for us behind the scenes.
    analysis = Analysis(
        algo=data["algo"],
        step=data["step"],
        n_max=data["n_max"],
        sizes_json=json.dumps(data["sizes"]),
        steps_taken_json=json.dumps(data["steps_taken"]),
        image_base64=data["image_base64"],
    )

    session = SessionLocal()
    try:
        session.add(analysis)
        session.commit()
        session.refresh(analysis)  # loads the auto-generated id and created_at
        saved = analysis.to_dict()
    finally:
        session.close()

    return jsonify({
        "message": "Analysis saved successfully.",
        "analysis": saved,
    }), 201


@app.route("/analyses")
def list_analyses():
    """Lists every analysis saved so far, newest first. Handy for testing."""
    session = SessionLocal()
    try:
        rows = session.query(Analysis).order_by(Analysis.id.desc()).all()
        results = [row.to_dict() for row in rows]
    finally:
        session.close()

    return jsonify(results)


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)