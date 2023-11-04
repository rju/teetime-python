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

from teetime.framework.pipe.pipe import IPipe
from teetime.util.framework.port.PortRemovedListener import PortRemovedListener

T = TypeVar("T")

class PortList(Generic[T]):

	_opened_ports = list() # list

	_closed_ports = list() # list= new ArrayList<T>()

	_ports_removed_listeners = list() # = new HashSet<PortRemovedListener<T>>()

	def get_opened_ports(self) -> List[T]:
		return self._opened_ports

	def add(self, port: T) -> T:
		return self._opened_ports.add(port)

	def remove(self, port: T) -> bool:
		removed: bool = self._opened_ports.remove(port) #// BETTER remove by index for performance reasons
		self._fire_port_removed(port)
		if (not removed):
			raise IllegalStateException()

		return removed

	def close(self, port: T) -> bool:
		removed: bool = self.remove(port)
		return removed

	def size(self) -> int:
		return self._opened_ports.size()

	def _fire_port_removed(self, removed_port: T):
		for listener in self._ports_removed_listeners:
			listener.on_port_removed(removed_port)

	def add_port_removed_listener(self, listener: PortRemovedListener[T]):
		self._ports_removed_listeners.add(listener)

