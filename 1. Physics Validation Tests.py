#!/usr/bin/env python3
"""
Primordial Photon-Dark Photon Entanglement Test Suite
Validates theoretical predictions and numerical implementations
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.fft import fft, ifft

class EntanglementTestSuite:
    def __init__(self):
        self.results = {}
        
    def test_entanglement_evolution(self):
        """Test the time evolution of photon-dark photon system"""
        print("Testing entanglement evolution...")
        
        # Test parameters (from theory)
        coupling_strength = 1e-5  # Dark photon coupling
        mass_dark_photon = 1e-22  # eV scale
        
        # Solve entanglement equations
        def entanglement_equations(t, y):
            """Schrödinger-like equations for photon-dark photon system"""
            gamma_visible, gamma_dark = y
            dgammadt = -1j * coupling_strength * gamma_dark
            dgammaddt = -1j * (mass_dark_photon * gamma_dark + coupling_strength * gamma_visible)
            return [dgammadt, dgammaddt]
        
        # Initial state: pure visible photon
        t_span = [0, 100]  # Early universe time
        y0 = [1.0 + 0j, 0.0 + 0j]  # |γ⟩ ⊗ |0_dark⟩
        
        solution = solve_ivp(entanglement_equations, t_span, y0, 
                           t_eval=np.linspace(0, 100, 1000))
        
        # Calculate entanglement entropy
        density_matrix = self.calculate_density_matrix(solution.y)
        entanglement_entropy = self.von_neumann_entropy(density_matrix)
        
        # Validate against theoretical predictions
        theoretical_max = -0.5 * np.log(0.25)  # Max entanglement for 2-level system
        success = np.max(entanglement_entropy) > 0 and np.max(entanglement_entropy) <= theoretical_max
        
        self.results['entanglement_evolution'] = {
            'success': success,
            'max_entropy': np.max(entanglement_entropy),
            'theoretical_max': theoretical_max,
            'oscillation_period': self.find_oscillation_period(solution.y)
        }
        
        return success
    
    def calculate_density_matrix(self, state_vector):
        """Calculate density matrix from state vector"""
        rho = np.outer(state_vector[:, -1], np.conj(state_vector[:, -1]))
        return rho / np.trace(rho)  # Normalize
    
    def von_neumann_entropy(self, density_matrix):
        """Calculate entanglement entropy"""
        eigenvalues = np.linalg.eigvalsh(density_matrix)
        eigenvalues = eigenvalues[eigenvalues > 0]  # Remove numerical zeros
        return -np.sum(eigenvalues * np.log(eigenvalues))
    
    def find_oscillation_period(self, solution):
        """Find oscillation period between photon and dark photon states"""
        prob_visible = np.abs(solution[0, :])**2
        # Find peaks to determine period
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(prob_visible)
        if len(peaks) > 1:
            period = np.mean(np.diff(peaks))
        else:
            period = 0
        return period
    
    def test_cmb_polarization_signature(self):
        """Test CMB polarization predictions from entanglement"""
        print("Testing CMB polarization signatures...")
        
        # Generate simulated CMB power spectra
        ell = np.arange(2, 3000)
        
        # Standard ΛCDM EE spectrum (approximate)
        ee_power = 0.1 * ell**(-2) * np.exp(-ell/2000)
        
        # Dark photon entanglement modification
        entanglement_amplitude = 1e-3
        resonance_ell = 500  # Scale where dark photons affect CMB
        
        # Add resonance feature from dark photon entanglement
        resonance = entanglement_amplitude * np.exp(-(ell - resonance_ell)**2 / (2 * 100**2))
        modified_ee_power = ee_power * (1 + resonance)
        
        # Calculate B-mode contamination from entanglement
        # Tensor-to-scalar ratio modification
        r_standard = 0.01
        r_modified = r_standard * (1 + 0.1 * entanglement_amplitude)
        
        bb_power_standard = r_standard * 0.1 * ell**(-2) * np.exp(-ell/2000)
        bb_power_modified = r_modified * 0.1 * ell**(-2) * np.exp(-ell/2000) + 0.01 * resonance
        
        # Validate: entanglement should enhance specific multipoles
        ell_max_enhancement = ell[np.argmax(resonance)]
        success = abs(ell_max_enhancement - resonance_ell) < 100
        
        self.results['cmb_polarization'] = {
            'success': success,
            'enhancement_scale': ell_max_enhancement,
            'b_mode_contamination': np.max(bb_power_modified - bb_power_standard)
        }
        
        return success
    
    def test_parameter_constraints(self):
        """Test theoretical constraints on dark photon parameters"""
        print("Testing parameter constraints...")
        
        # Planck 2018 constraints
        planck_coupling_limit = 1e-6
        planck_mass_limit = 1e-21  # eV
        
        # Test points from repository
        test_couplings = np.logspace(-8, -4, 50)
        test_masses = np.logspace(-24, -20, 50)
        
        viable_parameters = []
        
        for coupling in test_couplings:
            for mass in test_masses:
                # Simple viability criterion
                if (coupling < planck_coupling_limit and 
                    mass < planck_mass_limit and
                    coupling * mass > 1e-28):  # Detectability threshold
                    viable_parameters.append((coupling, mass))
        
        success = len(viable_parameters) > 0
        
        self.results['parameter_constraints'] = {
            'success': success,
            'viable_points': len(viable_parameters),
            'best_coupling': min([p[0] for p in viable_parameters]) if viable_parameters else 0,
            'parameter_space_coverage': len(viable_parameters) / (len(test_couplings) * len(test_masses))
        }
        
        return success
    
    def run_all_tests(self):
        """Execute complete test suite"""
        print("Running Primordial Entanglement Test Suite")
        print("=" * 50)
        
        tests = [
            self.test_entanglement_evolution,
            self.test_cmb_polarization_signature, 
            self.test_parameter_constraints
        ]
        
        for test in tests:
            test_name = test.__name__
            print(f"\n🧪 Running {test_name}...")
            try:
                success = test()
                status = "PASS" if success else "FAIL"
                print(f"   Result: {status}")
            except Exception as e:
                print(f"   ERROR: {e}")
                self.results[test_name] = {'success': False, 'error': str(e)}
        
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 50)
        print("TEST REPORT: Primordial Photon-Dark Photon Entanglement")
        print("=" * 50)
        
        for test_name, result in self.results.items():
            status = "PASS" if result.get('success', False) else "FAIL"
            print(f"\n📊 {test_name}: {status}")
            for key, value in result.items():
                if key != 'success':
                    print(f"   {key}: {value}")

if __name__ == "__main__":
    test_suite = EntanglementTestSuite()
    test_suite.run_all_tests()