import numpy as np
import math
import matplotlib.pyplot as plt


def log_binning(counter_dict, n_bins=50, plot=False):
    # x = np.sort(counter_dict.values())
    x = sorted(counter_dict)
    x_prime = []

    for i in range(len(x)):
        if x[i] > 0.00:
            x_prime.append(x[i])

    log_bins = np.logspace(math.log10(min(x_prime)), math.log10(max(x)), n_bins)
    n, bins, _ = plt.hist(x_prime, bins=log_bins, log=True, density=True)

    if plot:
        plt.xscale('log')
        plt.yscale('log')
        plt.show()
    else:
        plt.clf()

    return n, bins


def get_log_log_points(x_orig, y_orig):
    x_log = []
    y_log = []

    for i in range(len(x_orig)):
        if y_orig[i] > 0.00:
            x_log.append(math.log10(x_orig[i]))
            y_log.append(math.log10(y_orig[i]))

    return x_log, y_log


def plot_scatter(x, y, s=20*0.1, c='r', title='', x_label='', y_label='', log_log=False):
    if log_log:
        x, y = get_log_log_points(x, y)

    plt.scatter(x, y, s=s, c=c)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
