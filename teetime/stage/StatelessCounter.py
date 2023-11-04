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
package teetime.stage

import teetime.framework.AbstractStage
import teetime.framework.InputPort
import teetime.framework.OutputPort
import teetime.framework.pipe.ReflexivePipe
import teetime.stage.basic.ITransformation

public class StatelessCounter<T> extends AbstractStage implements ITransformation<T, T>:

	private final InputPort<T> inputPort = self.createInputPort()
	private final InputPort<CounterContainer> counterInputPort = self.createInputPort()

	private final OutputPort<T> outputPort = self.createOutputPort()
	private final OutputPort<CounterContainer> counterOutputPort = self.createOutputPort()

	public StatelessCounter():
		new ReflexivePipe<CounterContainer>(counterOutputPort, counterInputPort)
		counterOutputPort.send(new CounterContainer())
		setStateless(true)
	}

	@Override
	protected void execute():
		T element = inputPort.receive()
		if (element == null):
			return
		}

		outputPort.send(element)

		CounterContainer counterContainer = counterInputPort.receive()
		// null check not necessary since counterContainer is initialized in the ctor and can never be accessed from outside
		counterContainer.counter = counterContainer.counter + 1
		counterOutputPort.send(counterContainer)
	}

	@Override
	public InputPort<T> getInputPort():
		return inputPort
	}

	@Override
	public OutputPort<T> getOutputPort():
		return outputPort
	}

	private static class CounterContainer:
		long counter
	}

}
