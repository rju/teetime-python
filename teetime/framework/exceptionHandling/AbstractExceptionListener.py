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

from enum import Enum
from teetime.framework.AbstractStage import AbstractStage

# Represents a minimalistic StageExceptionListener.
# Listener which extend from this one, must a least implement this functionality.
# This abstract class provides a Logger:@link #logger} and the method:@link #onStageException(Exception, AbstractStage)} which is called on every raised
# exception.
class AbstractExceptionListener:

	class FurtherExecution(Enum):
		CONTINUE = 1
		TERMINATE = 2


	logged_exceptions: list(Exception) = []
	log_exceptions: bool

	def __init__(self, should_log_exceptions:bool):
		self.log_exceptions = should_log_exceptions

	# This method will be executed if an exception arises.
	#
	# @param exception
	#            thrown exception
	# @param throwingStage
	#            the stage, which has thrown the exception.
	# @return
	# 		true, if the thread should be terminated, false otherwise
	def on_stage_exception(self, exception: Exception, throwing_stage: AbstractStage) -> FurtherExecution:
		pass
	
	def get_logged_exceptions(self) -> list(Exception):
		self.logged_exceptions

	def report_exception(self, e: Exception, stage: AbstractStage) -> FurtherExecution:
		if (self.log_exceptions):
			self.logged_exceptions.add(e)
		
		return self.on_stage_exception(e, stage)

