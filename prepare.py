# Preparing the data.

import math


def add_month_dummies(d):
    for m in range(1, 13):
        d['DATE_M%02d' % m] = 1 if d['DATE'].month == m else 0


def add_quarter_dummies(d):
    for q in range(1, 5):
        d['DATE_Q%02d' % q] = 1 if d['DATE'].month // 4 == q else 0


def add_year_dummies(d):
    for y in [2008, 2009]:
        d['DATE_Y%d' % y] = 1 if d['DATE'].year == y else 0


def add_btype_dummies(d):
    for bt in range(1, 5):
        d['BTYPE_%d' % bt] = 1 if d['BTYPE'] == bt else 0


def add_dummies(dicts):
    for d in dicts:
        # add_month_dummies(d)
        add_quarter_dummies(d)
        add_year_dummies(d)
        add_btype_dummies(d)


def add_sample(dicts):
    for d in dicts:
        d['Sample'] = (d['PRICE'] * d['LOTSIZE'] *
                       d['FLOORSPACE'] * d['AGE'] % 521) / 521.0


def add_var_from_func(name, func):
    def derive(dicts):
        for d in dicts:
            try:
                d[name] = func(d)
            except:
                raise Exception('Error while adding ' + name + str(d))
    return derive


def add_var_transformations(var, dicts):

    add_log = add_var_from_func(var + '_LOG', lambda d: math.log(d[var] + 1))
    add_inv = add_var_from_func(var + '_INV', lambda d: 1.0 / (d[var] + 1.0))
    add_sqrt = add_var_from_func(var + '_SQRT', lambda d: math.sqrt(d[var]))
    add_sq = add_var_from_func(var + '_SQ', lambda d: d[var] ** 2)
    add_cu = add_var_from_func(var + '_CU', lambda d: d[var] ** 3)
    add_p4 = add_var_from_func(var + '_P4', lambda d: d[var] ** 4)

    values = {d[var] for d in dicts}
    nvalues = len(values)

    if nvalues == 3:
        a, b, c = sorted(values)
        if b > (a + c) / 2:
            add_log(dicts)
        else:
            add_sq(dicts)
    elif nvalues > 3:
        add_log(dicts)
        add_inv(dicts)
        add_sqrt(dicts)
        add_sq(dicts)
        add_cu(dicts)
        add_p4(dicts)


def add_transformations(dicts, variables):
    for var in variables:
        add_var_transformations(var, dicts)


def remove_bad_vars(dicts):
    for var in list(dicts[0].keys()):
        values = {d[var] for d in dicts}
        bad = len(values) < 2 
        for value in values:
            if type(value) not in [int, float]:
                bad = True
                break
        if bad:
            for d in dicts:
                del d[var]


def add_crossterm(v1, v2, dicts):
    for d in dicts:
        d[v1 + ' x ' + v2] = d[v1] * d[v2]


def add_crossterms(V1, V2, dicts):
    for v1 in V1:
        for v2 in V2:
            prefix1 = v1.split('_')[0]
            prefix2 = v2.split('_')[0]
            if prefix1 != prefix2:
                add_crossterm(v1, v2, dicts)


def pick_vars(variables, dicts):
    return [[d[v] for v in variables] for d in dicts]


def pick_var(variable, dicts):
    return [d[variable] for d in dicts]
