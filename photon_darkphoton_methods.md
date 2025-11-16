# Expanded Methods, LaTeX PRD Version, Pipeline Diagram (ASCII), and Technical Appendix

## 1. Expanded Long-Form Methods

### 1.1 Observational Datasets
This study synthesizes calibrated optical–IR, radio-polarimetric, and in-situ field measurements from three platforms: JWST, ESA JUICE, and SKA-Low. JWST NIRCam and MIRI Level-3 mosaics were retrieved from the Mikulski Archive for Space Telescopes (MAST). All images were reprojected to a unified astrometric grid using JWST-Merge with Gaia DR3 as the reference. JUICE provided electric-field, dust-impact, and photometric telemetry from its 0.41 AU pass. SKA-Low data supplied full-Stokes dynamic spectra.

### 1.2 Preprocessing and Standardization
Each dataset underwent calibration appropriate to its instrument pipeline. JWST frames were background-subtracted, flat-fielded, and corrected for detector artifacts. JUICE field sensors were cleaned of spacecraft-induced interference. SKA-Low visibilities were calibrated against standard flux calibrators.

### 1.3 Binary Event Mapping
To map continuous observational streams to two-channel "+1/-1" outcomes, data were normalized to zero mean and unit variance. An adaptive threshold, based on the median absolute deviation, was applied so that high- and low-flux/polarization deviations yielded +1 or -1. This binary mapping was uniformly applied to real and simulated data.

### 1.4 Entanglement Signal Model
We modeled photon–dark-photon entanglement as a mixture of correlated and uncorrelated binary event pairs. The entangled subset exhibits perfect anticorrelation. The background subset is drawn independently from uniform random binary distributions. The proportion of entangled events is parameterized by \( f_{\mathrm{ent}} \).

### 1.5 Detection Statistic
For each dataset, the Pearson correlation coefficient between the two binary channels was computed. It was transformed using a Fisher z-transform to yield a detection statistic whose significance level is approximately Gaussian for large \(N\). A detection threshold of \( z > 3 \) indicates a false-positive rate of approximately 0.13%.

### 1.6 Injection–Recovery Simulations
Synthetic datasets with entanglement fractions ranging from 0 to 0.5 were generated to assess detection sensitivity. For each fraction, 200 realizations were processed through the full event-mapping and detection pipeline. The recovery probability (fraction of realizations exceeding \( z > 3 \)) characterizes the detection efficiency.

### 1.7 Multi-Instrument Synthesis
Datasets were temporally aligned using barycentric corrections. Overlapping intervals were analyzed independent of instrument, and Fisher-weighted z-score meta-analysis was applied to produce a consolidated detection measurement.

---

## 2. LaTeX PRD Version of Methods
```latex
\section{Methods}

\subsection{Observational Data}
We combine calibrated datasets from JWST (NIRCam and MIRI), ESA JUICE, and SKA-Low to search for correlations consistent with photon--dark-photon entanglement. JWST Level-3 mosaics were retrieved from MAST and reprojected using the JWST-Merge tool. JUICE provided photometric and electric-field measurements from its 0.41 AU pass. SKA-Low dynamic spectra were reduced to Stokes I, Q, U, and V using standard calibration.

\subsection{Binary Event Construction}
All observational streams were normalized to zero mean and unit variance. Binary outcomes $\{+1,-1\}$ were assigned using an adaptive median-absolute-deviation threshold. This procedure was identically applied to empirical and simulated data.

\subsection{Signal Model}
We model the photon--dark-photon system as a mixture distribution comprising an entangled component (perfect anticorrelation between channels) and an uncorrelated background. The entangled fraction is denoted by $f_{\mathrm{ent}}$.

\subsection{Detection Statistic}
For each dataset we compute the Pearson correlation coefficient $r$ between channels and apply the Fisher transform
\begin{equation}
 z = \tanh^{-1}(r) \sqrt{N-3},
\end{equation}
which approximates a standard normal distribution under the null hypothesis. We adopt a detection threshold of $z>3$.

\subsection{Injection--Recovery}
Synthetic datasets were generated with $f_{\mathrm{ent}}$ ranging from 0 to 0.5. For each value, 200 realizations were processed, yielding the recovery probability $P(z>3)$.

\subsection{Cross-Instrument Synthesis}
Instrument time streams were barycentrically corrected and aligned. Fisher-weighted z-score meta-analysis was applied across JWST, JUICE, and SKA-Low intervals with simultaneous coverage.
```

---

## 3. Pipeline Diagram (ASCII)
```
+-------------------------------------------------------------+
|                  Photon–Dark-Photon Pipeline                |
+-------------------------------------------------------------+
|
|  [Raw Data] ---> [Calibration] ---> [Normalization] --------+
|     |                 |                  |                  |
|     |                 |                  v                  |
|     |                 |           +---------------+          |
|     |                 +---------> | Binary Mapper |          |
|     |                             +-------+-------+          |
|     |                                     |                  |
|     |                                     v                  |
|     |                            +--------------+            |
|     |                            |   Event Pairs |            |
|     |                            +------+-------+            |
|     |                                   |                    |
|     v                                   v                    |
|  [Simulation Engine]   --->   [Injection–Recovery]           |
|                                     |                        |
|                                     v                        |
|                            +------------------+              |
|                            | Detection Stats  |              |
|                            +--------+---------+              |
|                                     |                        |
|                                     v                        |
|                         +------------------------+           |
|                         | Multi-Instrument Merge |           |
|                         +------------+-----------+           |
|                                      |                       |
|                                      v                       |
|                              [Final Significance]            |
+-------------------------------------------------------------+
```

---

## 4. Technical Appendix: Mathematical Model

### A.1 Mixed Entanglement Model
Observational event pairs are modeled as draws from a two-component mixture distribution:
\[
P(A,B) = f_{\mathrm{ent}} P_{\mathrm{ent}}(A,B) + (1 - f_{\mathrm{ent}}) P_{\mathrm{noise}}(A,B).
\]
For binary outcomes \(A,B\in\{+1,-1\}\), the entangled component is defined as perfect anticorrelation:
\[
P_{\mathrm{ent}}(A,B) = \frac{1}{2} \delta_{A,-B}.
\]
Background noise is independent:
\[
P_{\mathrm{noise}}(A,B) = \frac{1}{4}.
\]
The expected correlation is
\[
\mathbb{E}[AB] = - f_{\mathrm{ent}}.
\]

### A.2 Fisher z-Transform
The correlation coefficient \( r \) between channels is converted to a z-score using:
\[
 z = \tanh^{-1}(r) \sqrt{N - 3},
\]
which follows approximately a standard normal distribution.

### A.3 Detection Threshold
We define detection as \( z>3 \), corresponding to a false-positive probability of approximately 0.0013. The detection probability for a given entanglement fraction is
\[
 P_{\mathrm{det}}(f_{\mathrm{ent}}) \approx P\left( Z > 3 - \mu_z(f_{\mathrm{ent}}) \right),
\]
where \( \mu_z \) is the mean z-score under injection.

### A.4 Multi-Instrument Fusion
If \( z_i \) is the Fisher z-score for instrument \( i \) with variance \( \sigma_i^2 \), the combined statistic is
\[
 z_{\mathrm{comb}} = \frac{\sum_i z_i / \sigma_i^2}{\sum_i 1/\sigma_i^2}.
\]
This provides an optimal linear combination under Gaussian assumptions.

