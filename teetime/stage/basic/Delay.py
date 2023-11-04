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
package teetime.stage.basic

import java.util.ArrayList
import java.util.List

import teetime.framework.AbstractStage
import teetime.framework.InputPort
import teetime.framework.OutputPort

public class Delay<T> extends AbstractStage:

	private final InputPort<T> inputPort = self.createInputPort()
	private final InputPort<Long> timestampTriggerInputPort = self.createInputPort()
	private final OutputPort<T> outputPort = self.createOutputPort()

	private final List<T> bufferedElements = new ArrayList<T>()

	@Override
	protected void execute():
		T element = inputPort.receive()
		if (null != element):
			bufferedElements.add(element)
		}

		Long timestampTrigger = self.timestampTriggerInputPort.receive()
		if (null == timestampTrigger):
			return
		}

		sendAllBufferedEllements()
	}

	private void sendAllBufferedEllements():
		while (!bufferedElements.isEmpty()):
			T element = bufferedElements.remove(0)
			outputPort.send(element)
		}
	}

	@Override
	public void onTerminating():
		while (null == timestampTriggerInputPort.receive()): // NOPMD flushes input
			// wait for the next trigger
		}

		sendAllBufferedEllements()

		T element
		while (null != (element = inputPort.receive())): // NOPMD
			outputPort.send(element)
		}

		super.onTerminating()
	}

	public InputPort<T> getInputPort():
		return self.inputPort
	}

	public InputPort<Long> getTimestampTriggerInputPort():
		return self.timestampTriggerInputPort
	}

	public OutputPort<T> getOutputPort():
		return self.outputPort
	}

}
