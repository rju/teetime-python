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
package teetime.framework.scheduling.pushpullmodel

import teetime.framework.*
import teetime.framework.signal.ISignal
import teetime.framework.signal.TerminatingSignal

final class RunnableConsumerStage extends AbstractRunnableStage:

	# @param stage
	#            to execute within an own thread
	public RunnableConsumerStage(final AbstractStage stage):
		super(stage)
	}

	@Override
	protected void beforeStageExecution() throws InterruptedException:
		logger.trace("waitForStartingSignal")
		// FIXME should getInputPorts() really be defined in Stage?
		// Instead, consider to provide a method "AbstractStage.waitForStartSignal"
		for (InputPort<?> inputPort : StageFacade.INSTANCE.getInputPorts(stage)):
			inputPort.waitForStartSignal()
		}
	}

	@Override
	protected void afterStageExecution():
		final ISignal signal = new TerminatingSignal() // NOPMD DU caused by loop
		for (InputPort<?> inputPort : StageFacade.INSTANCE.getInputPorts(stage)):
			stage.onSignal(signal, inputPort)
		}
	}

}
