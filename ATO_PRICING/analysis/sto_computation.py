from data.generator import epsilon_ms, delta_ms, lead_times_ms
from data.params import parametros, bill_of_materials, price_set
from analysis.vss import VSS
from analysis.evpi import EVPI
from analysis.vss_ts import VSS_2S

import gurobipy as gp
from gurobipy import GRB

def extract_params(size, bom, costs, price, demand, lead_times):

    comp, prod, time, scenarios, branching, seed, _ = size
    min_use, max_use, w_model = bom
    min_cost, max_cost, inv_factor, I0 = costs
    lb_price, ub_price, step_price = price
    a, b, lb_epsilon, ub_epsilon, mu_delta, std_delta = demand
    lb_L, ub_L, det = lead_times

    C, H, pi = parametros(comp, min_cost, max_cost, inv_factor, scenarios, seed)
    A = bill_of_materials(comp, prod, min_use, max_use, seed, w_model)
    price = price_set(lb_price, ub_price, step_price)
    mult = epsilon_ms(time, scenarios, branching, seed, lb_epsilon, ub_epsilon)
    add = delta_ms(prod, time, scenarios, branching, seed, mu_delta, std_delta)
    L = lead_times_ms(comp, time, scenarios, branching, seed, lb_L, ub_L, det)

    if I0 is None:
        I0 = [0] * comp
    else:
        I0 = [gp.quicksum((a - b * I0)*A[i][j] for j in range(prod)) for i in range(comp)]

    return C, H, pi, A, price, mult, add, L, a, b, I0


def uncertainty_analysis(vss_ms, evpi_ms, vss_ts, size, bom, costs, price, demand, lead_times, incumbent):

    C, H, pi, A, price, mult, add, L, a, b, I0 = extract_params(size, bom, costs, price, demand, lead_times)
    _,_, time, scenarios, branching, seed, _ = size  
    _, _, det = lead_times

    if vss_ms:
        vss = VSS(seed, time, scenarios, A, price, L, det, mult, add, a, b, C, H, pi, branching, incumbent, I0)
        print(f"Value of Stochastic Solution (VSS): {vss:.4f}%")
    else:
        vss = -1
        pass

    if vss_ts:
        vss_2s = VSS_2S(seed, time, scenarios, A, price, L, det, mult, add, a, b, C, H, pi, branching, incumbent, I0)
        print(f"Value of Stochastic Solution - Two Stage (VSS_TS): {vss_2s:.4f}%")
        # seed, time, scenarios, A, price, L, L_det, ypsilon, delta, a, b, C, H, pi, branching, incumbent, I0
    else:
        vss_2s = -1
        pass

    if evpi_ms:
        evpi = EVPI(seed, time, scenarios, A, price, L, det, mult, add, a, b, C, H, pi, branching, incumbent, I0)
        print(f"Expected Value of Perfect Information (EVPI): {evpi:.4f}%")
    else:
        evpi = -1
        pass
    return vss, evpi, vss_2s