# Learning code.

import collections

from sklearn.metrics import mean_absolute_error
from sklearn import linear_model
from sklearn.feature_selection import SelectKBest, f_regression

import prepare


def mae(model, X, Y):
    return mean_absolute_error(Y, model.predict(X))


def score(name, model, X, Y):
    print(name, 'R^2 =', model.score(X, Y), 'Mean error =', mae(model, X, Y))


def fit_one(name, model, V, IN, OUT, verbose=False):

    X0 = prepare.pick_vars(V, IN)
    Y0 = prepare.pick_var('PRICE', IN)
    X1 = prepare.pick_vars(V, OUT)
    Y1 = prepare.pick_var('PRICE', OUT)

    if verbose:
        print('=== model:', name, '===')
    model.fit(X0, Y0)

    if verbose:
        print('intercept:', model.intercept_)
        print('coefficients:')
        for v, w in sorted(zip(V, model.coef_)):
            print('    ', v, w)
        print()

    score('in sample', model, X0, Y0)
    score('out sample', model, X1, Y1)

    V_ = [v for v, c in zip(V, model.coef_) if abs(c) > 0.00001]

    if model.score(X1, Y1) > 0.30 or len(V) > 40:
        return V_
    else:
        return V


def fit_all(V, IN, OUT):

    models = [
        ('Linear', linear_model.LinearRegression()),
        ('Ridge', linear_model.Ridge(alpha=0.5)),
        ('LassoLarsIC', linear_model.LassoLarsIC(max_iter=5000))
    ]

    scores = collections.defaultdict(int)

    for name, model in models:
        V_ = fit_one(name, model, V, IN, OUT, True)
        for v in V_:
            scores[v] += 1

    max_score = max(scores.values())
    return [v for v in V if scores[v] == max_score]


def optimize_vars(V, IN, OUT):

    model = linear_model.LassoLarsIC(max_iter=5000) 
    V_ = fit_one('LassoLarsIC', model, V, IN, OUT)

    dropped = sorted(set(V) - set(V_))
    if dropped:
        print('remaining variables:', sorted(V_))
        return optimize_vars(V_, IN, OUT)
    else:
        print(len(V), 'final variables:', sorted(V))
        return V


def pick_vars(num_vars, V, IN):

    X = prepare.pick_vars(V, IN)
    Y = prepare.pick_var('PRICE', IN)

    fsel = SelectKBest(f_regression, num_vars).fit(X, Y)
    indices = set(fsel.get_support(indices=True))

    V_ = [v for i, v in enumerate(V) if i in indices]

    print(num_vars, 'best variables:', V_)
    return V_
