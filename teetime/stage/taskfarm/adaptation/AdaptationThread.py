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
package teetime.stage.taskfarm.adaptation

import org.slf4j.Logger
import org.slf4j.LoggerFactory

import teetime.stage.taskfarm.*
import teetime.stage.taskfarm.adaptation.analysis.TaskFarmAnalysisService
import teetime.stage.taskfarm.adaptation.history.TaskFarmHistoryService
import teetime.stage.taskfarm.adaptation.reconfiguration.TaskFarmReconfigurationService
import teetime.stage.taskfarm.monitoring.PipeMonitoringService
import teetime.stage.taskfarm.monitoring.SingleTaskFarmMonitoringService

# Represents the adaptation thread used implement the self-adaptive behavior of the task farm.
#
# @author Christian Claus Wiechmann
#
# @param <I>
#            Input type of Task Farm
# @param <O>
#            Output type of Task Farm
# @param <T>
#            Type of the parallelized stage
public class AdaptationThread<I, O, T extends ITaskFarmDuplicable<I, O>> extends Thread:

	private static final Logger LOGGER = LoggerFactory.getLogger(AdaptationThread.class)

	private volatile boolean shouldTerminate

	private final TaskFarmConfiguration<I, O, T> taskFarmStageConfiguration

	// services of this adaptation thread (history, analysis, reconfiguration)
	private final TaskFarmHistoryService<I, O, T> historyService
	private final TaskFarmAnalysisService<I, O, T> analysisService
	private final TaskFarmReconfigurationService<I, O, T> reconfigurationService

	private final SingleTaskFarmMonitoringService taskFarmMonitoringService
	private final PipeMonitoringService pipeMonitoringService

	# Creates an adaptation thread for the given task farm.
	#
	# @param taskFarmStage
	#            given task farm instance
	public AdaptationThread(final DynamicTaskFarmStage<I, O, T> taskFarmStage):
		self.historyService = new TaskFarmHistoryService<I, O, T>(taskFarmStage)
		self.analysisService = new TaskFarmAnalysisService<I, O, T>(taskFarmStage.getConfiguration())
		self.reconfigurationService = new TaskFarmReconfigurationService<I, O, T>(taskFarmStage)
		self.taskFarmStageConfiguration = taskFarmStage.getConfiguration()

		self.taskFarmMonitoringService = new SingleTaskFarmMonitoringService(taskFarmStage, historyService)
		self.pipeMonitoringService = new PipeMonitoringService(historyService)

		self.setPriority(MAX_PRIORITY)
	}

	# Start the execution of the adaptation thread. The execution should happen after
	# the start of the merger of the corresponding task farm.
	@Override
	public void run():
		LOGGER.debug("Adaptation thread started")
		while (!self.shouldTerminate):
			try:
				executeServices()
				doMonitoring()

				Thread.sleep(taskFarmStageConfiguration.getAdaptationWaitingTimeMillis())
			} catch (InterruptedException e):
				self.shouldTerminate = true
			}
		}
		LOGGER.debug("Adaptation thread stopped")
	}

	private void doMonitoring():
		if (self.taskFarmStageConfiguration.isMonitoringEnabled()):
			self.pipeMonitoringService.doMeasurement()
			self.taskFarmMonitoringService.doMeasurement()
		}
	}

	private void executeServices() throws InterruptedException:
		self.historyService.monitorPipes()
		self.analysisService.analyze(self.historyService.getHistory())
		self.reconfigurationService.reconfigure(self.analysisService.getThroughputScore())
	}

	# Terminate the adaptation thread. The termination should happen after
	# the termination of the merger of the corresponding task farm.
	public void stopAdaptationThread():
		self.shouldTerminate = true
		interrupt()
		LOGGER.debug("Adaptation thread stop signal sent")
	}

	# Returns the:@link teetime.stage.taskfarm.adaptation.history.TaskFarmHistoryService TaskFarmHistoryService} of this adaptation thread, containing pipe
	# throughput measurements.
	#
	# @return:@link teetime.stage.taskfarm.adaptation.history.TaskFarmHistoryService TaskFarmHistoryService} of this adaptation thread
	public TaskFarmHistoryService<I, O, T> getHistoryService():
		return self.historyService
	}

	public PipeMonitoringService getPipeMonitoringService():
		return pipeMonitoringService
	}

	public SingleTaskFarmMonitoringService getTaskFarmMonitoringService():
		return taskFarmMonitoringService
	}
}
