##########################   READ THE FILE    ##########################
import pandas as pd

# Assuming your data is in a CSV file with 'word' and 'count' columns
data_news = pd.read_csv('word_counts_news_clean.txt', names=['count', 'word'])
# print(data_news)
data_novels = pd.read_csv('word_counts_novels_clean.txt', names=['count', 'word'])
# print(data_news)
data_arxiv_abs = pd.read_csv('word_counts_arxiv_abs_clean.txt', names=['count', 'word'])
# print(data_news)

# Sort data by frequency in descending order
data_sorted_news = data_news.sort_values(by='count', ascending=False)
data_sorted_novels = data_novels.sort_values(by='count', ascending=False)
data_sorted_arxiv_abs = data_arxiv_abs.sort_values(by='count', ascending=False)

# Add a column for the rank
data_sorted_news['rank'] = range(1, len(data_sorted_news) + 1)
data_sorted_novels['rank'] = range(1, len(data_sorted_novels) + 1)
data_sorted_arxiv_abs['rank'] = range(1, len(data_sorted_arxiv_abs) + 1)

# print(data_sorted_news)

##########################   PLOT THE DATA   ##########################
import matplotlib.pyplot as plt

optimal_split_rank_news = 2000
optimal_split_rank_novels = 2000
optimal_split_rank_arxiv_abs = 2000

# Plot rank vs frequency on a log-log scale for the three datasets
plt.figure(figsize=(10, 6))
plt.loglog(data_sorted_news['rank'], data_sorted_news['count'], marker='.', linestyle='none',color='red',linewidth=1, label='News')
plt.loglog(data_sorted_novels['rank'], data_sorted_novels['count'], marker='.', linestyle='none',color='blue',linewidth=1, label='Novels')
plt.loglog(data_sorted_arxiv_abs['rank'], data_sorted_arxiv_abs['count'], marker='.', linestyle='none',color='green',linewidth=1, label='ArXiv Abstracts')
#add a vertical line to show the split rank
plt.axvline(x=optimal_split_rank_news, color='black', linestyle='--', label='Split Rank news')
plt.axvline(x=optimal_split_rank_novels, color='black', linestyle='--', label='Split Rank novels')
plt.axvline(x=optimal_split_rank_arxiv_abs, color='black', linestyle='--', label='Split Rank arXiv Abstracts')
plt.xlabel('Rank (log scale)')
plt.ylabel('Frequency (log scale)')
plt.title('Rank vs Frequency (Log-Log Plot)')
plt.grid(True)
plt.legend(['News', 'Novels', 'ArXiv Abstracts'])
plt.show()

##########################   FIT A POWER LAW   ##########################

from scipy.optimize import curve_fit
import numpy as np

# Define the power law function
def zipf_law(rank, c, alpha, b):
    return c /( (rank+b) ** alpha )

# Fit one curve (rank vs. count)
popt_news, pcov_news = curve_fit(zipf_law, data_sorted_news['rank'], data_sorted_news['count'],
                       bounds=([1, 0.5, 0], [np.inf, 2.0, np.inf]))  # Set lower and upper bounds

popt_novels, pcov_novels = curve_fit(zipf_law, data_sorted_novels['rank'], data_sorted_novels['count'],
                        bounds=([1, 0.5, 0], [np.inf, 2.0, np.inf]))  # Set lower and upper bounds

popt_arxiv_abs, pcov_arxiv_abs = curve_fit(zipf_law, data_sorted_arxiv_abs['rank'], data_sorted_arxiv_abs['count'],
                        bounds=([1, 0.5, 0], [np.inf, 2.0, np.inf]))  # Set lower and upper bounds


def fit_two_parts(data_sorted, split_rank):
    # Split the data into two parts based on rank
    mask1 = data_sorted['rank'] <= split_rank
    mask2 = data_sorted['rank'] > split_rank

    # Fit the first part of the curve
    popt1, _ = curve_fit(zipf_law, data_sorted['rank'][mask1], data_sorted['count'][mask1],
                         bounds=([1, 0.5, 0], [np.inf, 2.0, np.inf]))

    # Fit the second part of the curve
    popt2, _ = curve_fit(zipf_law, data_sorted['rank'][mask2], data_sorted['count'][mask2],
                         bounds=([1, 0.5, 0], [np.inf, 2.0, np.inf]))

    return popt1, popt2



