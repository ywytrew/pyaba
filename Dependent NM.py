import numpy as np
from scipy.optimize import basinhopping
import matplotlib.pyplot as plt

# Experimental stress-strain data
strain = np.array([0.005193936,0.027073319,0.076475178, 0.130999613, 0.197089594, 0.278509751, 0.370589691, 0.441752953, 0.473755818])
stress = np.array([59078.31488,220015.7933,454291.8696, 658010.1967, 833579.7908, 1063409.668, 1291388.278, 1470846.322, 1576779.852])

# 2nd-degree polynomial model
def poly_model(parameters, strain):
    C10,C01,C20,C11,C02  = parameters

    lam = 1 +strain
    I1 = lam**2 + 2*lam**(-1)
    I2 = lam ** (-2) + 2 * lam
    stress = 2*(1-lam**(-3))*(C10*lam+C01+2*C20*lam*(I1-3)+C11*(I1-3+lam*(I2-3))+2*C02*(I2-3))
    '''
    I1 = (1 + 2 * strain)**2
    I2 = 1 / (1 - 2 * strain)

    #psi = C10 * (I1 - 3) + C01 * (I2 - 3) + C20 * (I1 - 3)**2 + C11 * (I1 - 3) * (I2 - 3) + C02 * (I2 - 3)**2
    # Calculate stress from strain energy function
    stress = 2 * (C10 + 2 * C20 * (I1 - 3) + C11 * (I2 - 3)) * (1 + 2 * strain)
    '''
    return stress

# Objective function to minimize
def error_function(parameters):
    stress_model = poly_model(parameters, strain)
    error = np.sum((stress - stress_model)**2)
    return error

# Initial guess for material parameters
initial_parameters = np.array([1, 1, 1, 1, 1])

# Simulated Annealing optimization
minimizer_kwargs = {"method": "BFGS"}
result = basinhopping(error_function, initial_parameters, minimizer_kwargs=minimizer_kwargs, niter=10)

# Identified material parameters
C10,C01,C20,C11,C02 = result.x
print(f"Identified material parameters: C10 = {C10:.4f}, C01 = {C01:.4f}, C20 = {C20:.4f}, C11 = {C11:.4f},  C02 = {C02:.4f}")

# Plot experimental data and fitted model
plt.scatter(strain, stress, label="Experimental data", color="red")
strain_fine = np.linspace(0, 0.473755818, 100)
stress_fine = poly_model(result.x, strain_fine)
plt.plot(strain_fine, stress_fine, label="Fitted 2nd-degree polynomial", color="blue")
plt.xlabel("Strain")
plt.ylabel("Stress")
plt.legend()
plt.show()
