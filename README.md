# Vectorized actuarial loops

Companion to: https://andyreagan.github.io/2020/09/17/vectorizing-code-matters/ (also published on [Medium](https://towardsdatascience.com/vectorizing-code-matters-66c5f95ddfd5)).

## Run the timings

    python3.8 -m venv venv
    venv/bin/pip install -U pip
    venv/bin/pip install -r requirements.txt

Build the cython code with:

    venv/bin/python setup.py build_ext --inplace

for each of the `pyx` files.

Then run the script (may take 15 minutes):

    venv/bin/python timed.py
