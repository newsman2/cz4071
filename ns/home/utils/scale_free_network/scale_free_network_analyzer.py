from scipy.stats import linregress

import matplotlib.pyplot as plt
import numpy as np
import math

from ..plot_util import log_binning, get_log_log_points, plot_scatter


def calculate_real_degree_exponent(degree_count, plot=False):
    try:
        n, bins = log_binning(degree_count, n_bins=50)
        bin_centers = list((bins[1:] + bins[:-1]) / 2)
        n = list(n)

        x_log, y_log = get_log_log_points(bin_centers, n)
        slope, intercept, _, _, _ = linregress(x_log, y_log)

        if math.isnan(slope):
            return None

        xl = [math.log10(i) for i in range(1, 10000)]
        yl = [slope * math.log10(i) + intercept for i in range(1, 10000)]

        if plot:
            plt.plot(xl, yl, 'b')
            plot_scatter(
                bin_centers,
                n,
                title='Log-Log Degree Distribution with Log Binning',
                x_label='k',
                y_label='P(k)',
                log_log=True
            )

        return -slope

    except ValueError:
        return None


def calculate_expected_max_degree(n, min_degree, degree_exponent):
    if degree_exponent is None:
        return None

    return min_degree * math.pow(n, 1 / (degree_exponent - 1))


def calculate_expected_average_distance(no_of_nodes, degree_exponent):
    if degree_exponent is None or degree_exponent < 2:
        return None
    elif degree_exponent == 2:
        return 'It\'s a constant'
    elif 2 < degree_exponent < 3:
        return math.log(math.log(no_of_nodes)) / math.log(degree_exponent - 1)
    elif degree_exponent == 3:
        return math.log(no_of_nodes) / math.log(math.log(no_of_nodes))
    else:
        return math.log(no_of_nodes)


def calculate_expected_degree_exponent(no_of_nodes, kmax, kmin):
    try:
        return (math.log(no_of_nodes) / math.log(kmax / kmin)) + 1

    except ZeroDivisionError:
        return None



