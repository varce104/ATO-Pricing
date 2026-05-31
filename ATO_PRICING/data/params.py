import numpy as np
import random


def bill_of_materials(inst, comp, prod, min_use, max_use, seed, other):
    random.seed(seed)
    np.random.seed(seed)
    A = np.zeros((comp, prod), dtype=int)

    if inst == "Oh_et_al":
        A = [[1,0],[1,1],[0,1]]

    elif inst == "Oh_et_al_2":
        comp = 11; prod = 11; min_use = 4; max_use = 7
        A = np.zeros((comp, prod), dtype=int)       
        for j in range(prod):
            k_j = np.random.randint(min_use, max_use + 1)
            chosen_components = np.random.choice(
                comp,
                size=k_j,
                replace=False)
            A[chosen_components, j] = 1

    else:
        for j in range(prod):
            k_j = np.random.randint(min_use, max_use + 1)
            chosen_components = np.random.choice(
                comp,
                size=k_j,
                replace=False)
            A[chosen_components, j] = 1

        if other:
            A = [[1,0],[1,1],[0,1]]
            #A = [[1,1],[0,1]]        

    return A


def price_set(inst, inf, sup, step):
    if inst == "Oh_et_al":
        inf = 15; sup = 60
    
    elif inst == "Oh_et_al_2":
        inf = 30; sup = 80

    else:
        pass
    return list(range(inf, sup + 1, step))


def parametros(inst, comp, min_cost, max_cost, inv_factor, scenarios, seed, prob=True):
    random.seed(seed)
    np.random.seed(seed)
    
    if inst == "Oh_et_al":
        C = [5, 5, 45]; I = [4, 4, 36]

    elif inst == "Oh_et_al_2":
        comp = 11; min_cost = 5; max_cost = 25; inv_factor = 0.15
        C_raw = [random.randrange(min_cost, max_cost+1, 5) for i in range(comp)]
        total_cost = sum(C_raw)
        C = [int(round(x * 55 / total_cost)) for x in C_raw]
        I = [x * inv_factor for x in C]

    else:
        C = [random.randrange(min_cost, max_cost+1, 5) for i in range(comp)]
        I = [x * inv_factor for x in C]

    if prob:
        prob_scenarios = [1/scenarios for s in range(scenarios)] # probabilidad uniforme
        return C, I, prob_scenarios
    else:
        return C, I