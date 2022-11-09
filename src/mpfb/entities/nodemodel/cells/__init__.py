import bpy
from inspect import signature
from mpfb.services.logservice import LogService
from mpfb.entities.nodemodel.molecules import MoleculeNodeManager

from .bodysectionsrouter import MpfbBodySectionsRouter

_LOG = LogService.get_logger("nodemodel.cells")
_LOG.trace("initializing nodemodel cells module")

class CellNodeManager(MoleculeNodeManager):
    def __init__(self, node_tree):
        _LOG.trace("Constructing CellNodeManager with node_tree", node_tree)
        MoleculeNodeManager.__init__(self, node_tree)

        self._cell_singletons = dict()
        self._cell_singletons["MpfbBodySectionsRouter"] = MpfbBodySectionsRouter()

    def createMpfbBodySectionsRouter(self, x=0.0, y=0.0, name=None, label=None, DefaultBodyShader=None, AureolaeShader=None, FaceShader=None, LipsShader=None, FingernailsShader=None, ToenailsShader=None):
        return self._cell_singletons["MpfbBodySectionsRouter"].create_instance(self.node_tree, x=x, y=y, name=name, label=label, DefaultBodyShader=DefaultBodyShader, AureolaeShader=AureolaeShader, FaceShader=FaceShader, LipsShader=LipsShader, FingernailsShader=FingernailsShader, ToenailsShader=ToenailsShader)