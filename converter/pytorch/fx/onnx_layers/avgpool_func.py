import re
from loguru import logger
from onnx import helper
import onnx_layers as ops
import numpy as np

from onnx_layers.base_layer import BaseLayer


class AvgPoolFunc(BaseLayer):
    def __init__(self, source_node, module=None, auto_gen=True):
        super(AvgPoolFunc, self).__init__(source_node, module, auto_gen)

    def add_bottom_top(self, in_names=None, out_names=None):
        pass

    def generate_node(self, name=None, params=None, attr_dict=None):
        pad_layer = ops.PadFunc(self._source_node, auto_gen=False)
        pad_layer.add_bottom_top(out_names=[self._source_node.name+"_pad"])

        padding  = self.list_try_get(self._source_node.args, 3, 0)
        if isinstance(padding , tuple):
            if len(padding) == 1:
                pad_h = pad_w = padding[0]
            else:
                pad_h = padding[0]
                pad_w = padding[1]
        else:
            pad_h = pad_w = padding

        function_name = re.findall(r"(?:function|method) ([a-z|_|0-9]+.*?)", str(self._source_node.target))[0]

        if function_name == "avg_pool1d":
            pads = [0, 0, pad_h, 0, 0, pad_h]
        elif function_name == "avg_pool2d":
            pads = [0, 0, pad_h, pad_w, 0, 0, pad_h, pad_w]

        params = [np.array(pads), np.array(0)]
                
        pad_layer.generate_node(self._source_node.name+"_pad", params=params, attr_dict={'mode': 'constant'})

        self.node_post_process(pad_layer)                         

        pooling_layer = ops.PoolingFunc(self._source_node, auto_gen=False)
        pooling_layer.add_bottom_top(in_names=[self._source_node.name+"_pad"])
        pooling_layer.generate_node(self._source_node.name)
        self.node_post_process(pooling_layer)         