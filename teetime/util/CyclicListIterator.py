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
T = TypeVar('T')

# This iterator infinitely iterates over a list and allows the list to be modified without throwing a <code>ConcurrentMOdificationException</code>.
#
# @author Christian Wulf
#
# @param <T>
#            type of the elements contained in the list
class CyclicListIterator(Generic[T]):

	elements = {}

	current_index = 0

	def __init__(self, elements: List[T]):
		self.elements = elements

	def has_next() -> bool:
		return true

	def next() -> T:
		self.current_index = self.get_current_index()
		element = self.elements.get(self.current_index)
		self.current_index += 1
		return element

	def remove():
		self.currentIndex = self.get_current_index()
		self.elements.remove(self.current_index)

	private int get_current_index():
		return self.current_index % self.elements.size()

