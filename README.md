# SciKit Learn experiments with real estate price data.

This repository contains one experiment with SciKit Learn. We load the data
from a CSV file, filter and preprocess it a bit (remove broken-looking data,
convert category variables to mutliple flag variables, add variable
transformations such as log, inverse, square). Then we try to find the best
set of variables to use for linear regression and compute the regression
coefficients.

## Dependencies

I was using Anaconda 2.4.1 on Python 3.5. It would probably work with any
version of SciKit learn on a recent Python 3.X.

## Running

python main.py
