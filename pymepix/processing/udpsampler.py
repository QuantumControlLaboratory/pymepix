# This file is part of Pymepix
#
# In all scientific work using Pymepix, please reference it as
#
# A. F. Al-Refaie, M. Johny, J. Correa, D. Pennicard, P. Svihra, A. Nomerotski, S. Trippel, and J. Küpper:
# "PymePix: a python library for SPIDR readout of Timepix3", J. Inst. 14, P10003 (2019)
# https://doi.org/10.1088/1748-0221/14/10/P10003
# https://arxiv.org/abs/1905.07999
#
# Pymepix is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. If not,
# see <https://www.gnu.org/licenses/>.
import ctypes
from pathos.helpers import mp as multiprocessing
#from multiprocessing import Queue
Queue = multiprocessing.Queue
from multiprocessing.sharedctypes import Value
import numpy as np
import socket
import time

from .basepipeline import BasePipelineObject
from .datatypes import MessageType
from pymepix.processing.rawtodisk import raw2Disk


class UdpSampler(BasePipelineObject):
    """Recieves udp packets from SPDIR

    This class, creates a UDP socket connection to SPIDR and recivies the UDP packets from Timepix
    It them pre-processes them and sends them off for more processing



    """

    def __init__(self, address, longtime, chunk_size=1000, flush_timeout=0.3, input_queue=None, create_output=True,
                 num_outputs=1, shared_output=None):
        BasePipelineObject.__init__(self, 'UdpSampler', input_queue=input_queue, create_output=create_output,
                                    num_outputs=num_outputs, shared_output=shared_output)

        try:
            self.createConnection(address)
            self._chunk_size = chunk_size * 8192
            self._flush_timeout = flush_timeout
            self._packets_collected = 0
            self._packet_buffer = bytearray(2*self._chunk_size)
            self._packet_buffer_view = memoryview(self._packet_buffer)
            self._recv_bytes = 0
            self._total_time = 0.0
            self._longtime = longtime
            self._dataq = Queue() # queue for raw2Disk
            self._record = Value(ctypes.c_bool, 0)
            self._outfile_name = 'test'
        except Exception as e:
            self.error('Exception occured in init!!!')
            self.error(e, exc_info=True)
            raise

    def createConnection(self, address):
        """Establishes a UDP connection to spidr"""
        self._sock = socket.socket(socket.AF_INET,  # Internet
                                   socket.SOCK_DGRAM)  # UDP
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 5_500_000) # NIC buffer 5.5Mb?
        self._sock.settimeout(1.0)
        self.info('Establishing connection to : {}'.format(address))
        self._sock.bind(address)

    def pre_run(self):
        self._last_update = time.time()

    def post_run(self):
        if len(self._packet_buffer) > 1:
            #print("Debug: ", len(self._packet_buffer))
            packet = np.frombuffer(self._packet_buffer, dtype=np.uint64)
            #packet = np.frombuffer(b''.join(self._packet_buffer), dtype=np.uint64)
            #print("Debug1: ", len(packet))
        else:
            packet = np.frombuffer(self._packet_buffer[0], dtype=np.uint64)
        if packet.size > 0:
            if self.record:
                self._dataq.put(packet)
            return MessageType.RawData, (packet, self._longtime.value)
        else:
            return None, None

    def get_useful_packets(self, packet):
        # Get the header
        header = ((packet & 0xF000000000000000) >> 60) & 0xF
        subheader = ((packet & 0x0F00000000000000) >> 56) & 0xF
        pix_filter = (header == 0xA) | (header == 0xB)
        trig_filter = ((header == 0x4) | (header == 0x6)) & (subheader == 0xF)
        tpx_filter = pix_filter | trig_filter
        tpx_packets = packet[tpx_filter]
        return tpx_packets

    @property
    def record(self):
        """Enables saving data to disk

        Determines whether the class will perform processing, this has the result of signalling the process to terminate.
        If there are objects ahead of it then they will stop recieving data
        if an input queue is required then it will get from the queue before checking processing
        This is done to prevent the queue from growing when a process behind it is still working

        Parameters
        -----------
        value : bool
            Enable value

        Returns
        -----------
        bool:
            Whether the process should record and write to disk or not
        """
        return bool(self._record.value)

    @record.setter
    def record(self, value):
        self.debug(f'Setting record flag to {value}')
        self._record.value = int(value)

    @property
    def outfile_name(self):
        return self._outfile_name

    @outfile_name.setter
    def outfile_name(self, fileN):
        self.info(f'Setting file name flag to {fileN}')
        # start raw2Disk
        self._outfile_name = fileN
        self.stopRaw2Disk()
        self.startRaw2Disk()

    def process(self, data_type=None, data=None):
        start = time.time()
        # self.debug('Reading')
        try:
            self._recv_bytes += self._sock.recv_into(self._packet_buffer_view[self._recv_bytes:])
        except socket.timeout:
            return None, None
        except socket.error:
            return None, None
        # self.debug('Read {}'.format(raw_packet))

        self._packets_collected += 1
        end = time.time()

        self._total_time += end - start
        if self._packets_collected % 1000 == 0:
            self.debug('Packets collected {}'.format(self._packets_collected))
            self.debug('Total time {} s'.format(self._total_time))

        flush_time = end - self._last_update

        if (self._recv_bytes > self._chunk_size) or (flush_time > self._flush_timeout):
            packet = np.frombuffer(self._packet_buffer_view[:self._recv_bytes], dtype=np.uint64)

            # tpx_packets = self.get_useful_packets(packet)

            self._recv_bytes = 0
            self._last_update = time.time()
            if packet.size > 0:
                if self.record:
                    self._dataq.put(packet)
                return MessageType.RawData, (packet, self._longtime.value)
            else:
                return None, None
        else:
            return None, None

    def startRaw2Disk(self):
        self.info(f'start raw2Disk process')

        # generate worker to save the data directly to disk
        self._raw2Disk = raw2Disk(dataq=self._dataq, fileN=self.outfile_name)
        self._raw2Disk.enable = True
        self._raw2Disk.start()

    def stopRaw2Disk(self):
        self.info(f'stopping raw2Disk process')
        self._raw2Disk.enable = False
        self._raw2Disk.join(5.0)  # give it a chance to empty some more of the queue
        self._raw2Disk.terminate()
        self._raw2Disk.join()

        while not self._dataq.empty():
            self._dataq.get()
        self.info('Process Raw2Disk stop complete')