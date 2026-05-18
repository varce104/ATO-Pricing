import numpy as np
import random


def bill_of_materials(comp, prod, min_use, max_use, seed, w_model):
    random.seed(seed)
    np.random.seed(seed)
    A = np.zeros((comp, prod), dtype=int)
    for j in range(prod):
        
        k_j = np.random.randint(min_use, max_use + 1)
        chosen_components = np.random.choice(
            comp,
            size=k_j,
            replace=False)
        A[chosen_components, j] = 1
    if w_model:
        #A = [[1,0],[1,1],[0,1]]
        A = [[1,1],[0,1]]
    return A

def price_set(inf, sup, step):
    return list(range(inf, sup + 1, step))

def parametros(comp, min_cost, max_cost, inv_factor, scenarios, seed, prob=True):
    random.seed(seed)
    np.random.seed(seed)
    
    #cost_compra = [total_cost / total for i in range(comp)]
    cost_compra = [random.randrange(min_cost, max_cost+1, 5) for i in range(comp)]

    cost_inv = [x * inv_factor for x in cost_compra]

    if prob:
        prob_scenarios = [1/scenarios for s in range(scenarios)] # probabilidad uniforme
        return cost_compra, cost_inv, prob_scenarios
    else:
        return cost_compra, cost_inv