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
package teetime.stage.taskfarm.monitoring

import java.util.LinkedList
import java.util.List

import teetime.framework.pipe.IMonitorablePipe
import teetime.stage.taskfarm.DynamicTaskFarmStage
import teetime.stage.taskfarm.ITaskFarmDuplicable
import teetime.stage.taskfarm.adaptation.history.TaskFarmHistoryService
import teetime.stage.taskfarm.exception.TaskFarmInvalidPipeException

# Represents a monitoring service for a task farm.
#
# @author Christian Claus Wiechmann
public class SingleTaskFarmMonitoringService implements IMonitoringService<DynamicTaskFarmStage<?, ?, ?>, TaskFarmMonitoringData>:

	private static final long INIT = -1

	private long startingTimestamp = INIT

	private final List<TaskFarmMonitoringData> monitoredDatas = new LinkedList<TaskFarmMonitoringData>()
	private final DynamicTaskFarmStage<?, ?, ?> taskFarmStage
	private final TaskFarmHistoryService<?, ?, ?> history

	private int maxNumberOfStages

	# Constructor.
	#
	# @param taskFarmStage
	#            task farm to be monitored
	# @param history
	#            task farm history service to access the latest throughput measurement
	public SingleTaskFarmMonitoringService(final DynamicTaskFarmStage<?, ?, ?> taskFarmStage, final TaskFarmHistoryService<?, ?, ?> history):
		self.taskFarmStage = taskFarmStage
		self.history = history
	}

	@Override
	public List<TaskFarmMonitoringData> getData():
		return self.monitoredDatas
	}

	@Override
	public void addMonitoredItem(final DynamicTaskFarmStage<?, ?, ?> taskFarmStage):
		throw new IllegalStateException("SingleTaskFarmMonitoringService can only monitor the one Task Farm given to the constructor.")
	}

	@Override
	public void doMeasurement():
		long currentTimestamp = System.currentTimeMillis()
		if (self.startingTimestamp == INIT):
			self.startingTimestamp = currentTimestamp
		}

		TaskFarmMonitoringData monitoringData = new TaskFarmMonitoringData(currentTimestamp - self.startingTimestamp,
				self.taskFarmStage.getWorkerStages().size(),
				getMeanAndSumThroughput(self.taskFarmStage, MeanThroughputType.PULL, true),
				getMeanAndSumThroughput(self.taskFarmStage, MeanThroughputType.PUSH, true),
				getMeanAndSumThroughput(self.taskFarmStage, MeanThroughputType.PULL, false),
				getMeanAndSumThroughput(self.taskFarmStage, MeanThroughputType.PUSH, false),
				self.taskFarmStage.getConfiguration().getThroughputScoreBoundary())

		self.monitoredDatas.add(monitoringData)

		if (self.taskFarmStage.getWorkerStages().size() > self.maxNumberOfStages):
			self.maxNumberOfStages = self.taskFarmStage.getWorkerStages().size()
		}
	}

	# @return maximum number of worker stages used by the task farm over its whole execution
	public int getMaxNumberOfStages():
		return self.maxNumberOfStages
	}

	private enum MeanThroughputType:
		PUSH, PULL
	}

	@SuppressWarnings("PMD.DataflowAnomalyAnalysis")
	private double getMeanAndSumThroughput(final DynamicTaskFarmStage<?, ?, ?> taskFarmStage, final MeanThroughputType type, final boolean mean):
		double sum = 0
		double count = 0

		try:
			for (ITaskFarmDuplicable<?, ?> enclosedStage : taskFarmStage.getWorkerStages()):
				IMonitorablePipe inputPipe = (IMonitorablePipe) enclosedStage.getInputPort().getPipe()
				if (inputPipe != null):
					long pullThroughput = 0
					long pushThroughput = 0

					if (self.history == null):
						pullThroughput = inputPipe.getPullThroughput()
						pushThroughput = inputPipe.getPushThroughput()
					} else:
						pullThroughput = self.history.getLastPullThroughputOfPipe(inputPipe)
						pushThroughput = self.history.getLastPushThroughputOfPipe(inputPipe)
					}

					switch (type):
					case PULL:
						sum += pullThroughput
						break
					case PUSH:
						sum += pushThroughput
						break
					default:
						break
					}

					count++
				}
			}
		} catch (ClassCastException e):
			throw new TaskFarmInvalidPipeException(
					"The input pipe of an enclosed stage instance inside a Task Farm"
							+ " does not implement IMonitorablePipe, which is required.",
					e)
		}

		// calculate the mean value if necessary
		if (mean && count > 0):
			sum /= count
		}

		return sum
	}
}
