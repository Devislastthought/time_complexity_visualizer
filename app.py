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

import matplotlib
matplotlib.use("Agg")  # so matplotlib doesn't try to open a GUI window
import matplotlib.pyplot as plt

from flask import Flask, request, jsonify

from algorithms import ALGORITHMS, make_random_list

app = Flask(__name__)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)


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
    sizes = []
    steps_taken = []

    n = 0
    while n <= n_max:
        arr = make_random_list(n)
        steps = algo_function(arr)

        sizes.append(n)
        steps_taken.append(steps)

        n += step

    # --- 3. Plot the results and save as a PNG file ---
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, steps_taken, marker="o")
    plt.title(f"Time Complexity: {algo}")
    plt.xlabel("Input size (n)")
    plt.ylabel("Steps taken")
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


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
