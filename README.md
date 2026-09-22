# Time Complexity Visualizer

A small Flask server that visualizes how the number of steps an algorithm
takes grows as the input size grows.

## Setup

```bash
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

The server runs at `http://localhost:8000`.

## Usage

Hit the `/analyze` endpoint with three query parameters:

- `algo` — one of: `linear_search`, `binary_search`, `bubble_sort`, `nested_loops`, `selection_sort`
- `step` — how much to increase the input size by each time
- `n_max` — the largest input size to test (starts from 0)

Example:

```
http://localhost:8000/analyze?algo=linear_search&step=10&n_max=1000
```

## Response

A JSON object containing:

- `sizes` — list of input sizes tested
- `steps_taken` — number of steps the algorithm took at each size
- `image_base64` — base64-encoded PNG chart of size vs steps
- `image_path` — where the chart was saved locally (inside `static/`)

## Algorithms included

- Linear Search — O(n)
- Binary Search — O(log n)
- Bubble Sort — O(n²)
- Nested Loops — O(n²)
- Selection Sort — O(n²)
