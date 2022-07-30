from loguru import logger
from onnx import helper

from onnx_layers.base_layer import BaseLayer


class MulFunc(BaseLayer):
    def __init__(self, source_node, module=None, auto_gen=True):
        super(MulFunc, self).__init__(source_node, module, auto_gen)

    def generate_node(self, name=None, params=None, attr_dict=None):

        node = helper.make_node(
            "Mul", self._in_names, self._out_names, self._name
        )

        logger.info("mul_layer: " + self._name + " created")
        self._node.append(node)
