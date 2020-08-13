##############################################################################
##
# This file is part of Pymepix
#
# https://arxiv.org/abs/1905.07999
#
#
# Pymepix is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pymepix is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pymepix.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

"""Base implementation of objects relating to the processing pipeline"""

from pymepix.core.log import ProcessLogger
import multiprocessing
from multiprocessing import Queue
import traceback
from multiprocessing.sharedctypes import Value
import time
import zmq


class BasePipelineObject(multiprocessing.Process, ProcessLogger):
    """Base class for integration in a processing pipeline
    
    Parameters
    ------------
    name: str
        Name used for logging 
    input_queue: :obj:`multiprocessing.Queue`, optional
        Data queue to perform work on (usually) from previous step in processing pipeline
    create_output: bool, optional
        Whether this creates its own output queue to pass data, ignored if  (Default: True)
    num_outputs: int,optional
        Used with create_output, number of output queues to create (Default: 1)
    shared_output: :obj:`multiprocessing.Queue`, optional
        Data queue to pass results into, useful when multiple processes can put data into the same
        queue (such as results from centroiding). Ignored if create_output is True (Default: None)
    propogate_input: bool
        Whether the input data should be propgated further down the chain
    """

    @classmethod
    def hasOutput(cls):
        """Defines whether this class can output results or not,
        e.g. Centroiding can output results but file writing classes do not
        
        Returns
        ---------
        bool
            Whether results are generated
        
        """
        return True

    def __init__(self, name, input_queue=None, create_output=True, num_outputs=1, shared_output=None,
                 propogate_input=True, addr_in=None, addr_out=None):
        ProcessLogger.__init__(self, name)
        multiprocessing.Process.__init__(self)

        self.conn_settings = {'input_queue': input_queue,
                              'output_queue': [],
                              'propgate_input': propogate_input,
                              'shared_output': shared_output,
                              'num_outputs': num_outputs,
                              'create_output': create_output,
                              'addr_in': addr_in,
                              'addr_out': addr_out
                              }
        self._enable = Value('I', 1)

    @property
    def outputQueues(self):
        """Exposes the outputs so they may be connected to the next step
        
        Returns
        ---------
        :obj:`list` of :obj:`multiprocessing.Queue`
            All of the outputs
        
        """
        return self.output_queue

    @property
    def enable(self):
        """Enables processing 
        
        Determines whether the class will perform processing, this has the result of signalling the process to terminate.
        If there are objects ahead of it then they will stop receiving data
        if an input queue is required then it will get from the queue before checking processing
        This is done to prevent the queue from growing when a process behind it is still working
        
        Parameters
        -----------
        value : bool
            Enable value
        

        Returns
        -----------
        bool:
            Whether the process is enabled or not


        """
        return bool(self._enable.value)

    @enable.setter
    def enable(self, value):
        self.debug('Setting enabled flag to {}'.format(value))
        self._enable.value = int(value)

    def pushOutput(self, data_type, data):
        """Pushes results to output queue (if available)
        

        Parameters
        -----------
        data_type : int
            Identifier for data type (see :obj:`MeesageType` for types)
        data : any
            Results from processing (must be picklable)

        """
        # self.debug('Pushing output {} {} to {}'.format(data_type,data,self.output_queue))
        '''
        for x in self.output_queue:
            if x is not None:
                x.put((data_type, data))
        '''
        #self.zmq_socket.send(data)
        self.debug('pushing')
        self.zmq_socket.send(b'3')

    def process(self, data_type=None, data=None):
        """Main processing function, override this do perform work

        To perform work within the pipeline, a class must override this function.
        General guidelines include, check for correct data type, and must return
        None for both if no output is given.
        """
        self.debug('I AM PROCESSING')
        time.sleep(0.1)
        return None, None

    def pre_run(self):
        """Function called before main processing loop, override to """
        pass

    def init_connection(self):
        """Establish ZMQ connections for processing stages"""
        '''
        if self.conn_settings['shared_output'] is not None:
            self.debug('Queue is shared')
            if type(self.conn_settings['shared_output']) is list:
                self.debug('Queue {} is a list', )
                self.output_queue.extend(self.conn_settings['shared_output'])
            else:
                #self.output_queue.append(shared_output)
                self.debug('####################### ZMQ')
                self.ctx = zmq.Context.instance()
                self.zmq_socket = self.ctx.socket(zmq.PUSH)
                self.zmq_socket.bind(self.conn_settings['addr_out'])
        elif self.conn_settings['create_output']:
            self.debug('Creating Queue')
            for x in range(self.conn_settings['num_outputs']):
                self.output_queue.append(Queue())
        '''
        if self.conn_settings['addr_in'] is not None:
            self.ctx = zmq.Context.instance()
            self.zmq_socket = self.ctx.socket(zmq.PULL)
            self.zmq_socket.bind(self.conn_settings['addr_in'])
        if self.conn_settings['addr_out'] is not None:
            self.ctx = zmq.Context.instance()
            self.zmq_socket = self.ctx.socket(zmq.PUSH)
            self.zmq_socket.bind(self.conn_settings['addr_out'])




    def post_run(self):
        """Function called after main processing loop, override to """
        return None, None

    def run(self):
        self.init_connection()
        self.pre_run()
        while True:
            enabled = self.enable
            try:
                if self.conn_settings['input_queue'] is not None:
                    self.debug('Getting value from input queue')
                    value = self.input_queue.get()

                    if value is None:
                        self.debug('Value is None')
                        # Put it back in the queue and leave
                        self.input_queue.put(None)
                        break
                    data_type, data = value

                    if enabled:
                        output_type, result = self.process(data_type, data)
                        if self._propgate_input:
                            self.pushOutput(*value)
                else:
                    if enabled:
                        output_type, result = self.process()
                    else:
                        self.debug('I AM LEAVING')
                        break
                if output_type is not None and result is not None and enabled:
                    self.zmq_socket.send_pyobj((output_type, result))
                    #self.pushOutput(output_type, result)
            except Exception as e:
                self.error('Exception occured!!!')
                self.error(e, exc_info=True)
                break
        # TODO: test this post_run again!
        '''
        output_type, result = self.post_run()
        if output_type is not None and result is not None: # not quite sure what happens without "enabled"
            self.pushOutput(output_type, result)
        '''
        self.info('Job complete')


def main():
    import logging
    import time
    # Create the logger
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    proc = BasePipelineObject('Base')
    proc.start()
    time.sleep(2.0)

    proc.enable = False
    logging.info('DISABLED')
    time.sleep(2.0)
    proc.terminate()
    proc.join()


if __name__ == "__main__":
    main()
