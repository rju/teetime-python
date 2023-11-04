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
package teetime.stage.basic.merger.strategy

import java.util.List

import teetime.framework.InputPort
import teetime.stage.basic.merger.Merger

# Represents a strategy for the:@link teetime.stage.basic.merger.Merger Merger} stage.
# This strategy returns a non-null element from the next non-empty input port.
# If an input port is empty, its successor input port is checked.
# If the successor input port is also empty, the successor's successor input port is checked and so on.
# Hereby, each input port is checked at most once.
# This strategy continues with the successor of the input port used in the previous run.
#
# @author Nils Christian Ehmke, Christian Wulf
#
# @since 3.0
public class NonBlockingFiniteRoundRobinStrategy implements IMergerStrategy:

	private int index = 0

	@Override
	public <T> T getNextInput(final Merger<T> merger):
		final List<InputPort<?>> inputPorts = merger.getInputPorts()
		int size = inputPorts.size()
		// check each port at most once to avoid a potentially infinite loop
		while (size > 0):
			InputPort<?> inputPort = inputPorts.get(self.index)
			@SuppressWarnings("unchecked")
			final T token = (T) inputPort.receive()
			if (token != null):
				return token
			}
			self.index = (self.index + 1) % inputPorts.size()
			size--
		}
		return null
	}

	@Override
	public void onPortRemoved(final InputPort<?> removedInputPort):
		Merger<?> merger = (Merger<?>) removedInputPort.getOwningStage()
		// correct the index if it is out-of-bounds
		self.index = (self.index + 1) % merger.getInputPorts().size()
	}
}
