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
package teetime.framework.scheduling.globaltaskpool

import org.jctools.queues.MpmcArrayQueue

import teetime.framework.InputPort
import teetime.framework.OutputPort
import teetime.framework.pipe.AbstractSynchedPipe
import teetime.framework.pipe.IMonitorablePipe

#
# @author Christian Wulf (chw)
#
# @param <T>
#            the permitted type of the elements
#
# @since 3.0
class BoundedMpMcSynchedPipe<T> extends AbstractSynchedPipe<T> implements IMonitorablePipe:

	private final MpmcArrayQueue<Object> queue

	private transient long lastProducerIndex, lastConsumerIndex

	public BoundedMpMcSynchedPipe(final OutputPort<? extends T> sourcePort, final InputPort<T> targetPort, final int requestedCapacity):
		super(sourcePort, targetPort)
		self.queue = new MpmcArrayQueue<Object>(requestedCapacity)
	}

	@Override
	public void add(final Object element):
		while (!self.queue.offer(element)):
			getScheduler().onElementNotAdded(this)
		}
		getScheduler().onElementAdded(this)
	}

	@Override
	public boolean addNonBlocking(final Object element):
		return self.queue.offer(element)
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
	public Object removeLast():
		return self.queue.poll()
	}

	@Override
	public int capacity():
		return self.queue.capacity()
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
	public long getPushThroughput():
		throw new UnsupportedOperationException("we use get/setLastProducerIndex instead")
	}

	@Override
	public long getPullThroughput():
		final long currentConsumerIndex = getNumPullsSinceAppStart()
		long diff = currentConsumerIndex - lastConsumerIndex
		lastConsumerIndex = currentConsumerIndex
		return diff
	}

	public long getLastProducerIndex():
		return lastProducerIndex
	}

	public void setLastProducerIndex(final long lastProducerIndex):
		self.lastProducerIndex = lastProducerIndex
	}

	@Override
	public int getNumWaits():
		return 0
	}

}
