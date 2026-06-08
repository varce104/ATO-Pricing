import gurobipy as gp
from gurobipy import GRB
import numpy as np
from sol_approach.affine_funct_app import MS_linear_affine
from sol_approach.linealization_prop import MS_linear
from output_config.lambda_export import extract_solution_arrays_affine_w

def fix_variables(model_vars, fixed_vals, is_dict=True):
    if is_dict:
        for key, val in fixed_vals.items():
            model_vars[key].LB = val
            model_vars[key].UB = val
    else:
        it = np.nditer(fixed_vals, flags=['multi_index'])
        for val in it:
            model_vars[it.multi_index].LB = val
            model_vars[it.multi_index].UB = val

def iterative_pricing_inventory(seed, time_periods, scenarios, A, price, L, L_det, ypsilon, delta, a, b, C, H, 
                                pi, branching_structure, I0, max_iter=5, tol=1e-2):
    import time

    comp, prod, pr = len(A), len(A[0]), len(price)

    print("\n--------- Iteracion 0: Resolviendo Modelo Afin Inicial ---------\n")
    m_af, x_af, lam_w, y_af, I_af, _, D_af, rho, Gamma = MS_linear_affine(
        seed, time_periods, scenarios, A, price, L, L_det, ypsilon, delta, a, b, C, H, pi, branching_structure, I0)
    start = time.time()
    
    m_af.setParam('OutputFlag', 1)
    m_af.optimize()

    
    w_bin = extract_solution_arrays_affine_w(lam_w, prod, time_periods, scenarios, pr)
    
    

    for iteration in range(1, max_iter + 1):
        print(f"\n--------- Iteracion {iteration} ---------\n")
        
        m_lin, x_lin, w_lin, y_lin, I_lin, _, D_lin = MS_linear(
            seed, time_periods, scenarios, A, price, L, L_det, ypsilon, delta, a, b, C, H, pi, branching_structure, I0)
        
        fix_variables(w_lin, w_bin, is_dict=False)
        
        m_lin.setParam('OutputFlag', 1)
        m_lin.optimize()
        
        if m_lin.status != GRB.OPTIMAL:
            print("\n ##### Fase Inventario Infactible/No optima. Abortando #####\n")
            break
            
        obj_lin = m_lin.objVal

        print(f"\nObj Fase Inventario (Precio Fijo): {obj_lin}\n")
        
        x_fixed = {(i, t, s): x_lin[i, t, s].X for i in range(comp) for t in range(time_periods) for s in range(scenarios)}
        
        m_af, x_af, lam_w, y_af, _, _, _, rho, Gamma = MS_linear_affine(
            seed, time_periods, scenarios, A, price, L, L_det, ypsilon, delta, a, b, C, H, pi, branching_structure, I0)
        
        fix_variables(x_af, x_fixed, is_dict=True)
        
        m_af.setParam('OutputFlag', 1)
        m_af.optimize()
        
        if m_af.status != GRB.OPTIMAL:
            print("\n ##### Fase Precio Infactible/No óptima. Abortando #####\n")
            break
            
        obj_af = m_af.objVal

        print(f"\n--- Obj Fase Precio (Compras Fijas): {obj_af} ---\n")
        
        if abs(obj_af - best_obj) < tol:
            print(f"\n ------ Convergencia alcanzada. Iteracion {iteration} ------\n")
            break
            
        best_obj = obj_af
        
        w_bin = extract_solution_arrays_affine_w(lam_w, prod, time_periods, scenarios, pr)
    end = time.time()
    exec_time = end - start
    return m_lin, obj_lin, exec_time