def compute_rho(k_vals, t_eval, params):
    """
    Compute density matrix evolution for photon-dark photon system.
    
    Parameters
    ----------
    k_vals : array_like
        Comoving momentum values to evaluate
    t_eval : array_like  
        Time points at which to store the computed solution
    params : dict
        Physical parameters (masses, mixing, Hubble)
        
    Returns
    -------
    results : ndarray
        Array of density matrices for each k and time
    """
    try:
        results = []
        total_k = len(k_vals)
        
        for i, k in enumerate(k_vals):
            # Progress indication for computationally intensive runs
            if i % max(1, total_k // 10) == 0:  # Print ~10 updates
                print(f"Progress: {i}/{total_k} (k = {k:.2e})")
            
            # Solve von Neumann equation for this k
            sol = solve_ivp(von_neumann, [t_eval[0], t_eval[-1]], 
                          rho0.flatten(), t_eval=t_eval, 
                          args=(k, params), method='DOP853',
                          rtol=1e-10, atol=1e-12)
            
            # Reshape solution back to density matrix format
            rho_t = sol.y.reshape(2, 2, -1)
            results.append(rho_t)
            
        return np.array(results)
        
    except Exception as e:
        print(f"Computation failed at k-index {i}, k = {k:.2e}: {str(e)}")
        raise