# Flick Fixer

We attempted to model the choices of director, actor, genre,and content rating with a constraint satisfaction problem (CSP) driven by a randomforest movie rating predictor as a heuristic for each partial assignment of the movie.
## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

```
Python 2.7
NumPy
SciPy
```


### Running the Code

In order to run the CSP on 100 incomplete profiles run the following command (~ 40 mins):


```
python csp_eval.py
```

## Functional Breakdown of Codebase
* csp.py - Movie CSP constructor and backtracking search algorithm
* csp_baseline.py - baseline for evaluating CSP
* csp_eval.py - testing script for running CSP on incomplete profiles
* util.py - CSP class and Profile class 
* final_data.csv -  csv of training data
* cleaned_features.csv - cleaned version of final_data
* make_csv.py - generates cleaned_features
* forest.py, lasso.py, regression.py, svm.py - ratings predictors code
* Pickle files hold maps of variable names to their id numbers and other properties





## Authors

* **Veeral Patel** 
* **Sumit Minocha**
* **Rohun Saxena**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Chuan Sun and NYC Data Science
* Mohana Prasad Sathya Moorthy
* CS221 Class CSP implementation
