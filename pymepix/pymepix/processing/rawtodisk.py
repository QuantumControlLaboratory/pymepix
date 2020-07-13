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
import time
import numpy as np
from pymepix.core.log import ProcessLogger
import multiprocessing
from multiprocessing.sharedctypes import Value
import queue
from pymepix.util.storage import open_output_file, store_raw
from pymepix.processing.basepipeline import BasePipelineObject

import ctypes
import subprocess, os

class raw2Disk (BasePipelineObject):
    def __init__(self, name='raw2Disk', input_queue=None, file_name='test', create_output=True, num_outputs=1,
                 shared_output=None):
        BasePipelineObject.__init__(self, name, input_queue=input_queue, create_output=create_output,
                                    num_outputs=num_outputs, shared_output=shared_output)

        self.info(f'initialising {name}')
        if self.input_queue is not None:
            try:
                # TODO: filename from args.output in pymepix
                # possible: TimepixDevice.setupAcquisition() remove call in init
                #           > higher level call from pymepix including all args
                self._raw_file = open_output_file(file_name, 'raw')
            except:
                self.info(f'Cannot open file {file_name}')
        else:
            self.error('Exception occured in init; no data queue provided?')

        self._buffer = np.array([], dtype=np.uint64)
        self._enable = Value(ctypes.c_bool, 1)
        self._timerBool = Value(ctypes.c_bool, 0)
        self._startTime = Value(ctypes.c_double, 0)
        self._stopTime = Value(ctypes.c_double, 1)


    @property
    def timer(self):
        return self._timerBool.value

    @timer.setter
    def timer(self, value):
        self.debug('Setting timer flag to {}'.format(value))
        if value == 1:
            self._startTime.value = time.time()
        elif value == 0:
            self._stopTime.value = time.time()
        self._timerBool.value = int(value)

    def postRun(self, input_queue):
        # empty buffer before closing
        if len(self._buffer) > 0:
            store_raw(self._raw_file, (self._buffer, 1))
        # store_raw(self._raw_file, (self._buffer, 1))
        # empty queue before closing
        if not input_queue.empty():
            remains = []
            item = input_queue.get(block=False)
            while item:
                try:
                    remains.append(input_queue.get(block=False))
                except queue.Empty:
                    break
            print(f'{len(remains)} remains collected')
            store_raw(self._raw_file, (np.asarray(remains), 1))
        self._raw_file.close()

    def process(self, data_type=None, data=None):

        self._buffer = np.append(self._buffer, data)
        if len(self._buffer) > 10000:
            store_raw(self._raw_file, (self._buffer, 1))
            self._buffer = np.array([], dtype=np.uint64)

        # TODO: print only if in debug mode
        #size = np.fromfile(self._raw_file.name, dtype=np.uint64).shape[0]
        #timeDiff = self._stopTime.value - self._startTime.value
        #print(f'recieved {size} packets; {64 * size * 1e-6:.2f}MBits {(64 * size * 1e-6) / timeDiff:.2f}MBits/sec; {(64 * size * 1e-6 / 8) / timeDiff:.2f}MByte/sec')
        self.info("finished saving data")
        if os.path.getsize(self._raw_file.name) > 0:
            from subprocess import Popen
            self.info(f'start process data from: {self._raw_file.name}')
            # TODO: FLASH specific
            #Popen(['python', '/home/bl1user/timepix/conversionClient.py', self._raw_file.name])
        return None, None
