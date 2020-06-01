#   Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import yaml
from paddlerec.core.reader import Reader
from paddlerec.core.utils import envs
try:
    import cPickle as pickle
except ImportError:
    import pickle
import paddle.fluid.incubate.data_generator as dg


class TrainReader(dg.MultiSlotDataGenerator):
    def __init__(self, config):
        dg.MultiSlotDataGenerator.__init__(self)
        if os.path.isfile(config):
            with open(config, 'r') as rb:
                _config = yaml.load(rb.read(), Loader=yaml.FullLoader)
        else:
            raise ValueError("reader config only support yaml")

    def init(self):
        pass

    def _process_line(self, line):
        features = line.strip('\n').split('\t')
        feat_idx = []
        feat_value = []
        for idx in range(1, 40):
            feat_idx.append(int(features[idx]))
            feat_value.append(1.0)
        label = [int(features[0])]
        return feat_idx, feat_value, label

    def generate_sample(self, line):
        def data_iter():
            feat_idx, feat_value, label = self._process_line(line)

            s = ""
            for i in [('feat_idx', feat_idx), ('feat_value', feat_value),
                      ('label', label)]:
                k = i[0]
                v = i[1]
                for j in v:
                    s += " " + k + ":" + str(j)
            print s.strip()
            yield None

        return data_iter


reader = TrainReader("../config.yaml")
reader.init()
reader.run_from_stdin()