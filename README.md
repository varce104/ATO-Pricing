# Assemble-to-order + Pricing decision problem

The following library optimizes a multistage assemble-to-order model, where component replenishment, production and pricing decisions are made. These decisions are taken under an price-sensitive uncertain demand, as well as a positive and uncertain component lead times. 

## Requirements
 
- Python 3.10+
- [Gurobi](https://www.gurobi.com/) (with valid license)
- `gurobipy`, `numpy`, `pandas`, `openpyxl`, `matplotlib`

## Project Structure
 
```
ATO_PRICING/
├── main.py                        # Entry point. All parameters are set here.
├── instances.py                   # Runs single or multiple seeds; aggregates results.
│
├── data/
│   ├── generator.py               # Generates stochastic scenario tree (ε, δ, lead times).
│   └── params.py                  # BOM, cost, and price set definitions. Includes literature instances.
│
├── models/
│   ├── multistage.py              # Standard multistage stochastic model (nonlinear objective).
│   ├── multistage_FP.py           # Multistage model with pricing as a here-and-now decision.
│   ├── twostage_dlt_slt.py        # Two-stage recourse model (deterministic/stochastic lead times).
│   └── solver.py                  # Model dispatcher: builds, solves, and routes outputs.
│
├── sol_approach/
│   ├── linealization_prop.py      # Linearized multistage model (MILP via auxiliary variable r).
│   ├── affine_funct_app.py        # Multistage affine function approximation (continuous relaxation of w).
│   ├── twostage_affine.py         # Two-stage version of the affine approximation.
│   ├── Benders/
│   │   ├── benders.py             # Benders decomposition loop.
│   │   ├── MP.py                  # Benders master problem.
│   │   └── SP.py                  # Benders subproblem.
│   └── price_policies/
│       └── price_heuristic.py     # Pricing heuristics (from literature).
│
├── uncertainty_analysis/
│   ├── vss.py                     # Value of the Stochastic Solution (VSS).
│   ├── evpi.py                    # Expected Value of Perfect Information (EVPI).
│   ├── vss_ts.py                  # VSS relative to two-stage model.
│   └── sto_computation.py         # Orchestrates uncertainty metrics.
│
├── output_config/
│   ├── results_output.py          # Main export dispatcher.
│   ├── var_export.py              # Extracts and exports solution arrays to Excel.
│   ├── lambda_export.py           # Exports affine policy (λ) results.
│   ├── mean_var.py                # Averages solutions across multiple seeds.
│   └── graphs/
│       ├── boxplot.py
│       ├── candlestick.py
│       └── heatmap.py
│
├── figures/                       # Output figures (generated at runtime).
├── var_results/                   # Output Excel files (generated at runtime).
└── data/                          # (Reserved for data files.)
```
 
---

## Instance Generation
TBD (here all the things that involve paramaters input and the descriptions on these. The corect thing would be define maybe 3-4, all from literature)

## Solver
TBD (talk about the different models, their particularities, and things like lambda handling, output of variables, graphs, several instances, optimal policies, etc)


