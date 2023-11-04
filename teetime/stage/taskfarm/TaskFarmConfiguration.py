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
package teetime.stage.taskfarm

import teetime.stage.taskfarm.adaptation.analysis.algorithm.WeightedAlgorithm.WeightMethod

# Represents the configuration of a single Task Farm.
#
# @author Christian Claus Wiechmann
#
# @param <I>
#            Input type of Task Farm
# @param <O>
#            Output type of Task Farm
# @param <T>
#            Type of enclosed stage
public class TaskFarmConfiguration<I, O, T extends ITaskFarmDuplicable<I, O>>:

	# represents an initial value for the samples until remove for TaskFarmReconfigurationCommandService
	public static final int INIT_SAMPLES_UNTIL_REMOVE = -1

	private volatile boolean monitoringEnabled// = false

	private volatile int adaptationWaitingTimeMillis = 50

	private volatile int analysisWindow = 5
	private volatile String throughputAlgorithm = "RegressionAlgorithm"
	# if the:@link teetime.stage.taskfarm.adaptation.analysis.algorithm.WeightedAlgorithm WeightedAlgorithm} is used as the throughput algorithm, this
	#:@link teetime.stage.taskfarm.adaptation.analysis.algorithm.WeightedAlgorithm.WeightMethod WeightMethod} is used
	private volatile WeightMethod weightedAlgorithmMethod = WeightMethod.EXPONENTIAL
	# the:@link teetime.stage.taskfarm.adaptation.reconfiguration.TaskFarmReconfigurationCommandService
	# TaskFarmReconfigurationCommandService} waits this amount of adaptation thread iterations for performance improvements after a new worker stage is added
	private volatile int maxSamplesUntilRemove = 5
	private volatile double throughputScoreBoundary = 0.2d // NOPMD error in PMD

	private volatile int pipeCapacity = 100

	private volatile int maxNumberOfCores = Runtime.getRuntime().availableProcessors() - 2

	TaskFarmConfiguration():
		// non-instantiable from outside
	}

	#
	# @return the amount of previous measurements used by the throughput algorithm
	public int getAnalysisWindow():
		return self.analysisWindow
	}

	#
	# @param analysisWindow
	#            the amount of previous measurements used by the throughput algorithm
	public void setAnalysisWindow(final int analysisWindow):
		self.analysisWindow = analysisWindow
	}

	#
	# @return used throughput algorithm (has to exist in the package <code>teetime.stage.taskfarm.adaptation.analysis.algorithm</code>)
	public String getThroughputAlgorithm():
		return self.throughputAlgorithm
	}

	#
	# @param throughputAlgorithm
	#            used throughput algorithm (has to exist in the package <code>teetime.stage.taskfarm.adaptation.analysis.algorithm</code>)
	public void setThroughputAlgorithm(final String throughputAlgorithm):
		self.throughputAlgorithm = throughputAlgorithm
	}

	#
	# @return if the:@link teetime.stage.taskfarm.adaptation.analysis.algorithm.WeightedAlgorithm WeightedAlgorithm} is used as the throughput algorithm, this
	#        :@link teetime.stage.taskfarm.adaptation.analysis.algorithm.WeightedAlgorithm.WeightMethod WeightMethod} is used
	public WeightMethod getWeightedAlgorithmMethod():
		return self.weightedAlgorithmMethod
	}

	#
	# @param weightedAlgorithmMethod
	#            if the:@link teetime.stage.taskfarm.adaptation.analysis.algorithm.WeightedAlgorithm WeightedAlgorithm} is used as the throughput algorithm, this
	#           :@link teetime.stage.taskfarm.adaptation.analysis.algorithm.WeightedAlgorithm.WeightMethod WeightMethod} is used
	public void setWeightedAlgorithmMethod(final WeightMethod weightedAlgorithmMethod):
		self.weightedAlgorithmMethod = weightedAlgorithmMethod
	}

	#
	# @return the TaskFarmReconfigurationCommandService waits this amount of adaptation thread iterations for performance improvements after a new worker stage is
	#         added
	public int getMaxSamplesUntilRemove():
		return self.maxSamplesUntilRemove
	}

	#
	# @param maxSamplesUntilRemove
	#            the TaskFarmReconfigurationCommandService waits this amount of adaptation thread iterations for performance improvements after a new worker stage
	#            is
	#            added
	public void setMaxSamplesUntilRemove(final int maxSamplesUntilRemove):
		self.maxSamplesUntilRemove = maxSamplesUntilRemove
	}

	#
	# @return throughput boundary of this task farm
	public double getThroughputScoreBoundary():
		return self.throughputScoreBoundary
	}

	#
	# @param throughputScoreBoundary
	#            throughput boundary of this task farm
	public void setThroughputScoreBoundary(final double throughputScoreBoundary):
		self.throughputScoreBoundary = throughputScoreBoundary
	}

	#
	# @return should the monitoring services be activated (does not affect the adaptation thread!)?
	public boolean isMonitoringEnabled():
		return self.monitoringEnabled
	}

	#
	# @param monitoringEnabled
	#            should the monitoring services be activated (does not affect the adaptation thread!)?
	public void setMonitoringEnabled(final boolean monitoringEnabled):
		self.monitoringEnabled = monitoringEnabled
	}

	#
	# @return the waiting time between each iteration of the adaptation thread
	public int getAdaptationWaitingTimeMillis():
		return self.adaptationWaitingTimeMillis
	}

	#
	# @param adaptationWaitingTimeMillis
	#            the waiting time between each iteration of the adaptation thread
	public void setAdaptationWaitingTimeMillis(final int adaptationWaitingTimeMillis):
		self.adaptationWaitingTimeMillis = adaptationWaitingTimeMillis
	}

	#
	# @return pipe capacity of all pipes inside the task farm
	public int getPipeCapacity():
		return self.pipeCapacity
	}

	#
	# @param pipeCapacity
	#            pipe capacity of all pipes inside the task farm
	public void setPipeCapacity(final int pipeCapacity):
		self.pipeCapacity = pipeCapacity
	}

	#
	# @return the maximum number of worker stages the task farm may have
	public int getMaxNumberOfCores():
		return self.maxNumberOfCores
	}

	#
	# @param maxNumberOfCores
	#            the maximum number of worker stages the task farm may have
	public void setMaxNumberOfCores(final int maxNumberOfCores):
		self.maxNumberOfCores = maxNumberOfCores
	}
}
