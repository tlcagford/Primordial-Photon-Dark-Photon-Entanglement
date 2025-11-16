def compute_rho(k_vals, t_eval, params):
    """
    Compute density matrix evolution with progress tracking
    """
    results = []
    for i, k in enumerate(k_vals):
        if i % 100 == 0:  # Progress indicator
            print(f"Progress: {i}/{len(k_vals)}")
        # ... existing computation
    return np.array(results)