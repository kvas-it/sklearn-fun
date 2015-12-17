# Main model builder.

import loader
import prepare
import learn


THRESHOLD = 0.95  # For choosing in/out-sample.

lists = loader.read_csv(loader.ALL_WARDS)
dicts = loader.to_dicts(lists)
dicts = loader.convert_types(dicts)
dicts = loader.filter_broken(dicts)
# dicts = list(filter(lambda d: d['WARD'] == 1, dicts))

prepare.add_dummies(dicts)
prepare.remove_bad_vars(dicts)
prepare.add_transformations(dicts, set(dicts[0].keys()) - {'PRICE', 'Sample'})
prepare.add_sample(dicts)

all_vars = set(dicts[0].keys()) - {'PRICE', 'Sample'}

def pick_by_prefix(prefixes):
    return {v for v in all_vars if {p for p in prefixes if v.startswith(p)}}

apt_vars = pick_by_prefix({
    'AC', 'AGE', 'BATHROOM', 'BEDROOM', 'CBD', 'FIREPLACE', 'FLOOR',
    'FLOORSPACE', 'HALFBATHROOM', 'HEAT', 'LOTSIZE', 'METRO', 'BTYPE_'
    })

nb_vars = pick_by_prefix({
    'ASIAN', 'BLACK', 'WHITE', 'HIS', 'FORE', 'TEENMUM', 'SUBPRIME', 'SCHOOL',
    'POVERTY', 'FEMALEHEADED', 'INCOME', 'PCRIMES', 'OWNER', 'UNEM', 'VACANCY',
    'VCRIMES', 'POPU', 'LOWWEIGHT', 'MPRICE'
})

date_vars = pick_by_prefix({'DATE_'})

prepare.add_crossterms(pick_by_prefix({'SUBPRIME'}), ['DATE_Y2009'], dicts)

in_sample = list(filter(lambda d: d['Sample'] < THRESHOLD, dicts))
out_sample = list(filter(lambda d: d['Sample'] >= THRESHOLD, dicts))

all_vars = set(dicts[0].keys()) - {'PRICE', 'Sample'}

print('starting with', len(all_vars), 'variables')
print('in_sample points', len(in_sample))
print('out_sample points', len(out_sample))

# good_vars = learn.pick_vars(200, all_vars, in_sample)
better_vars = learn.optimize_vars(all_vars, in_sample, out_sample)
learn.fit_all(better_vars, in_sample, out_sample)
