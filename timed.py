import timeit
import pandas as pd
import numpy as np

iterations = 100000

# vectorized, end up numpy arrays
setup_code = """import numpy as np
years = 10
prem = 50
wit = 5"""

main_code = """eom = np.arange(years*12)*prem - np.arange(years*12)*wit
# and if you still want bom as an array:
bom = eom + np.arange(years*12)*wit"""

t1 = min(timeit.repeat(
    stmt=main_code,
    setup=setup_code,
    number=iterations
))
print(t1)
# non-vectorized, end up numpy arrays
main_code = """bom = np.zeros(years*12)
eom = np.zeros(years*12)
for month in range(1, years*12):
    bom[month] = eom[month-1] + prem
    eom[month] = bom[month] - wit"""

t2 = min(timeit.repeat(
    stmt=main_code,
    setup=setup_code,
    number=iterations
))
print(t2)
print(t2/t1)

# non-vectorized, end up with list
main_code = """result = [{'bom': 0, 'eom': 0}]
for month in range(1, years*12):
    inner = {}
    inner.update({'bom': result[month-1]['eom'] + prem})
    inner.update({'eom': inner['bom'] - wit})
    result.append(inner)"""
t3 = min(timeit.repeat(
    stmt=main_code,
    setup="""years = 10
prem = 50
wit = 5""",
    number=iterations
))
print(t3)
print(t3/t1)

# could try pre-allocating the vectors in setup, for the above

# vectorized, end up datafame
setup_code = """import numpy as np
import pandas as pd
years = 10
prem = 50
wit = 5"""
main_code = """eom = np.arange(years*12)*prem - np.arange(years*12)*wit
# and if you still want bom as an array:
bom = eom + np.arange(years*12)*wit
pd.DataFrame(data={'bom': bom, 'eom': eom})"""

t4 = min(timeit.repeat(
    stmt=main_code,
    setup=setup_code,
    number=iterations
))
print(t4)
print(t4/t1)

# non-vectorized, end up datafame
main_code = """bom = np.zeros(years*12)
eom = np.zeros(years*12)
for month in range(1, years*12):
    bom[month] = eom[month-1] + prem
    eom[month] = bom[month] - wit
pd.DataFrame(data={'bom': bom, 'eom': eom})"""

t5 = min(timeit.repeat(
    stmt=main_code,
    setup=setup_code,
    number=iterations
))
print(t5)
print(t5/t1)

# non-vectorized, iterate on df
main_code = """df = pd.DataFrame(data={'bom': np.zeros(years*12), 'eom': np.zeros(years*12)})
for i, row in df.iterrows():
    if i > 0:
        row.bom = df.loc[i-1, 'eom']
        row.eom = row.bom - wit"""

t6 = min(timeit.repeat(
    stmt=main_code,
    setup=setup_code,
    number=int(iterations/10)
))*10
print(t6)
print(t6/t1)

setup_code = """import pandas as pd
years = 10
prem = 50
wit = 5"""
main_code = """result = [{'bom': 0, 'eom': 0}]
for month in range(1, years*12):
    inner = {}
    inner.update({'bom': result[month-1]['eom'] + prem})
    inner.update({'eom': inner['bom'] - wit})
    result.append(inner)
pd.DataFrame(result)"""
t7 = min(timeit.repeat(
    stmt=main_code,
    setup=setup_code,
    number=int(iterations/10)
))*10
print(t7)
print(t7/t1)

# vectorized? return as df? iterate on (np, {}, pd)
# t1, t1/t1. Y N --
# t2, t2/t1. N N np
# t3, t3/t1. N N {}
# t4, t4/t1. Y Y --
# t5, t5/t1. N Y np
# t6, t6/t1. N Y {}
# t7, t7/t1. N Y df

t8 = min(timeit.repeat(
    stmt="main()",
    setup="from cython_loop import main",
    number=iterations
))
print(t8)
print(t8/t1)

t9 = min(timeit.repeat(
    stmt="main()",
    setup="import numpy as np; from numpy_cython_loop import main",
    number=iterations
))
print(t9)
print(t9/t1)

t10 = min(timeit.repeat(
    stmt="main()",
    setup="from cython_loop_c_array import main",
    number=iterations
))
print(t10)
print(t10/t1)

d = pd.DataFrame([
    {'vectorized': True, 'return_type': 'numpy', 'iterate_type': '--', 'time': t1},
    {'vectorized': False, 'return_type': 'numpy', 'iterate_type': 'numpy', 'time': t2},
    {'vectorized': False, 'return_type': 'list(dict)', 'iterate_type': 'dict', 'time': t3},
    {'vectorized': True, 'return_type': 'pandas', 'iterate_type': '--', 'time': t4},
    {'vectorized': False, 'return_type': 'pandas', 'iterate_type': 'numpy', 'time': t5},
    {'vectorized': False, 'return_type': 'pandas', 'iterate_type': 'dict', 'time': t6},
    {'vectorized': False, 'return_type': 'pandas', 'iterate_type': 'pandas', 'time': t7},
    {'vectorized': False, 'return_type': 'list', 'iterate_type': 'list', 'time': t8},
    {'vectorized': False, 'return_type': 'numpy', 'iterate_type': 'numpy', 'time': t9},
    {'vectorized': False, 'return_type': 'list', 'iterate_type': 'c array', 'time': t10}
])
d['slowdown'] = np.floor(d.time/d.loc[0,'time'])
d['slowdown'].astype('int').astype('str') + 'X'
d
print(d.to_markdown())