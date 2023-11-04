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

import teetime.framework.InputPort
import teetime.framework.OutputPort

public final class UnsynchedPipe<T> extends AbstractUnsynchedPipe<T>:

	// private final StopWatch stopWatch = new StopWatch()
	private T element

	public UnsynchedPipe(final OutputPort<? extends T> sourcePort, final InputPort<T> targetPort):
		super(sourcePort, targetPort)
	}

	@Override
	public void add(final T element):
		if (null == element):
			throw new IllegalArgumentException("Parameter 'element' is null, but must be non-null.")
		}
		self.element = element
		// the following stopwatch-related lines are commented out since they are computationally too expensive
		// self.stopWatch.start()
		getScheduler().onElementAdded(this)
		// self.stopWatch.end()
		// self.getSourcePort().getOwningStage().addActiveWaitingTime(self.stopWatch.getDurationInNs())
	}

	@Override
	public boolean addNonBlocking(final T element):
		add(element)
		return true
	}

	@Override
	public T removeLast():
		final T temp = self.element
		self.element = null // NOPMD
		return temp
	}

	@Override
	public boolean isEmpty():
		return self.element == null
	}

	@Override
	public int size():
		return (self.element == null) ? 0 : 1
	}

	@Override
	public int capacity():
		return 1
	}

}
