# Magnetic Field Analysis

This project analyses magnetic field measurements from a Hall probe and a smartphone magnetometer using Python.

## Overview

The analysis includes:

* Averaging repeated measurements and estimating uncertainty (standard error of the mean)
* Conversion of Hall probe voltage to magnetic field strength
* Baseline correction of smartphone magnetometer data
* Nonlinear model fitting using a magnetic dipole field model
* Estimation of magnetic moment with uncertainties
* Evaluation of model fit using the coefficient of determination (R²)

## Data

The following datasets are used:

* `hall-probe-data.csv`
* `iphone-data.csv`

These should be placed in the `data/` directory.

## Project Structure

```
magnetic-field-analysis/
│
├── data/              # Raw experimental datasets
├── figures/           # Generated plots
├── src/
│   └── analysis.py    # Main analysis script
│
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

## How to Run

1. Install required packages:

```
pip install -r requirements.txt
```

2. Run the script:

```
python src/analysis.py
```

3. Output:

* Magnetic moment estimates printed in the terminal
* A figure saved in `figures/magnetic_field_analysis.png`

## Methods

* Magnetic dipole model:

  B(x) = (μ₀ m) / (2π (a² + x²)^(3/2))

* Nonlinear least-squares fitting using `scipy.optimize.curve_fit`
* Uncertainty estimation from covariance matrices
* Standard error of the mean used for measurement uncertainty
* The dipole model was fitted to Hall probe data for distances x ≥ 0.015 m, excluding near-field measurements where the approximation breaks down

## Results

* Magnetic field strength decreases with distance, consistent with dipole behaviour  
* Magnetic moments were estimated independently from Hall probe and smartphone data  
* Differences between sensors highlight variations in measurement sensitivity and noise  

The fitted magnetic moments are:

* **Hall probe:**  
  m = (4.50 ± 0.01) × 10⁻¹ A m²  
  R² ≈ 0.95  

* **iPhone magnetometer:**  
  m = (3.78 ± 0.01) × 10⁻¹ A m²  
  R² ≈ 0.98  

Both datasets show strong agreement with the dipole model, with high R² values indicating good fit quality.

<img width="1200" height="500" alt="Hall probe and smartphone magnetometer results" src="https://github.com/user-attachments/assets/f13ff99c-1005-423f-9364-4036ac98dd2f" />


## Technologies Used

* Python
* NumPy
* Matplotlib
* SciPy

## Notes

This project was developed as part of a university physics lab and extended with additional data processing and modelling.
