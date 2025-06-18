import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm

# Adjusted data: positive for donor to acceptor, negative for acceptor to donor
percentages = np.array([
    0,                      # Basal
    10, 15, 20, 25, 30,  # Donor to acceptor
    -10, -15, -20, -25, -30,           # Acceptor to donor
    1, 3, 5,                # Donor to acceptor (low %)
    -1, -3, -5              # Acceptor to donor (low %)
])

energies = np.array([
    -1716540.6,             # Basal
    -1715420.5, -1716237.43, -1716257.25, -1714771.67, -1715220.3199999998,
    -1715551.7999999998, -1713039.15, -1713652.61, -1715179.14, -1716039.42,
    -1716566.6, -1715479.2, -1715993.1,
    -1714323.6, -1714895.7999999998, -1714700.0
])

energies_error_1 = np.array([
    1180.0,
    971.0, 608.0, 630.0, 781.0, 777.0,
    656.0, 497.0, 447.0, 942.0, 755.0,
    424.0, 740.0, 656.0,
    637.0, 641.0, 619.0
])
energies_error_2 = np.array([
    3563.906,
    2922.737, 2732.9840, 2460.215, 2789.252, 2669.227,
    2554.312, 2468.415, 2257.252, 2963.457, 3071.706,
    2230.429, 2675.148, 2550.25,
    2544.659, 2344.282, 2509.883
])
energies_error_to_use = energies_error_1
energies -= np.mean(energies)

# Fit a linear regression line
coefficients = np.polyfit(percentages, energies, 1)
linear_fit = np.poly1d(coefficients)
fit_line = linear_fit(percentages)

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

# Show the plot
plt.savefig("0 PS 0 Cholesterol.png")
