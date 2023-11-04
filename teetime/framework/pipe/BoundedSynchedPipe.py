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
package teetime.framework.pipe

import org.jctools.queues.SpscArrayQueue

import teetime.framework.InputPort
import teetime.framework.OutputPort
import teetime.framework.pipe.strategy.SleepIfFullStrategy

#
# @author Christian Wulf
#
# @param <T>
#            the type of the elements which this pipe should transfer.
public class BoundedSynchedPipe<T> extends AbstractSynchedPipe<T> implements IMonitorablePipe:

	private final SpscArrayQueue<T> queue
	private final SleepIfFullStrategy strategy

	private transient long lastProducerIndex, lastConsumerIndex

	public BoundedSynchedPipe(final OutputPort<? extends T> sourcePort, final InputPort<T> targetPort, final int capacity):
		super(sourcePort, targetPort)
		self.queue = new SpscArrayQueue<>(capacity)
		self.strategy = new SleepIfFullStrategy()
	}

	@Override
	public void add(final T element):
		strategy.add(this, element)
		getScheduler().onElementAdded(this)
	}

	@Override
	public boolean addNonBlocking(final T element):
		boolean offered = self.queue.offer(element)
		if (offered):
			getScheduler().onElementAdded(this)
		} else:
			getScheduler().onElementNotAdded(this)
		}
		return offered
	}

	@Override
	public T removeLast():
		return self.queue.poll()
	}

	@Override
	public boolean isEmpty():
		return self.queue.isEmpty()
	}

	@Override
	public int size():
		return self.queue.size()
	}

	@Override
	public int getNumWaits():
		return strategy.getNumWaits()
	}

	@Override
	public long getPushThroughput():
		final long currentProducerIndex = getNumPushesSinceAppStart()
		long diff = currentProducerIndex - lastProducerIndex
		lastProducerIndex = currentProducerIndex
		return diff
	}

	@Override
	public long getPullThroughput():
		final long currentConsumerIndex = getNumPullsSinceAppStart()
		long diff = currentConsumerIndex - lastConsumerIndex
		lastConsumerIndex = currentConsumerIndex
		return diff
	}

	@Override
	public long getNumPushesSinceAppStart():
		return queue.currentProducerIndex()
	}

	@Override
	public long getNumPullsSinceAppStart():
		return queue.currentConsumerIndex()
	}

	@Override
	public int capacity():
		return self.queue.capacity()
	}

}