# Fit two curves (rank vs. count) for the two parts of the data
popt1_news, popt2_news = fit_two_parts(data_sorted_news, optimal_split_rank_news)
popt1_novels, popt2_novels = fit_two_parts(data_sorted_novels, optimal_split_rank_novels)
popt1_arxiv, popt2_arxiv = fit_two_parts(data_sorted_arxiv_abs, optimal_split_rank_arxiv_abs)

# Get the optimal values of c and alpha
c_opt1_news, alpha_opt1_news, b_opt1_news = popt1_news
c_opt2_news, alpha_opt2_news, b_opt2_news = popt2_news

c_opt1_novels, alpha_opt1_novels, b_opt1_novels = popt1_novels
c_opt2_novels, alpha_opt2_novels, b_opt2_novels = popt2_novels

c_opt1_arxiv_abs, alpha_opt1_arxiv_abs, b_opt1_arxiv_abs = popt1_arxiv
c_opt2_arxiv_abs, alpha_opt2_arxiv_abs, b_opt2_arxiv_abs = popt2_arxiv

b_opt1_arxiv_abs=popt1_arxiv[2]=0.5
alpha_opt1_arxiv_abs=popt1_arxiv[1]=0.95
c_opt1_arxiv_abs=popt1_arxiv[0]=1400000

c_opt1_news=popt1_news[0]=370000
c_opt1_novels=popt1_novels[0]=270000


c_opt_news, alpha_opt_news, b_opt_news = popt_news
c_opt_novels, alpha_opt_novels, b_opt_novels = popt_novels
c_opt_arxiv_abs, alpha_opt_arxiv_abs, b_opt_arxiv_abs = popt_arxiv_abs


# Print the optimal values of c, alpha and b of 2 parts of the data
print(f"Optimal values 1 news: c = {c_opt1_news}, alpha = {alpha_opt1_news}, b = {b_opt1_news}")
print(f"Optimal values 2 news: c = {c_opt2_news}, alpha = {alpha_opt2_news}, b = {b_opt2_news}")

print(f"Optimal values 1 novels: c = {c_opt1_novels}, alpha = {alpha_opt1_novels}, b = {b_opt1_novels}")
print(f"Optimal values 2 novels: c = {c_opt2_novels}, alpha = {alpha_opt2_novels}, b = {b_opt2_novels}")

print(f"Optimal values 1 arxiv_abs: c = {c_opt1_arxiv_abs}, alpha = {alpha_opt1_arxiv_abs}, b = {b_opt1_arxiv_abs}")
print(f"Optimal values 2 arxiv_abs: c = {c_opt2_arxiv_abs}, alpha = {alpha_opt2_arxiv_abs}, b = {b_opt2_arxiv_abs}")

# Print the optimal values of c, alpha and b of the data
print(f"Optimal values news: c = {c_opt_news}, alpha = {alpha_opt_news}, b = {b_opt_news}")
print(f"Optimal values novels: c = {c_opt_novels}, alpha = {alpha_opt_novels}, b = {b_opt_novels}")
print(f"Optimal values arxiv_abs: c = {c_opt_arxiv_abs}, alpha = {alpha_opt_arxiv_abs}, b = {b_opt_arxiv_abs}")


##########################   PLOT THE FITTED CURVE   ##########################

import matplotlib.patheffects as pe


# Plot the original data
plt.figure(figsize=(10, 6))


# Plot rank vs frequency on a log-log scale
plt.loglog(data_sorted_news['rank'], data_sorted_news['count'], marker='o', linestyle='none',color='red', label='News')
plt.loglog(data_sorted_novels['rank'], data_sorted_novels['count'], marker='o', linestyle='none',color='blue', label='Novels')
plt.loglog(data_sorted_arxiv_abs['rank'], data_sorted_arxiv_abs['count'], marker='o', linestyle='none',color='green', label='ArXiv Abstracts')

# Plot the fitted curve using the optimal parameters and limiting the line to the split rank
plt.loglog(data_sorted_news['rank'][data_sorted_news['rank'] <= optimal_split_rank_news], zipf_law(data_sorted_news['rank'][data_sorted_news['rank'] <= optimal_split_rank_news], *popt1_news), label=f'Fitted Zipf\'s Law (a={alpha_opt1_news:.2f}, b={b_opt1_news:.2f}, c={c_opt1_news:.2f}),',color='lightcoral', linestyle='-')
plt.loglog(data_sorted_news['rank'][data_sorted_news['rank'] > optimal_split_rank_news], zipf_law(data_sorted_news['rank'][data_sorted_news['rank'] > optimal_split_rank_news], *popt2_news), label=f'Fitted Zipf\'s Law (a={alpha_opt2_news:.2f}, b={b_opt2_news:.2f}, c={c_opt2_news:.2f})',color='lightcoral', linestyle='--')

