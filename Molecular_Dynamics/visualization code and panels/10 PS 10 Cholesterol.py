import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm

percentages = np.array([
    0,        # Basal
    1, 3, 5, 10, 20, 30, # Donor to acceptor (low %)
    -1, -3, -5, -10, -20, -30 # Acceptor to donor (low %)
])

# Corresponding energy values for 10% PS, 10% cholesterol in acceptor
energies = np.array([
    -1680271.2999999998,  # Basal
    -1680957.8, -1681161.0, -1681308.8, -1680947.1, -1680146.85, -1680986.1099999999, # Donor to acceptor
    -1680490.5, -1680014.12, -1680132.56, -1680019.24, -1679499.35, -1678925.41   # Acceptor to donor
])

energies_error_1 = np.array([
    613.0,
    661.0, 802.0, 852.0, 487.0, 758.0, 410.0, 
    1099.5, 718.0, 569.0, 639.0, 777.0, 648.0
])
energies_error_2 = np.array([
    2680.8239999999996,
    2699.79, 3015.19, 2935.307, 2485.505, 2883.0170000000003, 2270.5016,
    3385.0649999999996, 2688.746, 2504.665, 2741.309, 2918.5969999999998, 2805.473
])
energies_error_to_use = energies_error_1
energies -= np.mean(energies)

# Fit linear regression
coefficients = np.polyfit(percentages, energies, 1)
linear_fit = np.poly1d(coefficients)

# Generate x values from -30 to 30 for smooth fit line
x_fit = np.linspace(-32.5, 32.5, 200)
y_fit = linear_fit(x_fit)

# Create the plot
plt.figure(figsize=(10, 6))
# plt.scatter(percentages, energies, color='blue', label='Energy data')
plt.errorbar(
    percentages,
    energies,
    yerr=energies_error_to_use,
    fmt='o',                   # 'o' for circular markers
    color='blue',
    ecolor='black',            # Error bar color
    elinewidth=3,              # Bold error bar lines
    capsize=5,                 # End caps on error bars
    label='Energy data'
)
plt.plot(x_fit, y_fit, color='red', label='Linear Fit')

# Plot settings
plt.xticks(fontsize=22, fontweight='bold')
plt.yticks(fontsize=22, fontweight='bold')
plt.legend(
    fontsize=22,
    prop=fm.FontProperties(weight='bold', size=22),
    loc='best',
    markerscale=1.5,       # Enlarge the markers in legend
    handlelength=2.5       # Enlarge the line segment in legend
)

plt.xlim(-32.5, 32.5)
plt.ylim(-6000, 6000)
plt.grid(True)

import matplotlib.ticker as ticker
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))


# Calculate R^2
fit_line = linear_fit(percentages)
from sklearn.metrics import r2_score
r_squared = r2_score(energies, fit_line)

# Create annotation string
fit_eq = f"y = {coefficients[0]:.2f}x + {coefficients[1]:.2f}\n$R^2$ = {r_squared:.4f}"

# Add text to the image (bottom right corner)
plt.text(
    0.05, 0.05, fit_eq,
    fontsize=22,
    fontweight='bold',
    ha='left',
    va='bottom',
    transform=plt.gca().transAxes,
    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3')
)

# Save the plot
plt.savefig("10 PS 10 Cholesterol.png")