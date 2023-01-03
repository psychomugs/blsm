# from src import gadgets
# import src.gadgets
from src import gadgets as gadget_shelf
from src.utils import loaders
# from src.gadgets.server import start_server
from src.gadgets.server import Cable
from multiprocessing import Process
import pickle

class Rig(Cable):
    def __init__(self, hostname='localhost', port=8080, **kwargs):
        Cable.__init__(self, hostname, port, **kwargs)
        self.gadgets = {}
        self.server = None
        self.hostname = hostname
        self.port = port
        self.power = False
    
    def add_gadget(self, gadget_name):
        config = loaders.load_config(gadget_name)
        gadget = getattr(gadget_shelf, config['type'])(config)
        # breakpoint()
        self.gadgets.update({
            gadget_name:gadget
        })
        return gadget
        
    def power_on(self,):
        self.start()
        [g.start() for g in self.gadgets.values()]
        # for gadget in self.gadgets:
            # gadget.start()
            
        self.power = True
            
    def power_off(self,signum,frame,**kwargs):
        self.join()
        [g.join() for g in self.gadgets.values()]
        
        # for gadget in self.gadgets:
        #     gadget.join()
        self.power = False
        
    def add_message(self, tx_gadget, rx_gadget, msg_func):
        tx_namespace, rx_namespace = map(
            lambda gadget : self.gadgets.get(gadget).namespace, 
            [tx_gadget, rx_gadget])
        def func_emit(sid, data):
            # print(msg_func(pickle.loads(data)))
            emit_data = self.gadgets[rx_gadget].message(**msg_func(pickle.loads(data)))
            print('emit_data', emit_data.event, tx_namespace, rx_namespace)
            # breakpoint()
            self.emit(
                event=emit_data.event,
                data=pickle.dumps(emit_data),
                to=None,
                namespace=rx_namespace
            )
            print('emitted')
        # breakpoint()
        self.on(
            msg_func()['event'],
            handler=func_emit,
            namespace=tx_namespace
        )
        breakpoint()
        
    def func_emit(self, sid, data, tx_namespace='/', rx_namespace='/'):
        # print(msg_func(pickle.loads(data)))
        emit_data = self.gadgets[rx_gadget].message(**msg_func(pickle.loads(data)))
        # print('emit_data', emit_data, rx_namespace)
        breakpoint()
        self.emit(
            emit_data.event,
            pickle.dumps(emit_data),
            namespace=rx_namespace
        )
    
        
    # def start_server(self, ):
    #     return Process(
    #         target=start_server,
    #         args=(self.hostname,self.port),
    #     ), hostname, port
        
    # def start_gadget(self, gadget):
    #     return Process(
    #         target=gadget.connect,
    #         args=(self.hostname, self.port)
    #     )
        
    # def power_on(self,):
    #     self.server_process = self.start_server()
    #     self.gadget_processes = {
    #         gadget.name:self.start_gadget(gadget) for gadget in self.gadgets
    #     }
    #     self.power = True

    # def power_off(self):
    #     self.server_process.join()
    #     [p.join() for p in list(self.gadget_processes.values())]
    #     self.power = False        
    
    