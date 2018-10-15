import json
import pickle
import numpy as np
import networkx as nx

from collections import defaultdict
from itertools import product
from epidemic.epidemic import SI
from imports.importcompsci import faculty_graph, school_metadata

selected_universities = ["MIT", "University of Colorado, Boulder", "New Mexico State University"]

# Add new runs of our SI epidemic simulation to our existing cache
def run_trials(si_trials=2, save_timeline=False):
    ps = np.linspace(0, 1, 11)
    rs = np.linspace(0, 1, 5, endpoint=False)
    timeline = []; 

    # If starting from an empty cache:
    results = {"size": {}, "length": {}}
    for p in ps:
        results["size"][p] = defaultdict(list)
        results["length"][p] = defaultdict(list)
    # results = pickle.load(open("cache/CS_SI.p", "rb"))
    for trial in xrange(si_trials):
        print("Trial progress: {}".format(trial / float(si_trials)))
        for p in ps:
            print("Transmission probability: {0}".format(p))
            for node in school_metadata.keys():
                epi = SI(faculty_graph.copy(), p=p)
                epi.infect_node(node)
                epi.simulate()
                results["size"][p][node].append(epi.size)
                results["length"][p][node].append(epi.length)
                
                if school_metadata[node]["institution"] in selected_universities:
                    timeline.append({"p": p, 
                                     "source_inst": school_metadata[node]["institution"],
                                     "path": [{"target": school_metadata[target]["institution"], 
                                               "timestep": time} for (target, time) in epi.timeline]
                                     })

    if save_timeline:
        with open("cache/CS_SI_timeline.json", "w") as outfile:
            json.dump(timeline, outfile, indent=4)

    # pickle.dump(results, open("cache/CS_SI.p", 'wb'))
    results.clear()
    print("SI done")

# Add new runs of our SI epidemic with random hops to our existing cache
def run_trials_graph_with_random_hops(si_trials=2):
    pjumps = np.linspace(0, 1, 11)

    # If starting from an empty cache:
    results = {"size": {}, "length": {}}
    for p in pjumps:
        results["size"][p] = defaultdict(list)
        results["length"][p] = defaultdict(list)
    # results = pickle.load(open("cache/random_jump/CS_SI.p", "rb"))
    for trial in xrange(si_trials):
        print("Trial progress: {}".format(trial / float(si_trials)))
        for p in pjumps:
            print("Jump probability: {0}".format(p))
            for node in school_metadata.keys():
                epi = SI(faculty_graph.copy(), p=0.1, random_jump_p=p, is_random_jump=True)
                epi.infect_node(node)
                epi.simulate()
                results["size"][p][node].append(epi.size)
                results["length"][p][node].append(epi.length)
    # pickle.dump(results, open("cache/random_jump/CS_SI.p", 'wb'))
    results.clear()
    print("SI + RANDOM HOP done")


if __name__ == "__main__":
    run_trials(si_trials=1, save_timeline=True)
    # run_trials_graph_with_random_hops(si_trials=1)
