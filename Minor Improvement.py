# Suggested enhancement in physics.py:
def compute_rho(k_vals, t_eval, params):
    """
    Compute density matrix evolution with enhanced error handling
    """
    try:
        results = []
        for i, k in enumerate(k_vals):
            # Add progress indication for long computations
            if i % 100 == 0:
                print(f"Progress: {i}/{len(k_vals)}")
            
            sol = solve_ivp(von_neumann, t_span, rho0.flatten(), 
                          t_eval=t_eval, args=(k, params), 
                          method='DOP853', rtol=1e-10, atol=1e-12)
            # [rest of existing code]
        return np.array(results)
    except Exception as e:
        print(f"Computation failed: {str(e)}")
        raise