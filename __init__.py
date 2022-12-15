import binaryninja as bn


bn.PluginCommand.register("BinjDiff",
                          "Function Signature Matching",
                          StartInspection.inspect,
                          StartInspection.is_bv_valid_for_plugin)