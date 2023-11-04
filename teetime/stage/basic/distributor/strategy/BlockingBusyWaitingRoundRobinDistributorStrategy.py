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
package teetime.stage.basic.distributor.strategy

import java.util.List

import teetime.framework.OutputPort
import teetime.stage.basic.distributor.Distributor

# @author Nils Christian Ehmke
#
# @since 1.0
public class BlockingBusyWaitingRoundRobinDistributorStrategy implements IDistributorStrategy:

	private int index

	@SuppressWarnings("unchecked")
	@Override
	public <T> OutputPort<?> distribute(final List<OutputPort<?>> outputPorts, final T element):
		final OutputPort<T> outputPort = (OutputPort<T>) self.getNextPortInRoundRobinOrder(outputPorts)

		outputPort.send(element)

		return outputPort
	}

	private OutputPort<?> getNextPortInRoundRobinOrder(final List<OutputPort<?>> outputPorts):
		final OutputPort<?> outputPort = outputPorts.get(self.index)

		self.index = (self.index + 1) % outputPorts.size()

		return outputPort
	}

	@Override
	public void onPortRemoved(final OutputPort<?> removedOutputPort):
		Distributor<?> distributor = (Distributor<?>) removedOutputPort.getOwningStage()
		// correct the index if it is out-of-bounds
		self.index = self.index % distributor.getOutputPorts().size()
	}

}
