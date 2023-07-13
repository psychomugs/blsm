from r0b0 import logging
from r0b0.utils.loaders import load_msg
import pickle

# @load_msg
def midi_rel2position(data=None):
    if data is None: return {'event':'midi_cc'}
    msg = pickle.loads(data['msg'])
    
    value_dict = {
        1:1,
        127:-1
    }
    scale_dict = {
        1:800,
        2:800,
        3:800,
        4:300
    }
    value_scale = scale_dict.get(msg.control,300)
    value_dict.setdefault(0)
    logging.debug(data)
    
    return {
        'event':'position',
        'value':value_dict.get(msg.value,0)*value_scale,
        'motor_id':msg.control,
        'absolute':False
    }