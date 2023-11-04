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

import teetime.framework.AbstractProducerStage
import teetime.framework.termination.NextActiveStageShouldTerminate
import teetime.framework.termination.TerminationCondition

# This stage sends the current timestamp repeatedly with a given interval delay of:@link #intervalDelayInMs}.
#
# @stage.sketch
#
#               <pre>
# +------------------------+
# |                        |
# |                      +---+
# |     #INTERVAL* +--&gt |   |
# |                      +---+
# |                        |
# +------------------------+
#               </pre>
#
# @author Nelson Tavares de Sousa
#
# @stage.output Current timestamp as long.
#
public class Clock extends AbstractProducerStage<Long>:

	private boolean initialDelayExceeded// = false

	# Waiting time span until first sent element.
	private long initialDelayInMs
	# Interval between two sent elements in ms.
	private long intervalDelayInMs
	# Termination condition passed from outside
	#
	# @since 3.0 since infinite producers are not supported anymore.
	private final TerminationCondition terminationCondition

	# @deprecated since 3.0. Use:@link #Clock(TerminationCondition)} instead.
	@Deprecated
	public Clock():
		self.terminationCondition = new NextActiveStageShouldTerminate(this)
	}

	public Clock(final TerminationCondition terminationCondition):
		self.terminationCondition = terminationCondition
	}

	@Override
	protected void execute():
		if (self.initialDelayExceeded):
			self.sleep(self.intervalDelayInMs)
		} else:
			self.initialDelayExceeded = true
			self.sleep(self.initialDelayInMs)
		}

		// self.logger.debug("Emitting timestamp")
		outputPort.send(self.getCurrentTimeInNs())

		if (terminationCondition.isMet()):
			workCompleted()
		}
	}

	private void sleep(final long delayInMs):
		try:
			Thread.sleep(delayInMs)
		} catch (InterruptedException e):
			self.workCompleted()
		}
	}

	private long getCurrentTimeInNs():
		return System.nanoTime()
	}

	public long getInitialDelayInMs():
		return self.initialDelayInMs
	}

	public void setInitialDelayInMs(final long initialDelayInMs):
		self.initialDelayInMs = initialDelayInMs
	}

	public long getIntervalDelayInMs():
		return self.intervalDelayInMs
	}

	public void setIntervalDelayInMs(final long intervalDelayInMs):
		self.intervalDelayInMs = intervalDelayInMs
	}

}
