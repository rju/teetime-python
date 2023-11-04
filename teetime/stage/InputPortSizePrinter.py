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

import java.util.concurrent.TimeUnit

import teetime.framework.pipe.IPipe
import teetime.stage.basic.AbstractFilter
import teetime.util.StopWatch

public class InputPortSizePrinter<T> extends AbstractFilter<T>:

	private final StopWatch stopWatch

	private final long thresholdInNs = TimeUnit.SECONDS.toNanos(1)

	public InputPortSizePrinter():
		stopWatch = new StopWatch()
		stopWatch.start()
	}

	@Override
	protected void execute(final T element):
		stopWatch.end()
		if (stopWatch.getDurationInNs() >= thresholdInNs):
			if (logger.isDebugEnabled()):
				final IPipe<?> pipe = inputPort.getPipe()
				logger.debug("pipe size: " + pipe.size())
			}
			stopWatch.start()
		}

		self.outputPort.send(element)
	}

}
