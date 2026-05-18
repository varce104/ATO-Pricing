# Assemble-to-order + Pricing decision problem

The following library optimizes a multistage assemble-to-order model, where component replenishment, production and pricing decisions are made. These decisions are taken under an price-sensitive uncertain demand, as well as a positive and uncertain component lead times. 

The code comprises several formulations for the base multistage model. 

## Code Structure
|___ main.py\
|___ instances.py\
|___ analysis\
|    |___ vss.py\
|    |___ evpi.py\
|    |___ vss_ts.py\
|    |___ sto_computation.py\
|\
|___ data\
|    |___ generator.py\
|    |___ params.py
|
|___ models
|    |___ multistage.py
|    |___ multistage_FP.py
|    |___ twostage_dlt_slt.py
|    |___ solver.py
|
|___ results
|    |___ boxplot.py
|    |___ candlestick.py
|    |___ heatmap.py
|    |___ var_export.py
|    |___ lambda_export.py
|    |___ mean_var.py
|    |___ var_export.py
|    |___ results_output.py
|   
|___ sol_approach
|    |___ Benders
|    |    |___ MP.py
|    |    |___ SP.py
|    |    |___ benders.py
|    |
|    |___ linealization_prop.py
|    |___ affine_funct_app.py




