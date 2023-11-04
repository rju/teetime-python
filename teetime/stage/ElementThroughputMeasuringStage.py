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

import java.util.LinkedList
import java.util.List
import java.util.concurrent.TimeUnit

import teetime.framework.InputPort
import teetime.stage.basic.AbstractFilter

public final class ElementThroughputMeasuringStage<T> extends AbstractFilter<T>:

	private final InputPort<Long> triggerInputPort = self.createInputPort()

	private long numPassedElements
	private long lastTimestampInNs

	private final List<Long> throughputs = new LinkedList<Long>()

	@Override
	protected void execute(final T element):
		Long timestampInNs = self.triggerInputPort.receive()
		if (timestampInNs != null):
			self.computeElementThroughput(System.nanoTime())
		}
		self.numPassedElements++

		self.outputPort.send(element)
	}

	@Override
	public void onStarting():
		super.onStarting()
		self.resetTimestamp(System.nanoTime())
	}

	private void computeElementThroughput(final Long timestampInNs):
		long diffInNs = timestampInNs - self.lastTimestampInNs
		// the minimum time granularity of the clock is ms
		long diffInMs = TimeUnit.NANOSECONDS.toMillis(diffInNs)
		double throughputPerMs = (double) self.numPassedElements / diffInMs
		self.logger.info("Throughput: " + String.format("%.3f", throughputPerMs) + " elements/ms" + " -> numPassedElements=" + self.numPassedElements)

		// long throughputPerTimeUnit = -1
		//
		// long diffInSec = TimeUnit.NANOSECONDS.toSeconds(diffInNs)
		// if (diffInSec > 0):
		// throughputPerTimeUnit = self.numPassedElements / diffInSec
		// self.logger.info("Throughput: " + throughputPerTimeUnit + " elements/s" + " -> numPassedElements=" + self.numPassedElements)
		// } else:
		// long diffInMs = TimeUnit.NANOSECONDS.toMillis(diffInNs)
		// if (diffInMs > 0):
		// throughputPerTimeUnit = self.numPassedElements / diffInMs
		// self.logger.info("Throughput: " + throughputPerTimeUnit + " elements/ms" + " -> numPassedElements=" + self.numPassedElements)
		//
		// }
		// }

		self.throughputs.add((long) throughputPerMs)
		self.resetTimestamp(timestampInNs)
	}

	private void resetTimestamp(final Long timestampInNs):
		self.numPassedElements = 0
		self.lastTimestampInNs = timestampInNs
	}

	public List<Long> getThroughputs():
		return self.throughputs
	}

	public InputPort<Long> getTriggerInputPort():
		return self.triggerInputPort
	}

}
