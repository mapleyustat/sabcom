import pandas as pd
import networkx as nx
import json
import os

from src.environment import EnvironmentNetwork
from src.runner import Runner


data_folder = 'measurement/baseline/'

# load parameters
with open('parameters.json') as json_file:
    parameters = json.load(json_file)

# load neighbourhood data
with open('neighbourhood_data.json') as json_file:
    neighbourhood_data = json.load(json_file)

# load age data
age_distribution = pd.read_csv('age_dist.csv', sep=';', index_col=0)
age_distribution_per_ward = dict(age_distribution.transpose())

# Monte Carlo simulation
for seed in range(parameters['monte_carlo_runs']):
    # make new folder for seed, if it does not exist
    if not os.path.exists('{}seed{}'.format(data_folder, seed)):
        os.makedirs('{}seed{}'.format(data_folder, seed))

    # initialization
    environment = EnvironmentNetwork(seed, parameters, neighbourhood_data, age_distribution_per_ward)

    # running the simulation
    runner = Runner()
    runner.baseline(environment, seed, data_folder=data_folder)

    # save network
    if not parameters["high_performance"]:
        for idx, network in enumerate(environment.infection_states):
            for i, node in enumerate(network.nodes):
                network.nodes[i]['agent'] = network.nodes[i]['agent'].status

            idx_string = '{0:04}'.format(idx)
            nx.write_graphml_lxml(network, "{}seed{}/network_time{}.graphml".format(data_folder, seed, idx_string))
