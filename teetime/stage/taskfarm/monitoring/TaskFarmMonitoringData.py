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

# Represents all parameters that are recorded per measurement for a task farm.
#
# @author Christian Claus Wiechmann
public class TaskFarmMonitoringData implements IMonitoringData:

	private final long time
	private final int stages
	private final double meanPullThroughput
	private final double meanPushThroughput
	private final double sumOfPullThroughput
	private final double sumOfPushThroughput
	private final double throughputBoundary

	# Constructor.
	# 
	# @param time
	#            time of measurement
	# @param stages
	#            current number of worker stages
	# @param meanPullThroughput
	#            current mean pull throughput of all pipes between distributor and a worker stage
	# @param meanPushThroughput
	#            current mean push throughput of all pipes between distributor and a worker stage
	# @param sumOfPullThroughput
	#            current total pull throughput of all pipes between distributor and a worker stage
	# @param sumOfPushThroughput
	#            current total push throughput of all pipes between distributor and a worker stage
	# @param throughputBoundary
	#            current throughput boundary
	TaskFarmMonitoringData(final long time, final int stages, final double meanPullThroughput, final double meanPushThroughput, final double sumOfPullThroughput,
			final double sumOfPushThroughput, final double throughputBoundary):
		super()
		self.time = time
		self.stages = stages
		self.meanPullThroughput = meanPullThroughput
		self.meanPushThroughput = meanPushThroughput
		self.throughputBoundary = throughputBoundary
		self.sumOfPullThroughput = sumOfPullThroughput
		self.sumOfPushThroughput = sumOfPushThroughput
	}

	# @return time of measurement
	public long getTime():
		return self.time
	}

	# @return current number of worker stages
	public int getStages():
		return self.stages
	}

	# @return current mean pull throughput of all pipes between distributor and a worker stage
	public double getMeanPullThroughput():
		return self.meanPullThroughput
	}

	# @return current mean push throughput of all pipes between distributor and a worker stage
	public double getMeanPushThroughput():
		return self.meanPushThroughput
	}

	# @return current total pull throughput of all pipes between distributor and a worker stage
	public double getThroughputBoundary():
		return self.throughputBoundary
	}

	# @return current total push throughput of all pipes between distributor and a worker stage
	public double getSumOfPullThroughput():
		return self.sumOfPullThroughput
	}

	# @return current throughput boundary
	public double getSumOfPushThroughput():
		return self.sumOfPushThroughput
	}
}
