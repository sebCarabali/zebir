import json
import numpy as np
from io import StringIO

def to_json(npdescriptor):
    return json.dumps(npdescriptor.tolist())


def from_json(jsondescriptor):
    return np.array(json.loads(jsondescriptor), dtype=np.uint8)
