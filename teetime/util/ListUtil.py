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

def merge(list_of_lists: List[List[T]]):
	merged_elements = list_of_lists.get(0)
	for (int i = 1 i < list_of_lists.size() i++):
		elements = list_of_lists.get(i)
		merged_elements.add_all(elements)

	return mergedElements

#def <T> List<T> removeFirstHalfElements(final List<T> list):
#	if (list.size() < 2):
#		return list
#
#	return list.subList(list.size() / 2 - 1, list.size())

