import numpy as np
import pandas as pd



def extract_solution_arrays_affine_w(lambda_vars, prod, time, scenarios, pr):
    w_simulada = np.zeros((prod, time, pr, scenarios))
    
    for j in range(prod):
        for t in range(time):
            for s in range(scenarios):
                lambda_values = [lambda_vars[j, t, p, s].X for p in range(pr)]
                best_p = np.argmax(lambda_values)
                w_simulada[j, t, best_p, s] = 1
    return w_simulada


def export_solution_to_excel_affine(filename, w_sim, time, scenarios, pr, A):
    comp, prod = len(A), len(A[0])

    w_bin = extract_solution_arrays_affine_w(w_sim, prod, time, scenarios, pr)
    data_w, indices_w = [], []
    for s in range(scenarios):
        for j in range(prod):
            for p in range(pr):
                data_w.append([w_bin[j, t, p, s] for t in range(time)])
                indices_w.append((f"Scenario_{s}", f"Prod_{j}", f"Price_{p}"))
    df_w = pd.DataFrame(data_w, index=pd.MultiIndex.from_tuples(indices_w, names=["Scenario", "Product", "Price"]), columns=[f"T{t}" for t in range(time)])

    data_lam, indices_lam = [], []
    for s in range(scenarios):
        for j in range(prod):
            for p in range(pr):
                data_lam.append([w_sim[j, t, p, s].X for t in range(time)])
                indices_lam.append((f"Scenario_{s}", f"Prod_{j}", f"Price_{p}"))
    df_lam = pd.DataFrame(data_lam, index=pd.MultiIndex.from_tuples(indices_lam, names=["Scenario", "Product", "Price"]), columns=[f"T{t}" for t in range(time)])

    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df_w.to_excel(writer, sheet_name='W_sol')
            df_lam.to_excel(writer, sheet_name='Lambda_raw')
        print(f"\n>> Resultados exportados a: {filename}")
    except Exception as e:
        print(f"Error al exportar Excel: {e}")




def fix_w_from_lambda(m, w_vars, w_rec, prod, time, pr, scenarios):
    for j in range(prod):
        for t in range(time):
            for p in range(pr):
                for s in range(scenarios):
                    idx = (f"Scenario_{s}", f"Prod_{j}", f"Price_{p}")
                    col = f"T{t}"
                    
                    val = float(w_rec.loc[idx, col])
                    
                    w_vars[j, t, p, s].LB = val
                    w_vars[j, t, p, s].UB = val
                    
    return w_rec