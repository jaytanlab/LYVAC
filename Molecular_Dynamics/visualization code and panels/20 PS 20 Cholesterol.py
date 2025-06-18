import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm

# Define the transfer percentages (positive: donor to acceptor, negative: acceptor to donor)
percentages = np.array([
    0,                      # Basal
    5, 10, 15, 20, 25, 30.4,    # Donor to acceptor
    -5, -9.6, -15, -20, -25, -30,  # Acceptor to donor
    1, 3,
    -1, -3
])

# Corresponding total_Ave energy values
energies = np.array([
    -1639750.9700000002,           # Basal
    -1642016.4100000001, -1642057.83, -1643334.02, -1642056.15, -1640822.4700000002, -1642110.95, # donor to acceptor
    -1640834.83, -1640776.6, -1636698.4, -1637325.5899999999, -1637155.74, -1636282.39,
    -1640624.3199999998, -1639597.15,
    -1640150.77, -1638624.45
])

energies_error_1 = np.array([
    844.0,
    858.0, 634.0, 522.0, 627.0, 713.0, 508.0,
    987.0, 892.0, 544.0, 573.0, 528.0, 801.0,
    554.0, 957.0,
    634.0, 615.0
])
energies_error_2 = np.array([
    3111.95,
    3024.036, 2575.709, 2584.115, 2371.67, 2458.519, 2448.5429999999997,
    3222.515, 2944.7619999999997, 2620.107, 2504.505, 2697.82, 2690.561,
    2312.398, 3007.367,
    2895.656, 2508.193
])
energies_error_to_use = energies_error_1
energies -= np.mean(energies)

# Fit linear regression
coefficients = np.polyfit(percentages, energies, 1)
linear_fit = np.poly1d(coefficients)
# Generate x values from -30 to 30 for smooth fit line
x_fit = np.linspace(-32.5, 32.5, 200)
y_fit = linear_fit(x_fit)

# Plotting
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

# Show plot
plt.savefig("20 PS 20 Cholesterol.png")
