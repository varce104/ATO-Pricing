from models.solver import solve
from results.mean_var import average_excel_solutions
import numpy as np
import pandas as pd
import math


#########################################################################
#################   SOLVER ATO PRICING - MULTI-STAGE    #################
#########################################################################

### PARAMETERS ###

##############################################
# GENERAL SIZE #
comp = 2
prod = 2
branching = [2, 2, 2, 2, 2]  # estructura del árbol de escenarios
time = len(branching) + 1
scenarios = math.prod(branching)
##############################################


##############################################
# BILL OF MATERIALS 
min_use = 1
max_use = 2
w_model = True # if true, 2 products use a shared component and a dedicated one.
##############################################


##############################################
# PRICES
lb_price = 40
ub_price = 80
step_price = 5
##############################################


##############################################
# COSTS
min_cost = 10
max_cost = 20
inv_factor = 0.15
I0 = np.max([lb_price, ub_price]) 
#I0=None
# price --> expected demand --> initial inventory
##############################################



# hacer algo que varíe componentes estocásticas y lead times, y eso iterarlos y promediar variables en excel
############################################## 
#  MULTIPLICATIVE STOCHASTIC COMPONENT - DEMAND
lb_epsilon = 0.75
ub_epsilon = 1.25
##############################################
# ADDITIVE STOCHASTIC COMPONENT - DEMAND
mu_delta = 0
std_delta = 3
##############################################
# PRICE LINEAR EXPRESSION - DEMAND
a = 180
b = 1.6
##############################################
# LEAD TIMES
lb_L = 1
ub_L = 2
det = True
##############################################



##############################################
# EXPERIMENTAL SETTINGS
save_var = True
show_heatmap = False
show_boxplot = True
show_candlestick = True
time_limit = 500
n_instances = 1
seed = 5
##############################################



##############################################
# UNCERTAINTY ANALYSIS
vss_calc = False
evpi_calc = False
vss_ts_calc = False
##############################################


size = comp, prod, time, scenarios, branching, seed, time_limit
bom = min_use, max_use, w_model 
costs = min_cost, max_cost, inv_factor, I0
price_param = lb_price, ub_price, step_price 
demand = a, b, lb_epsilon, ub_epsilon, mu_delta, std_delta
lead_times = lb_L, ub_L, det 
show = save_var, show_heatmap, show_boxplot, show_candlestick, vss_calc, evpi_calc, vss_ts_calc

#solve(size, bom, costs, price_param, demand, lead_times, show)

seeds = [seed + i for i in range(n_instances)]
results = []
files = []

for seed in seeds:
    size = comp, prod, time, scenarios, branching, seed, time_limit
    res = solve(size, bom, costs, price_param, demand, lead_times, show)
    results.append(res)
    files.append(f"var_data/MS_DL_inst{seed}.xlsx" if det else f"var_data/MS_SL_inst{seed}.xlsx")
    

df = pd.DataFrame(results)
df.to_csv(f"var_data/metrics_inst.csv", index=True)

average_excel_solutions(files, output_path="var_data/mean_vars_by_inst/avg_sol.xlsx")