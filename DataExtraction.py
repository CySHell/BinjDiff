from DataModel import *
from FeatureExtraction.Local import Feature
from typing import *
import networkx as nx

g_all_local_func_features: nx.DiGraph = nx.DiGraph()

def InitBv(bv: bn.binaryview) -> bool:
    # Any init procedures needed on the bv, such as re-basing etc.
    return True


def ExtractBBlockData(func: ):
    bb_list: list = list()
    for bb in self.func.basic_blocks:
        bb_list.append(BBlockFeatures(bb))
    return bb_list

def ExtractFuncData(func: bn.function.Function) -> Feature.FuncFeatures:
    return Feature.FuncFeatures(func.hlil)


def ExtractFuncGlobalData(all_local_func_features: dict) -> dict:
    pass


def IsFuncEligibleForExtraction(func: bn.function.Function) -> bool:
    if func.name.startswith('sub_'):
        return False
    return True

def InsertFuncFeatures(func: bn.Function, func_features: Feature.FuncFeatures) -> bool:
    # The graph recognizes a function as its offset from the base of the image because there might
    # be duplicate function names within an image (such as in constructors with different prototypes).
    g_all_local_func_features.add_node(func_features.func_offset, func_features.ToDict())


def ExtractDataAllFuncs(bv: bn.binaryview) -> Optional[dict]:
    all_func_features = None
    if InitBv(bv):
        for func in bv.functions:
            if IsFuncEligibleForExtraction(func):
                if func_features := ExtractFuncData(func):

                    if InsertFuncFeatures(func, func_features)
        if all_func_features := ExtractFuncGlobalData():
            return all_func_features
    return None