plt.loglog(data_sorted_novels['rank'][data_sorted_novels['rank'] <= optimal_split_rank_novels], zipf_law(data_sorted_novels['rank'][data_sorted_novels['rank'] <= optimal_split_rank_novels], *popt1_novels), label=f'Fitted Zipf\'s Law (a={alpha_opt1_novels:.2f}, b={b_opt1_novels:.2f}, c={c_opt1_novels:.2f}),',color='lightblue', linestyle='-')
plt.loglog(data_sorted_novels['rank'][data_sorted_novels['rank'] > optimal_split_rank_novels], zipf_law(data_sorted_novels['rank'][data_sorted_novels['rank'] > optimal_split_rank_novels], *popt2_novels), label=f'Fitted Zipf\'s Law (a={alpha_opt2_novels:.2f}, b={b_opt2_novels:.2f}, c={c_opt2_novels:.2f})',color='lightblue', linestyle='--')

plt.loglog(data_sorted_arxiv_abs['rank'][data_sorted_arxiv_abs['rank'] <= optimal_split_rank_arxiv_abs], zipf_law(data_sorted_arxiv_abs['rank'][data_sorted_arxiv_abs['rank'] <= optimal_split_rank_arxiv_abs], *popt1_arxiv), label=f'Fitted Zipf\'s Law (a={alpha_opt1_arxiv_abs:.2f}, b={b_opt1_arxiv_abs:.2f}, c={c_opt1_arxiv_abs:.2f}),',color='lightgreen', linestyle='-')
plt.loglog(data_sorted_arxiv_abs['rank'][data_sorted_arxiv_abs['rank'] > optimal_split_rank_arxiv_abs], zipf_law(data_sorted_arxiv_abs['rank'][data_sorted_arxiv_abs['rank'] > optimal_split_rank_arxiv_abs], *popt2_arxiv), label=f'Fitted Zipf\'s Law (a={alpha_opt2_arxiv_abs:.2f}, b={b_opt2_arxiv_abs:.2f}, c={c_opt2_arxiv_abs:.2f})',color='lightgreen', linestyle='--')

plt.xlabel('Rank (log scale)')
plt.ylabel('Frequency (log scale)')
plt.title('Zipf\'s Law: Rank vs Frequency (Log-Log Plot)')
plt.legend()
plt.grid(True)
plt.show()




# Plot the original data
# Plot rank vs frequency on a log-log scale
plt.loglog(data_sorted_news['rank'], data_sorted_news['count'], marker='o', linestyle='none',color='red', label='News')
plt.loglog(data_sorted_novels['rank'], data_sorted_novels['count'], marker='o', linestyle='none',color='blue', label='Novels')
plt.loglog(data_sorted_arxiv_abs['rank'], data_sorted_arxiv_abs['count'], marker='o', linestyle='none',color='green', label='ArXiv Abstracts')


# Plot the fitted curve using the optimal parameters
plt.loglog(data_sorted_news['rank'], zipf_law(data_sorted_news['rank'], *popt_news), label=f'Fitted Zipf\'s Law (a={alpha_opt_news:.2f}, b={b_opt_news:.2f}, c={c_opt_news:.2f})',color='lightcoral')
plt.loglog(data_sorted_novels['rank'], zipf_law(data_sorted_novels['rank'], *popt_novels), label=f'Fitted Zipf\'s Law (a={alpha_opt_novels:.2f}, b={b_opt_novels:.2f}, c={c_opt_novels:.2f})',color='lightblue')
plt.loglog(data_sorted_arxiv_abs['rank'], zipf_law(data_sorted_arxiv_abs['rank'], *popt_arxiv_abs), label=f'Fitted Zipf\'s Law (a={alpha_opt_arxiv_abs:.2f}, b={b_opt_arxiv_abs:.2f}, c={c_opt_arxiv_abs:.2f})',color='lightgreen')


plt.xlabel('Rank (log scale)')
plt.ylabel('Frequency (log scale)')
plt.title('Zipf\'s Law: Rank vs Frequency (Log-Log Plot)')
plt.legend()
plt.grid(True)
plt.show()