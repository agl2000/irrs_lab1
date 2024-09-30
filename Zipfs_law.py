#READ THE FILE
import pandas as pd

# Assuming your data is in a CSV file with 'word' and 'count' columns
data = pd.read_csv('word_counts_news_clean.txt', names=['count', 'word'])
print(data)

# Sort data by frequency in descending order
data_sorted = data.sort_values(by='count', ascending=False)

# Add a column for the rank
data_sorted['rank'] = range(1, len(data_sorted) + 1)

print(data_sorted)

# PLOT THE DATA
import matplotlib.pyplot as plt

# Plot rank vs frequency on a log-log scale
plt.figure(figsize=(10, 6))
plt.loglog(data_sorted['rank'], data_sorted['count'], marker='o', linestyle='none')
plt.xlabel('Rank (log scale)')
plt.ylabel('Frequency (log scale)')
plt.title('Rank vs Frequency (Log-Log Plot)')
plt.grid(True)
plt.show()

#FIT A POWER LAW

from scipy.optimize import curve_fit
import numpy as np

# Define the power law function
def zipf_law(rank, c, alpha):
    return c * rank ** (-alpha)

# Fit the curve (rank vs. count)
popt, pcov = curve_fit(zipf_law, data_sorted['rank'], data_sorted['count'])

# Get the optimal values of c and alpha
c_opt, alpha_opt = popt
print(f"Optimal values: c = {c_opt}, alpha = {alpha_opt}")

# Plot the data and the fitted curve
# Plot the original data
plt.figure(figsize=(10, 6))
plt.loglog(data_sorted['rank'], data_sorted['count'], marker='o', linestyle='none', label='Original data')

# Plot the fitted power law
plt.loglog(data_sorted['rank'], zipf_law(data_sorted['rank'], *popt), label=f'Fitted Zipf\'s Law (alpha = {alpha_opt:.2f})')

plt.xlabel('Rank (log scale)')
plt.ylabel('Frequency (log scale)')
plt.title('Zipf\'s Law: Rank vs Frequency (Log-Log Plot)')
plt.legend()
plt.grid(True)
plt.show()
