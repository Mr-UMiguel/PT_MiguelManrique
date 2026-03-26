
## Data and systme handling libraries 
import json
import os

## optimization library
import pulp

## constant path settings
ROOTH_PATH  = os.getcwd()
SOURCE_PATH = os.path.join(ROOTH_PATH, './source')
FILE_PATH   = os.path.join(SOURCE_PATH, 'reserve_trust.json')

## RESTRICTIONS
REQUIRED_LIQUIDITY = 0.4
REQUIRED_HAIRCUT   = 0.99
REQUIRED_WAL = 60


with open(FILE_PATH, "r") as f:
    data = json.load(f)

assets  = [i['id'] for i in data['assets']]
ayield = {i['id']: i['yield'] for i in data['assets']}
wal = {i['id']: i['wal'] for i in data['assets']}
liquidty = {i['id']: i['liquidity'] for i in data['assets']}
haircut = {i['id']: i['haircut'] for i in data['assets']}
internal_caps = {i['id']: i['internal_cap'] for i in data['assets']} 


## Initial settings
eq = pulp.LpProblem("MaximizeYield", pulp.LpMaximize)
w = pulp.LpVariable.dicts("weight", assets, lowBound=0, upBound=1)

## Objective function
eq += pulp.lpSum([ayield[a] * w[a] for a in assets])


## Restrictions
eq += pulp.lpSum([w[a] for a in assets]) == 1
eq += pulp.lpSum([liquidty[a] * w[a] for a in assets]) >= REQUIRED_LIQUIDITY
eq += pulp.lpSum([haircut[a] * w[a] for a in assets]) >= REQUIRED_HAIRCUT
for a in assets:
    eq += w[a] <= internal_caps[a]
for a in assets:
    eq += wal[a] <= REQUIRED_WAL

eq.solve(pulp.PULP_CBC_CMD(msg=0))

print(pulp.LpStatus[eq.status])
print("Optimal Portfolio Weights:")
for a in assets:
    print( f"{a}: {w[a].varValue:.2%}" )
print(f"optimal yield: {pulp.value(eq.objective):.2%}")

