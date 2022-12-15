import binaryninja as bn


class FuncFeatures:
    def __init__(self, func: bn.highlevelil.HighLevelILFunction):
        self.func = func
        self.base_of_image: int = func.source_function.view.start
        self.func_offset: int = self.func.source_function.start - self.base_of_image
        self.func_name: str = self.GetName()
        self.callers: list = self.GetCallers()
        self.callees: list = self.GetCallees()


    def ToDict(self) -> dict:
        pass

    def GetCallers(self) -> list:
        return [caller_addr.start - self.base_of_image for caller_addr in self.func.source_function.callers]

    def GetCallees(self) -> list:
        return [callee_addr.start - self.base_of_image for callee_addr in self.func.source_function.callees]

    def GetName(self) -> str:
        return self.func.source_function.name


class BBlockFeatures:
    def __init__(self, bb: bn.highlevelil.HighLevelILBlock):
        self.bb = bb

    def GetNames(self):
        pass

    def GetStrings(self):
        pass
