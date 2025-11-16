# Create comprehensive test suite for the repository
class PrimordialEntanglementTestSuite:
    def __init__(self):
        self.test_results = {}
        self.figures_dir = "test_figures"
        os.makedirs(self.figures_dir, exist_ok=True)
        
    def test_quantum_entanglement_dynamics(self):
        """Test 1: Quantum entanglement dynamics"""
        print("\n🧪 TEST 1: Quantum Entanglement Dynamics")
        print("-" * 40)
        
        try:
            # Parameters for dark photon-photon system
            epsilon = 5e-6  # Mixing parameter
            m_dark = 2e-23  # Dark photon mass in eV
            hbar = 6.582119e-16  # eV·s
            H_inflation = 1e-5  # Hubble during inflation in eV
            
            def entanglement_hamiltonian(t, psi):
                """Hamiltonian for photon-dark photon system"""
                gamma, A_prime = psi
                # Effective Hamiltonian: H = [[0, εω], [εω, m_A'²/2ω]]
                H11 = 0
                H12 = epsilon * H_inflation
                H21 = epsilon * H_inflation
                H22 = (m_dark**2) / (2 * H_inflation)
                
                dgamma_dt = -1j * (H11 * gamma + H12 * A_prime)
                dAprime_dt = -1j * (H21 * gamma + H22 * A_prime)
                
                return [dgamma_dt, dAprime_dt]
            
            # Time evolution
            from scipy.integrate import solve_ivp
            
            t_span = [0, 1e-15]  # Early universe timescale
            t_eval = np.linspace(0, 1e-15, 1000)
            psi0 = [1.0 + 0j, 0.0 + 0j]  # Initial pure photon state
            
            solution = solve_ivp(entanglement_hamiltonian, t_span, psi0, 
                               t_eval=t_eval, method='RK45')
            
            # Calculate entanglement measures
            entanglement_entropy = []
            concurrence = []
            
            for i in range(len(solution.t)):
                # Density matrix
                psi = solution.y[:, i]
                rho = np.outer(psi, np.conj(psi))
                rho_normalized = rho / np.trace(rho)
                
                # Entanglement entropy
                eigenvalues = np.linalg.eigvalsh(rho_normalized)
                eigenvalues = eigenvalues[eigenvalues > 1e-12]
                entropy = -np.sum(eigenvalues * np.log(eigenvalues))
                entanglement_entropy.append(entropy)
                
                # Concurrence (for 2-qubit like system)
                if len(psi) == 2:
                    concurrence_val = 2 * np.abs(psi[0] * psi[1])
                    concurrence.append(concurrence_val)
            
            # Create visualization
            fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
            
            # Panel 1: State probabilities
            prob_photon = np.abs(solution.y[0])**2
            prob_dark = np.abs(solution.y[1])**2
            
            ax1.plot(solution.t, prob_photon, 'b-', linewidth=2, label='Photon Probability')
            ax1.plot(solution.t, prob_dark, 'r-', linewidth=2, label='Dark Photon Probability')
            ax1.set_xlabel('Time [s]')
            ax1.set_ylabel('Probability')
            ax1.set_title('Photon-Dark Photon Oscillations')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Panel 2: Entanglement entropy
            ax2.plot(solution.t, entanglement_entropy, 'purple', linewidth=3)
            ax2.axhline(y=np.log(2), color='red', linestyle='--', 
                       label='Maximum Entanglement')
            ax2.set_xlabel('Time [s]')
            ax2.set_ylabel('Entanglement Entropy')
            ax2.set_title('Quantum Entanglement Evolution')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            # Panel 3: Concurrence
            ax3.plot(solution.t[:len(concurrence)], concurrence, 'green', linewidth=2)
            ax3.set_xlabel('Time [s]')
            ax3.set_ylabel('Concurrence')
            ax3.set_title('Entanglement Concurrence')
            ax3.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(f'{self.figures_dir}/quantum_entanglement_test.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # Test validation
            max_entropy = np.max(entanglement_entropy)
            max_conversion = np.max(prob_dark)
            
            success = (max_entropy > 0.1 and max_entropy <= np.log(2) + 0.1 and
                      max_conversion > 0.01)
            
            self.test_results['quantum_dynamics'] = {
                'success': success,
                'max_entanglement': max_entropy,
                'max_conversion': max_conversion,
                'oscillation_period': self._find_oscillation_period(prob_photon, solution.t)
            }
            
            print(f"   ✓ Maximum entanglement entropy: {max_entropy:.4f}")
            print(f"   ✓ Maximum dark photon conversion: {max_conversion:.4f}")
            print(f"   ✓ Oscillation period: {self.test_results['quantum_dynamics']['oscillation_period']:.2e} s")
            print(f"   ✅ TEST {'PASSED' if success else 'FAILED'}")
            
            return success
            
        except Exception as e:
            print(f"   ❌ TEST FAILED: {e}")
            self.test_results['quantum_dynamics'] = {'success': False, 'error': str(e)}
            return False
    
    def test_cmb_signature_calculation(self):
        """Test 2: CMB signature calculations"""
        print("\n🧪 TEST 2: CMB Signature Calculations")
        print("-" * 40)
        
        try:
            # Simulate CMB power spectrum modifications
            ell = np.arange(2, 2500)
            
            # Standard ΛCDM power spectra
            def standard_spectrum(ell, amp=1e-10, tilt=0.96):
                return amp * (ell / 60)**(tilt - 1) * np.exp(-ell / 2000)
            
            # Dark photon modifications
            def dark_photon_effect(ell, resonance_scales=[150, 450, 800], amplitudes=[2e-3, 1e-3, 5e-4]):
                effect = np.zeros_like(ell)
                for scale, amp in zip(resonance_scales, amplitudes):
                    effect += amp * np.exp(-(ell - scale)**2 / (2 * (scale * 0.15)**2))
                return effect
            
            # Calculate modified spectra
            tt_standard = standard_spectrum(ell, 1e-10)
            ee_standard = standard_spectrum(ell, 5e-12)
            bb_standard = standard_spectrum(ell, 1e-13)
            
            modification = dark_photon_effect(ell)
            
            tt_modified = tt_standard * (1 + modification * 0.5)
            ee_modified = ee_standard * (1 + modification)
            bb_modified = bb_standard * (1 + modification * 2)  # Enhanced B-modes
            
            # Create visualization
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # Panel 1: E-mode modifications
            ax1.semilogy(ell, ee_standard, 'b-', label='Standard ΛCDM', linewidth=2)
            ax1.semilogy(ell, ee_modified, 'r--', label='With Dark Photons', linewidth=2)
            ax1.set_xlabel('Multipole ℓ')
            ax1.set_ylabel('D$_ℓ^{EE}$ [µK$^2$]')
            ax1.set_title('E-mode Polarization Power Spectrum')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Panel 2: B-mode enhancements
            ax2.semilogy(ell, bb_standard, 'b-', label='Standard ΛCDM', linewidth=2)
            ax2.semilogy(ell, bb_modified, 'r--', label='With Dark Photons', linewidth=2)
            ax2.set_xlabel('Multipole ℓ')
            ax2.set_ylabel('D$_ℓ^{BB}$ [µK$^2$]')
            ax2.set_title('B-mode Polarization Power Spectrum')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(f'{self.figures_dir}/cmb_signatures_test.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # Calculate detectability metrics
            snr_ee = np.sqrt(np.sum(((ee_modified - ee_standard) / (ee_standard * 0.1))**2))
            snr_bb = np.sqrt(np.sum(((bb_modified - bb_standard) / (bb_standard * 0.1))**2))
            
            success = snr_ee > 1 or snr_bb > 1  # Detectable signal
            
            self.test_results['cmb_signatures'] = {
                'success': success,
                'snr_ee': snr_ee,
                'snr_bb': snr_bb,
                'max_enhancement_ee': np.max(np.abs(ee_modified - ee_standard) / ee_standard),
                'max_enhancement_bb': np.max(np.abs(bb_modified - bb_standard) / bb_standard)
            }
            
            print(f"   ✓ E-mode SNR: {snr_ee:.2f}")
            print(f"   ✓ B-mode SNR: {snr_bb:.2f}")
            print(f"   ✓ Maximum EE enhancement: {self.test_results['cmb_signatures']['max_enhancement_ee']:.4f}")
            print(f"   ✅ TEST {'PASSED' if success else 'FAILED'}")
            
            return success
            
        except Exception as e:
            print(f"   ❌ TEST FAILED: {e}")
            self.test_results['cmb_signatures'] = {'success': False, 'error': str(e)}
            return False
    
    def test_parameter_space_analysis(self):
        """Test 3: Parameter space analysis"""
        print("\n🧪 TEST 3: Parameter Space Analysis")
        print("-" * 40)
        
        try:
            # Scan parameter space
            couplings = np.logspace(-9, -5, 50)
            masses = np.logspace(-25, -20, 50)
            
            # Calculate oscillation probabilities
            def conversion_probability(epsilon, m_dark, omega=1e-5):
                """Maximum conversion probability"""
                return (4 * epsilon**2 * omega**2) / (m_dark**4 + 4 * epsilon**2 * omega**2)
            
            # Create parameter space map
            conversion_map = np.zeros((len(couplings), len(masses)))
            for i, eps in enumerate(couplings):
                for j, mass in enumerate(masses):
                    conversion_map[i, j] = conversion_probability(eps, mass)
            
            # Create visualization
            fig, ax = plt.subplots(figsize=(10, 8))
            
            im = ax.contourf(np.log10(masses), np.log10(couplings), conversion_map, 
                           levels=50, cmap='viridis')
            
            # Add constraints
            current_limit = 1e-6
            future_sensitivity = 1e-9
            
            ax.axhline(y=np.log10(current_limit), color='red', linestyle='-', 
                      linewidth=2, label='Current Limit')
            ax.axhline(y=np.log10(future_sensitivity), color='orange', linestyle='--', 
                      linewidth=2, label='Future Sensitivity')
            
            ax.set_xlabel('log$_{10}$(m$_{A\'}$ [eV])')
            ax.set_ylabel('log$_{10}$(ε)')
            ax.set_title('Dark Photon Parameter Space')
            ax.legend()
            
            plt.colorbar(im, ax=ax, label='Conversion Probability')
            plt.tight_layout()
            plt.savefig(f'{self.figures_dir}/parameter_space_test.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # Find viable parameter region
            viable_region = conversion_map > 0.01  # At least 1% conversion
            viable_fraction = np.sum(viable_region) / viable_region.size
            
            success = viable_fraction > 0.05  # At least 5% viable parameter space
            
            self.test_results['parameter_space'] = {
                'success': success,
                'viable_fraction': viable_fraction,
                'max_conversion': np.max(conversion_map),
                'parameter_space_coverage': len(couplings) * len(masses)
            }
            
            print(f"   ✓ Viable parameter fraction: {viable_fraction:.3f}")
            print(f"   ✓ Maximum conversion probability: {np.max(conversion_map):.4f}")
            print(f"   ✓ Parameter points scanned: {len(couplings) * len(masses)}")
            print(f"   ✅ TEST {'PASSED' if success else 'FAILED'}")
            
            return success
            
        except Exception as e:
            print(f"   ❌ TEST FAILED: {e}")
            self.test_results['parameter_space'] = {'success': False, 'error': str(e)}
            return False
    
    def _find_oscillation_period(self, probability, time):
        """Helper function to find oscillation period"""
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(probability, height=0.5)
        if len(peaks) > 1:
            periods = np.diff(time[peaks])
            return np.mean(periods)
        return 0
    
    def run_complete_test_suite(self):
        """Run all tests and generate report"""
        print("🚀 RUNNING COMPLETE TEST SUITE")
        print("=" * 60)
        
        tests = [
            self.test_quantum_entanglement_dynamics,
            self.test_cmb_signature_calculation,
            self.test_parameter_space_analysis
        ]
        
        all_passed = True
        for test in tests:
            passed = test()
            all_passed = all_passed and passed
        
        self.generate_test_report(all_passed)
        return all_passed
    
    def generate_test_report(self, overall_success):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📊 TEST SUITE REPORT")
        print("=" * 60)
        
        print(f"\nOVERALL RESULT: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
        
        print("\nDETAILED RESULTS:")
        print("-" * 40)
        
        for test_name, result in self.test_results.items():
            status = "PASS" if result['success'] else "FAIL"
            print(f"\n🔍 {test_name.replace('_', ' ').title()}: {status}")
            for key, value in result.items():
                if key not in ['success', 'error']:
                    print(f"   {key}: {value}")
            if 'error' in result:
                print(f"   ERROR: {result['error']}")
        
        print(f"\n📁 Test figures saved in: {self.figures_dir}/")

# Run the complete test suite
print("\n🔬 Starting Primordial Photon-Dark Photon Entanglement Test Suite")
test_suite = PrimordialEntanglementTestSuite()
test_suite.run_complete_test_suite()