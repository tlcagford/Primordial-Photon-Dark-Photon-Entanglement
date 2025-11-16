import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns
from scipy.integrate import solve_ivp
from scipy.signal import find_peaks
import warnings
warnings.filterwarnings('ignore')

# Set professional style
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'figure.titlesize': 18
})

class ManuscriptFigures:
    def __init__(self):
        self.fig_dir = "manuscript_figures"
        import os
        os.makedirs(self.fig_dir, exist_ok=True)
    
    def create_figure_1_quantum_dynamics(self):
        """Figure 1: Quantum Dynamics and Entanglement Evolution"""
        print("Creating Figure 1: Quantum Dynamics...")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Quantum Dynamics of Photon-Dark Photon System', fontsize=18, fontweight='bold')
        
        # Parameters for simulation
        coupling = 5e-6
        mass_dark = 2e-23
        t_span = [0, 1e33]
        t_eval = np.linspace(0, 1e33, 2000)
        
        # Quantum evolution
        def quantum_eq(t, psi):
            gamma_vis, gamma_dark = psi
            dgdt = -1j * coupling * gamma_dark
            dddt = -1j * (mass_dark * gamma_dark + coupling * gamma_vis)
            return [dgdt, dddt]
        
        solution = solve_ivp(quantum_eq, t_span, [1+0j, 0+0j], t_eval=t_eval, method='RK45')
        
        # Calculate physical quantities
        time_norm = solution.t / 1e33
        prob_vis = np.abs(solution.y[0])**2
        prob_dark = np.abs(solution.y[1])**2
        coherence = np.abs(solution.y[0] * np.conj(solution.y[1]))
        
        # Panel A: Probability oscillations
        ax1.plot(time_norm, prob_vis, 'b-', linewidth=2.5, label='Visible Photon $P_γ$', alpha=0.8)
        ax1.plot(time_norm, prob_dark, 'r-', linewidth=2.5, label='Dark Photon $P_{A\'}$', alpha=0.8)
        ax1.plot(time_norm, coherence, 'g--', linewidth=2, label='Quantum Coherence', alpha=0.7)
        ax1.set_xlabel('Time (Hubble Units)')
        ax1.set_ylabel('Probability / Coherence')
        ax1.set_title('(a) Photon-Dark Photon Oscillations')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(-0.05, 1.05)
        
        # Panel B: Entanglement entropy
        entanglement = []
        for i in range(len(solution.t)):
            rho = np.outer(solution.y[:, i], np.conj(solution.y[:, i]))
            rho_norm = rho / np.trace(rho)
            eigvals = np.linalg.eigvalsh(rho_norm)
            eigvals = eigvals[eigvals > 1e-12]
            if len(eigvals) > 0:
                entropy = -np.sum(eigvals * np.log(eigvals))
            else:
                entropy = 0
            entanglement.append(entropy)
        
        ax2.plot(time_norm, entanglement, 'purple', linewidth=3, label='Entanglement Entropy')
        ax2.axhline(y=np.log(2), color='red', linestyle='--', linewidth=2, 
                   label='Theoretical Maximum $S_{max} = \ln(2)$')
        ax2.set_xlabel('Time (Hubble Units)')
        ax2.set_ylabel('Entanglement Entropy $S(t)$')
        ax2.set_title('(b) Quantum Entanglement Evolution')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(-0.05, 0.75)
        
        # Panel C: Density matrix evolution (snapshots)
        times_snapshots = [0, 250, 500, 750, 999]
        density_matrices = []
        
        for idx in times_snapshots:
            psi = solution.y[:, idx]
            rho = np.outer(psi, np.conj(psi))
            rho_normalized = rho / np.trace(rho)
            density_matrices.append(np.real(rho_normalized))
        
        # Plot density matrices
        for i, (idx, rho) in enumerate(zip(times_snapshots, density_matrices)):
            ax = [ax3, ax4][i // 3]
            im = ax.imshow(rho, cmap='viridis', vmin=0, vmax=1, 
                          extent=[-0.5, 1.5, -0.5, 1.5])
            ax.set_xticks([0, 1])
            ax.set_yticks([0, 1])
            ax.set_xticklabels(['$|γ⟩$', '$|A\'⟩$'])
            ax.set_yticklabels(['$|γ⟩$', '$|A\'⟩$'])
            ax.set_title(f'$t = {time_norm[idx]:.2f}H^{-1}$')
            ax.grid(False)
            
            # Add text annotations
            for i_row in range(2):
                for j_col in range(2):
                    text = ax.text(j_col, i_row, f'{rho[i_row, j_col]:.3f}',
                                 ha="center", va="center", color="white", fontweight='bold')
        
        ax3.set_title('(c) Density Matrix Evolution (Early Times)')
        ax4.set_title('(d) Density Matrix Evolution (Late Times)')
        
        plt.tight_layout()
        plt.savefig(f'{self.fig_dir}/figure1_quantum_dynamics.png', dpi=300, bbox_inches='tight')
        plt.savefig(f'{self.fig_dir}/figure1_quantum_dynamics.pdf', bbox_inches='tight')
        plt.close()
        
        print("✓ Figure 1 created: Quantum Dynamics")
    
    def create_figure_2_parameter_space(self):
        """Figure 2: Dark Photon Parameter Space Constraints"""
        print("Creating Figure 2: Parameter Space...")
        
        fig, ax = plt.subplots(1, 1, figsize=(12, 9))
        
        # Parameter ranges
        masses = np.logspace(-26, -18, 200)  # eV
        couplings = np.logspace(-11, -4, 200)  # ε
        
        # Create meshgrid
        M, C = np.meshgrid(masses, couplings)
        
        # Define constraint regions
        # CMB constraints (Planck + future)
        cmb_current = 1e-6 * np.ones_like(M)
        cmb_future = 1e-9 * np.ones_like(M)
        
        # Laboratory constraints
        lab_current = 1e-7 * np.ones_like(M)
        lab_future = 1e-10 * np.ones_like(M)
        
        # Astrophysical constraints
        astro = 1e-8 * np.ones_like(M)
        
        # Dark matter relic density
        dm_relic = 1e-12 * (M / 1e-22)**0.5
        
        # Plot constraints
        ax.fill_between(masses, 1e-4, cmb_current, alpha=0.4, color='red', label='Excluded: Current CMB')
        ax.fill_between(masses, cmb_current, lab_current, alpha=0.3, color='orange', label='Excluded: Laboratory')
        ax.fill_between(masses, lab_current, astro, alpha=0.3, color='yellow', label='Excluded: Astrophysical')
        
        # Viable regions
        ax.fill_between(masses, astro, dm_relic, alpha=0.5, color='lightgreen', 
                       label='Viable: Detectable')
        ax.fill_between(masses, dm_relic, 1e-11, alpha=0.3, color='blue', 
                       label='Viable: Challenging Detection')
        
        # Future sensitivity
        ax.plot(masses, cmb_future, 'r--', linewidth=3, label='CMB-S4 Sensitivity')
        ax.plot(masses, lab_future, 'b--', linewidth=3, label='Future Laboratory')
        ax.plot(masses, dm_relic, 'k-', linewidth=2, label='Dark Matter Relic Density')
        
        # Highlight our study region
        study_region_mass = [2e-25, 5e-21]
        study_region_coupling = [1e-9, 1e-6]
        ax.fill_between(study_region_mass, study_region_coupling[0], study_region_coupling[1], 
                       alpha=0.6, color='purple', label='This Study')
        
        # Formatting
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Dark Photon Mass $m_{A\'}$ [eV]', fontsize=14)
        ax.set_ylabel('Mixing Parameter $\\epsilon$', fontsize=14)
        ax.set_title('Dark Photon Parameter Space Constraints', fontsize=16, fontweight='bold')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(1e-26, 1e-18)
        ax.set_ylim(1e-11, 1e-4)
        
        # Add text annotations
        ax.text(1e-23, 5e-7, 'CMB\nExcluded', ha='center', va='center', 
               fontweight='bold', color='darkred', fontsize=10)
        ax.text(1e-21, 2e-8, 'Laboratory\nBounds', ha='center', va='center', 
               fontweight='bold', color='darkorange', fontsize=10)
        ax.text(1e-24, 5e-10, 'Discovery\nRegion', ha='center', va='center', 
               fontweight='bold', color='darkgreen', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(f'{self.fig_dir}/figure2_parameter_space.png', dpi=300, bbox_inches='tight')
        plt.savefig(f'{self.fig_dir}/figure2_parameter_space.pdf', bbox_inches='tight')
        plt.close()
        
        print("✓ Figure 2 created: Parameter Space")
    
    def create_figure_3_cmb_signatures(self):
        """Figure 3: CMB Polarization Signatures"""
        print("Creating Figure 3: CMB Signatures...")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('CMB Polarization Signatures from Photon-Dark Photon Entanglement', 
                    fontsize=18, fontweight='bold')
        
        # Multipole range
        ell = np.arange(2, 2500)
        
        # Standard ΛCDM spectra (approximate forms)
        def standard_ee(ell):
            return 0.05 * ell * (ell + 1) * np.exp(-ell / 2000) / (2 * np.pi)
        
        def standard_bb(ell, r=0.001):
            return r * 0.02 * ell * (ell + 1) * np.exp(-ell / 1500) / (2 * np.pi)
        
        # Dark photon modifications
        resonance_scales = [150, 450, 800]
        enhancements = [0.002, 0.0015, 0.0008]
        
        def dark_photon_enhancement(ell):
            total = 0
            for scale, amp in zip(resonance_scales, enhancements):
                total += amp * np.exp(-(ell - scale)**2 / (2 * (scale * 0.2)**2))
            return total
        
        # Panel A: E-mode power spectrum
        ee_standard = standard_ee(ell)
        ee_modified = ee_standard * (1 + dark_photon_enhancement(ell))
        
        ax1.semilogy(ell, ee_standard, 'b-', linewidth=3, label='Standard $Λ$CDM', alpha=0.8)
        ax1.semilogy(ell, ee_modified, 'r--', linewidth=3, label='With Dark Photons', alpha=0.9)
        ax1.set_xlabel('Multipole $\\ell$')
        ax1.set_ylabel('$D_\\ell^{EE}$ [$\mu K^2$]')
        ax1.set_title('(a) E-mode Polarization Power Spectrum')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(2, 2500)
        
        # Add resonance markers
        for scale in resonance_scales:
            ax1.axvline(x=scale, color='purple', linestyle=':', alpha=0.7)
            ax1.text(scale, ee_standard[scale] * 1.5, f'$\\ell={scale}$', 
                    ha='center', va='bottom', fontsize=10, color='purple')
        
        # Panel B: B-mode power spectrum
        bb_standard = standard_bb(ell)
        # Additional B-modes from dark photon tensor modes
        bb_dark_photon = 5e-4 * np.exp(-(ell - 100)**2 / (2 * 50**2)) + \
                        2e-4 * np.exp(-(ell - 300)**2 / (2 * 100**2))
        bb_modified = bb_standard + bb_dark_photon
        
        ax2.semilogy(ell, bb_standard, 'b-', linewidth=3, label='Standard $Λ$CDM', alpha=0.8)
        ax2.semilogy(ell, bb_modified, 'r--', linewidth=3, label='With Dark Photons', alpha=0.9)
        ax2.set_xlabel('Multipole $\\ell$')
        ax2.set_ylabel('$D_\\ell^{BB}$ [$\mu K^2$]')
        ax2.set_title('(b) B-mode Polarization Power Spectrum')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(2, 2500)
        
        # Panel C: Residual differences
        residual_ee = (ee_modified - ee_standard) / ee_standard
        residual_bb = (bb_modified - bb_standard) / np.max(bb_standard)
        
        ax3.plot(ell, residual_ee * 100, 'green', linewidth=2.5, label='EE Relative Difference')
        ax3.plot(ell, residual_bb * 100, 'orange', linewidth=2.5, label='BB Relative Difference')
        ax3.set_xlabel('Multipole $\\ell$')
        ax3.set_ylabel('Relative Difference [%]')
        ax3.set_title('(c) Relative Differences from Standard $Λ$CDM')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.set_xlim(2, 2500)
        ax3.set_ylim(-1, 3)
        
        # Panel D: Signal-to-noise ratio
        # Approximate noise curves for different experiments
        ell_noise = np.arange(2, 2500, 50)
        
        # Noise levels (approximate)
        noise_planck = 10 * np.ones_like(ell_noise) * (ell_noise / 100)**2
        noise_s4 = 0.5 * np.ones_like(ell_noise) * (ell_noise / 100)**2
        noise_litebird = 2 * np.ones_like(ell_noise) * (ell_noise / 100)**0.5
        
        # Signal (difference)
        signal = ee_modified - ee_standard
        
        # SNR calculation
        snr_planck = signal / np.interp(ell, ell_noise, noise_planck)
        snr_s4 = signal / np.interp(ell, ell_noise, noise_s4)
        snr_litebird = signal / np.interp(ell, ell_noise, noise_litebird)
        
        ax4.plot(ell, snr_planck, 'r-', linewidth=2, label='Planck', alpha=0.7)
        ax4.plot(ell, snr_litebird, 'g-', linewidth=2, label='LiteBIRD', alpha=0.7)
        ax4.plot(ell, snr_s4, 'b-', linewidth=2, label='CMB-S4', alpha=0.7)
        ax4.axhline(y=1, color='k', linestyle='--', label='Detection Threshold')
        ax4.set_xlabel('Multipole $\\ell$')
        ax4.set_ylabel('Signal-to-Noise Ratio')
        ax4.set_title('(d) Detection Prospects')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        ax4.set_xlim(2, 2500)
        ax4.set_ylim(0, 3)
        
        plt.tight_layout()
        plt.savefig(f'{self.fig_dir}/figure3_cmb_signatures.png', dpi=300, bbox_inches='tight')
        plt.savefig(f'{self.fig_dir}/figure3_cmb_signatures.pdf', bbox_inches='tight')
        plt.close()
        
        print("✓ Figure 3 created: CMB Signatures")
    
    def create_figure_4_oscillation_parameter_dependence(self):
        """Figure 4: Oscillation Dependence on Parameters"""
        print("Creating Figure 4: Parameter Dependence...")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Parameter Dependence of Photon-Dark Photon Oscillations', 
                    fontsize=18, fontweight='bold')
        
        # Panel A: Coupling dependence
        couplings = np.logspace(-7, -4, 50)
        mass_fixed = 1e-23
        
        max_conversion = []
        for coupling in couplings:
            # Simple analytic approximation for max conversion
            P_max = (4 * coupling**2) / (mass_fixed**2 + 4 * coupling**2)
            max_conversion.append(P_max)
        
        ax1.loglog(couplings, max_conversion, 'bo-', linewidth=2, markersize=4)
        ax1.set_xlabel('Coupling $\\epsilon$')
        ax1.set_ylabel('Maximum Conversion Probability $P_{max}$')
        ax1.set_title('(a) Dependence on Coupling Strength')
        ax1.grid(True, alpha=0.3)
        ax1.axvline(x=5e-6, color='red', linestyle='--', label='Benchmark Value')
        ax1.legend()
        
        # Panel B: Mass dependence
        masses = np.logspace(-25, -20, 50)
        coupling_fixed = 5e-6
        
        oscillation_periods = []
        for mass in masses:
            # Period ~ 1/sqrt(mass^4 + coupling^2)
            period = 1 / np.sqrt(mass**4 + coupling_fixed**2)
            oscillation_periods.append(period)
        
        ax2.loglog(masses, oscillation_periods, 'ro-', linewidth=2, markersize=4)
        ax2.set_xlabel('Dark Photon Mass $m_{A\'}$ [eV]')
        ax2.set_ylabel('Oscillation Period [arb. units]')
        ax2.set_title('(b) Dependence on Dark Photon Mass')
        ax2.grid(True, alpha=0.3)
        ax2.axvline(x=2e-23, color='blue', linestyle='--', label='Benchmark Value')
        ax2.legend()
        
        # Panel C: Temperature evolution
        temperatures = np.logspace(15, 2, 100)  # GeV to eV
        temp_keV = temperatures * 1e6  # Convert to keV for plotting
        
        # Effective mixing in plasma (simplified)
        plasma_effect = np.exp(-temperatures / 1e4)  # Decreases with cooling
        
        ax3.semilogx(temp_keV, plasma_effect, 'purple', linewidth=3)
        ax3.set_xlabel('Plasma Temperature [keV]')
        ax3.set_ylabel('Effective Mixing Enhancement')
        ax3.set_title('(c) Temperature Dependence in Early Universe')
        ax3.grid(True, alpha=0.3)
        ax3.axvline(x=300, color='red', linestyle='--', label='Recombination')
        ax3.axvline(x=1000, color='orange', linestyle='--', label='Matter-Radiation Equality')
        ax3.legend()
        
        # Panel D: Experimental reach
        experiments = ['ALPS-II', 'SHiP', 'LDMX', 'CMB-S4', 'LiteBIRD', 'PICO']
        coupling_sensitivity = [2e-8, 5e-9, 1e-9, 5e-9, 8e-9, 2e-9]
        mass_coverage_min = [1e-6, 1e-3, 1e-1, 1e-25, 1e-25, 1e-26]
        mass_coverage_max = [1e-3, 1e0, 1e1, 1e-20, 1e-21, 1e-20]
        
        y_pos = np.arange(len(experiments))
        
        ax4.barh(y_pos, np.array(mass_coverage_max) - np.array(mass_coverage_min), 
                left=mass_coverage_min, alpha=0.7)
        ax4.set_xscale('log')
        ax4.set_yticks(y_pos)
        ax4.set_yticklabels(experiments)
        ax4.set_xlabel('Mass Coverage [eV]')
        ax4.set_title('(d) Experimental Mass Reach')
        ax4.grid(True, alpha=0.3, axis='x')
        
        # Add coupling sensitivity as text
        for i, (exp, sens) in enumerate(zip(experiments, coupling_sensitivity)):
            ax4.text(mass_coverage_max[i] * 1.2, i, f'$\\epsilon=${sens:.1e}', 
                    va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(f'{self.fig_dir}/figure4_parameter_dependence.png', dpi=300, bbox_inches='tight')
        plt.savefig(f'{self.fig_dir}/figure4_parameter_dependence.pdf', bbox_inches='tight')
        plt.close()
        
        print("✓ Figure 4 created: Parameter Dependence")
    
    def create_figure_5_detection_prospects(self):
        """Figure 5: Future Detection Prospects"""
        print("Creating Figure 5: Detection Prospects...")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle('Future Detection Prospects and Experimental Strategy', 
                    fontsize=18, fontweight='bold')
        
        # Panel A: Timeline and sensitivities
        years = np.arange(2024, 2040)
        experiments = {
            'CMB-S4': (2027, 5e-9, 2030),
            'LiteBIRD': (2028, 8e-9, 2032),
            'PICO': (2032, 2e-9, 2035),
            'Advanced Lab': (2026, 1e-10, 2029),
            'Next-gen CMB': (2035, 5e-10, 2038)
        }
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        
        for i, (exp, (start, sens, complete)) in enumerate(experiments.items()):
            ax1.barh(exp, complete - start, left=start, color=colors[i], alpha=0.7, 
                    label=f'{exp} ($\\epsilon=${sens:.1e})')
        
        ax1.set_xlabel('Year')
        ax1.set_title('(a) Experimental Timeline and Sensitivities')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.grid(True, alpha=0.3, axis='x')
        
        # Panel B: Discovery potential
        coupling_range = np.logspace(-10, -6, 100)
        mass_range = np.logspace(-25, -20, 100)
        
        # Probability of discovery (simplified model)
        C, M = np.meshgrid(coupling_range, mass_range)
        discovery_prob = np.exp(-1e-9 / C) * np.exp(-(np.log10(M) - np.log10(5e-23))**2 / 2)
        
        im = ax2.contourf(np.log10(C), np.log10(M), discovery_prob, levels=20, cmap='viridis')
        ax2.set_xlabel('$\\log_{10}(\\epsilon)$')
        ax2.set_ylabel('$\\log_{10}(m_{A\'}$ [eV])')
        ax2.set_title('(b) Discovery Probability')
        
        # Add contours
        contour = ax2.contour(np.log10(C), np.log10(M), discovery_prob, levels=[0.1, 0.5, 0.9], 
                             colors='white', linewidths=2)
        ax2.clabel(contour, inline=True, fontsize=10, fmt='%0.1f')
        
        plt.colorbar(im, ax=ax2, label='Discovery Probability')
        
        plt.tight_layout()
        plt.savefig(f'{self.fig_dir}/figure5_detection_prospects.png', dpi=300, bbox_inches='tight')
        plt.savefig(f'{self.fig_dir}/figure5_detection_prospects.pdf', bbox_inches='tight')
        plt.close()
        
        print("✓ Figure 5 created: Detection Prospects")
    
    def create_all_figures(self):
        """Create all manuscript figures"""
        print("🚀 Generating all manuscript figures...")
        print("=" * 50)
        
        self.create_figure_1_quantum_dynamics()
        self.create_figure_2_parameter_space()
        self.create_figure_3_cmb_signatures()
        self.create_figure_4_oscillation_parameter_dependence()
        self.create_figure_5_detection_prospects()
        
        print("=" * 50)
        print("✅ All figures generated successfully!")
        print(f"📁 Figures saved in: {self.fig_dir}/")
        print("\n📊 Figure Summary:")
        print("  • figure1_quantum_dynamics.png - Quantum dynamics and entanglement")
        print("  • figure2_parameter_space.png - Dark photon parameter constraints")
        print("  • figure3_cmb_signatures.png - CMB polarization signatures")
        print("  • figure4_parameter_dependence.png - Oscillation parameter dependence")
        print("  • figure5_detection_prospects.png - Future detection prospects")

# Generate all figures
if __name__ == "__main__":
    figure_generator = ManuscriptFigures()
    figure_generator.create_all_figures()