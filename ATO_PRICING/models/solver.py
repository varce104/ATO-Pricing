from data.generator import epsilon_ms, delta_ms, lead_times_ms
from data.params import parametros, bill_of_materials, price_set
from models.multistage import Multistage_problem
from models.multistage_FP import Multistage_problem_Fix_price
from sol_approach.linealization_prop import MS_linear
from sol_approach.affine_funct_app import MS_linear_affine
from sol_approach.Benders.benders import Benders_dec
from analysis.sto_computation import uncertainty_analysis
from results.results_output import export
from results.lambda_export import fix_w_from_lambda

import numpy as np
import pandas as pd
from itertools import product
import gurobipy as gp
from gurobipy import GRB


def extract_params(size, bom, costs, price_param, demand, lead_times):

    comp, prod, stages, scenarios, branching, seed, _ = size
    min_use, max_use, w_model = bom
    min_cost, max_cost, inv_factor, I0 = costs
    lb_price, ub_price, step_price = price_param
    a, b, lb_epsilon, ub_epsilon, mu_delta, std_delta = demand
    lb_L, ub_L, det = lead_times

    C, H, pi = parametros(comp, min_cost, max_cost, inv_factor, scenarios, seed)
    A = bill_of_materials(comp, prod, min_use, max_use, seed, w_model)
    price = price_set(lb_price, ub_price, step_price)
    mult = epsilon_ms(stages, scenarios, branching, seed, lb_epsilon, ub_epsilon)
    add = delta_ms(prod, stages, scenarios, branching, seed, mu_delta, std_delta)
    L = lead_times_ms(comp, stages, scenarios, branching, seed, lb_L, ub_L, det)

    if I0 is None:
        I0 = [0] * comp
    else:
        I0 = [gp.quicksum((a - b * I0)*A[i][j] for j in range(prod)) for i in range(comp)]

    return C, H, pi, A, price, mult, add, L, a, b, I0



def solve(size, bom, costs, price_param, demand, lead_times, show):

    comp, prod, stages, scenarios, branching, seed, time_limit = size  
    C, H, pi, A, price, mult, add, L, a, b, I0 = extract_params(size, bom, costs, price_param, demand, lead_times)
    _,_, det = lead_times
    show_var, lambda_app, lambda_benders, show_heatmap, show_boxplot, show_candlestick, vss_calc, evpi_calc, vss_ts_calc, Model = show


    if Model == "MS":
        m, x_vars, w_vars, y_vars, I_vars, A, D_term = Multistage_problem(
                                                            seed, stages, scenarios, A, price, L, det, mult, add, a, b, C, H, pi, branching, I0)
        if lambda_app:
            w_sim = pd.read_excel(f"var_data/MS_lambda_app_inst{seed}.xlsx", sheet_name='W_sol', index_col=[0, 1, 2])
            fix_w_from_lambda(m, w_vars, w_sim, prod, stages, len(price), scenarios)
        if lambda_benders:
            w_sim = pd.read_excel(f"var_data/MS_benders_inst{seed}.xlsx", sheet_name='W_sol', index_col=[0, 1, 2])
            fix_w_from_lambda(m, w_vars, w_sim, prod, stages, len(price), scenarios)
            

    elif Model == "MS_FP":
        m, x_vars, w_vars, y_vars, I_vars, A, D_term = Multistage_problem_Fix_price(
                                                            seed, stages, scenarios, A, price, L, det, mult, add, a, b, C, H, pi, branching, I0)
        
    elif Model == "MS_linear":
        m, x_vars, w_vars, y_vars, I_vars, A, D_term = MS_linear(
                                                            seed, stages, scenarios, A, price, L, det, mult, add, a, b, C, H, pi, branching, I0)
        if lambda_app:
            w_sim = pd.read_excel(f"var_data/MS_lambda_app_inst{seed}.xlsx", sheet_name='W_sol', index_col=[0, 1, 2])
            fix_w_from_lambda(m, w_vars, w_sim, prod, stages, len(price), scenarios)

    elif Model == "MS_linear_affine":
        m, x_vars, w_vars, y_vars, I_vars, A, D_term, _, _ = MS_linear_affine(
                                                            seed, stages, scenarios, A, price, L, det, mult, add, a, b, C, H, pi, branching, I0)
        
    elif Model == "Benders":
        m, x_vars, w_vars, y_vars, I_vars, A, D_term = Benders_dec(
                                                            seed, stages, scenarios, A, price, L, det, mult, add, a, b, C, H, pi, branching, I0, time_limit)
        return None
    
    else:
        print("\nWrong input, try again...")
        return None
    

    m.setParam('TimeLimit', time_limit)
    m.setParam('OutputFlag', 1)
    m.Params.NonConvex = 0

    m.optimize()
    if m.status == GRB.OPTIMAL:
        incumbent = m.objVal
        bestbd = m.objBound
        gap = 0.0

    elif m.status == GRB.TIME_LIMIT:
        if m.SolCount > 0:
            incumbent = m.objVal
            bestbd = m.objBound
            gap = m.MIPGap
        else:
            incumbent = None
            bestbd = m.objBound
            gap = None

    else:
        incumbent = None
        bestbd = None
        gap = None

    vss, evpi, vss_ts = uncertainty_analysis(vss_calc, evpi_calc, vss_ts_calc, size, bom, costs, price_param, demand, lead_times, incumbent)

    solutions = [seed, x_vars, w_vars, I_vars, y_vars, D_term, price, stages, scenarios, A, det, lambda_app, Model]
    export(show_var, show_heatmap, show_boxplot, show_candlestick, solutions)

    return {"incumbent": incumbent, "bestbd": bestbd, "gap": gap, "time": m.Runtime, "vss": vss, "evpi": evpi, "vss_ts": vss_ts}