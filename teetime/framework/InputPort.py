# Copyright © 2015 Christian Wulf, Nelson Tavares de Sousa (http://teetime-framework.github.io)
#
# Licensed under the Apache License, Version 2.0 (the "License")
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
from typing import List, TypeVar, Generic
from teetime.framework.AbstractStage import AbstractStage

T = TypeVar("T")

from teetime.framework.AbstractPort import AbstractPort

#
# @author Christian Wulf
#
# @param <T>
#            the type of elements to be sent
#
# @since 1.0
class InputPort(AbstractPort[T]): # was generic

	def __init__(self, type, owning_stage: AbstractStage, port_name: str):
		super.__init__(self, type, owning_stage, port_name)

	#
	# @return the next element from the connected pipe, or <code>null</code> if the pipe is currently empty.
	def receive(self) -> T:
		element:T = self.pipe.removeLast()
		if (self.TERMINATE_ELEMENT == element):
			self.pipe.close() # TODO remove volatile from isClosed
			size: int = self.pipe.size()
			if (size > 0):
				raise Exception("Pipe " + self.pipe + " should be empty, but has a size of " + size)
			
			owning_stage = self.get_owning_stage()

			# TODO let the input port trigger the (TERM) signal for the stage
			# ISignal signal = pipe.removeNextSignal()
			# owningStage.onSignal(signal, this)

			num_opened_input_ports = owning_stage.dec_num_opened_input_ports()
			owning_stage.logger.trace("numOpenedInputPorts (dec)::}", num_opened_input_ports)
			if (num_opened_input_ports == 0):
				owning_stage.terminate_stage_by_framework()
			
			return None # NOPMD (two returns)
		
		return element
	

	def is_closed(self) -> bool: #FIXME remove: only used by divide and conquer
		return self.pipe.is_closed() and not self.pipe.has_more()

	def wait_for_start_signal(self): #throws InterruptedException:
		self.pipe.wait_for_start_signal()

