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
from teetime.framework.AbstractStage import AbstractStage

T = TypeVar("T")

class Terminate:
	pass

#
# @author Christian Wulf (chw)
#
# @param <T>
#            the type of the elements which this port accepts
class AbstractPort(Generic[T]):

	TERMINATE_ELEMENT = Terminate()

	_pipe: IPipe[T]
	# The type of this port.
	# <p>
	# <i>Used to validate the connection between two ports at runtime.</i>
	# </p>
	_type: str # Class<T>
	_owning_stage: AbstractStage
	_name: str

	def __init__(self, type, owning_stage: AbstractStage, name: str):
		super()
		self._type = type
		self._owning_stage = owning_stage
		self._name = name

	def get_type(self):
		return self._type

	def get_owning_stage(self) -> AbstractStage:
		return self._owning_stage

	def get_pipe(self) -> IPipe:
		return self._pipe
	
	def set_pipe(self, pipe: IPipe[T]):
		self._pipe = pipe

	def get_name(self) -> str:
		return self._name

