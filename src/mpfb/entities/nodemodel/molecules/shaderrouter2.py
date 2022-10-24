from mpfb.services.logservice import LogService
from .molecule import Molecule

import bpy

_LOG = LogService.get_logger("nodemodel.shaderrouter2")
_GROUP_NAME = "MpfbShaderRouter2"

class MpfbShaderRouter2(Molecule):
    def __init__(self):
        _LOG.trace("Constructing Molecule for", _GROUP_NAME)
        Molecule.__init__(self, _GROUP_NAME)

    def create_group(self):
        _LOG.debug("Create group in " + _GROUP_NAME)

        nodes = dict()

        (nodes["Group Input"], nodes["Group Output"]) = self.create_input_and_output()
        nodes["Group Output"].location = [345.2333679199219, -122.97506713867188]
        nodes["Group Input"].location = [-383.4490661621094, -122.97506713867188]

        self.add_input_socket("Value", socket_type="NodeSocketFloat", default_value=0.5)
        self.add_input_socket("Threshold", socket_type="NodeSocketFloat", default_value=0.5)
        self.add_input_socket("Section1Shader", socket_type="NodeSocketShader")
        self.add_input_socket("Section2Shader", socket_type="NodeSocketShader")

        self.add_output_socket("Shader", socket_type="NodeSocketShader")

        nodes["Mix Shader"] = self.createShaderNodeMixShader(name="Mix Shader", x=131.0485382080078, y=-127.71904754638672, Fac=0.5)
        nodes["Math"] = self.createShaderNodeMath(name="Math", x=-111.90221405029297, y=18.855880737304688, Value=0.5, Value_001=0.5, Value_002=0.5, operation='GREATER_THAN', use_clamp=False)

        self.add_link(nodes["Group Input"], "Value", nodes["Math"], "Value")
        self.add_link(nodes["Group Input"], "Threshold", nodes["Math"], "Value_001")
        self.add_link(nodes["Group Input"], "Section1Shader", nodes["Mix Shader"], "Shader")
        self.add_link(nodes["Group Input"], "Section2Shader", nodes["Mix Shader"], "Shader_001")
        self.add_link(nodes["Mix Shader"], "Shader", nodes["Group Output"], "Shader")
        self.add_link(nodes["Math"], "Value", nodes["Mix Shader"], "Fac")
