import os
import math
import numpy as np
import matplotlib.pyplot as plt

import networkx as nx
import pandas as pd
import os
from .. import path as path
from collections import Counter
import plotly as p
import plotly.graph_objs as go
from plotly.offline import plot
#import realnetwork.path as path
from ..plot_util import get_log_log_points


def calculate_no_of_edges(n, p):
    return p * (n * (n - 1) / 2)


def calculate_average_degree(n, p):
    return p * (n - 1)


def calculate_average_distance(n, p):
    avg_degree = calculate_average_degree(n, p)

    if avg_degree < 1.00:
        return 'N/A'

    return math.log(n) / math.log(avg_degree)


def calculate_clustering_coefficient(p):
    return p


def calculate_degree_prob_distribution(network_name, n, p):
    avg_degree = calculate_average_degree(n, p)
    size = 10000

    if n >= 1000:
        vals = np.random.poisson(avg_degree, size)
    else:
        vals = np.random.binomial(n, p, size)

    file_name = network_name + '_degree_distribution_log_binning.png'
    file_path = os.path.join(path.DB_PLOT_DIR_PATH, file_name)

    x = np.sort(vals)
    unique = np.unique(x)

    # log space start at lowest value in distribution, end at highest, sample of 50
    log_bins = np.logspace(math.log10(min(x)) if min(x) > 0 else math.log10(unique[1]), math.log10(max(x)), 50)
    # Returns count and bins, bins = buckets, set of intervals in histogram
    y, bins, _ = plt.hist(x, bins=log_bins, log=True, density=True)
    # get center of the bin intervals for creating a graph
    bin_centers = list((bins[1:] + bins[:-1]) / 2)
    y = list(y)

    # log10 to every point for each axis
    x_log, y_log = get_log_log_points(bin_centers, y)
    plt.clf()
    plt.scatter(x_log, y_log, s=2, c='r')
    plt.title('Log-Log Degree Distribution with Log Binning')
    plt.xlabel('k')
    plt.ylabel('P(k)')
    plt.savefig(file_path)
    plt.show()
    plt.close()

    return file_name


def get_regime_type(n, p):
    avg_degree = calculate_average_degree(n, p)
    if avg_degree < 1:
        return 'Sub Critical'
    elif avg_degree == 1:
        return 'Critical'
    elif avg_degree > math.log(n):
        return 'Connected'
    elif avg_degree > 1:
        return 'Super Critical'


def plot_closeness(networkx_graph):
       closeness = nx.closeness_centrality(networkx_graph)
       x = list(closeness.keys())
       y = list(closeness.values())
       print(x)
       print(y)

       # p.offline.plot({
       #     "data": [go.Scatter(x=x, y=y)],
       #     "layout": go.Layout(title="closeness")
       # }, auto_open=True,  )

       fig = go.Figure(data=[go.Scatter(x=x, y=y)],
                       layout=go.Layout(
                           title='Closeness',
                           titlefont=dict(size=16),
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20, l=5, r=5, t=40),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

       plot_div = plot(fig, output_type='div', include_plotlyjs=False)
       return plot_div


def plot_degree_centrality(networkx_graph):
    degree_centrality = nx.degree_centrality(networkx_graph)
    x = list(degree_centrality.keys())
    y = list(degree_centrality.values())
    print(x)
    print(y)

    # p.offline.plot({
    #     "data": [go.Scatter(x=x, y=y)],
    #     "layout": go.Layout(title="closeness")
    # }, auto_open=True,  )

    fig = go.Figure(data=[go.Scatter(x=x, y=y)],
                    layout=go.Layout(
                        title='Degree Centrality',
                        titlefont=dict(size=16),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div

def plot_betweeness(networkx_graph):
       closeness = nx.betweenness_centrality(networkx_graph)
       x = list(closeness.keys())
       y = list(closeness.values())

       # plt.clf()
       # plt.scatter(x=x, y=y, s=2, c='r')
       # plt.title('Log-Log Degree Correlations')
       # plt.xlabel('k')
       # plt.ylabel('knn(k)')
       # plt.show()

       # print(x)
       # print(y)

       # p.offline.plot({
       #     "data": [go.Scatter(x=x, y=y)],
       #     "layout": go.Layout(title="betweeness")
       # }, auto_open=True,  )

       fig = go.Figure(data=[go.Scatter(x=x, y=y)],
                       layout=go.Layout(
                           title='Betweeness',
                           titlefont=dict(size=16),
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20, l=5, r=5, t=40),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

       plot_div = plot(fig, output_type='div', include_plotlyjs=False)
       return plot_div


