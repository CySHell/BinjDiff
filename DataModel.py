"""
This file contains all the data structures used within the plugin.
"""

import binaryninja as bn
import networkx as nx



#############################
#       Data Templates      *
#############################

class BinjFunc:
    def __init__(self):
        pass

BinjBasicBlock: dict = dict()

#############################
#       Globals      *
#############################

g_binj_funcs: nx.Graph = nx.DiGraph()