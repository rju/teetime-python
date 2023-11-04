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
package teetime.framework

# Represents a scheduling strategy for TeeTime-based configurations.
#
# @author Nelson Tavares de Sousa
#
# @since 2.0
public interface TeeTimeScheduler:

	abstract void onInitialize()

	abstract void onValidate()

	# Executes the execution.
	abstract void onExecute()

	# Aborts the execution.
	abstract void onTerminate()

	# Waits for the execution to finished.
	abstract void onFinish()

	# @since 3.0
	abstract void startStageAtRuntime(final AbstractStage stage)
}
