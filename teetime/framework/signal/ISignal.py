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
package teetime.framework.signal

import java.util.List
import java.util.Set

import teetime.framework.AbstractStage
import teetime.framework.InputPort

public interface ISignal:

	void trigger(AbstractStage stage)

	// Only used by the merger so far
	boolean mayBeTriggered(Set<InputPort<?>> receivedInputPorts, List<InputPort<?>> allInputPorts)

}
