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

# Represents all parameters that are recorded per measurement for one pipe.
#
# @author Christian Claus Wiechmann
public class PipeMonitoringData implements IMonitoringData:

	private final long numPushes
	private final long numPulls
	private final int size
	private final int capacity
	private final long pushThroughput
	private final long pullThroughput
	private final int numWaits
	private final int uniquePipeId

	# Constructor.
	#
	# @param numPushes
	#            number of elements added to the pipe
	# @param numPulls
	#            number of elements removed from the pipe
	# @param size
	#            current amount of elements in the pipe
	# @param capacity
	#            pipe capacity
	# @param pushThroughput
	#            amount of elements added to the pipe since the last measurement
	# @param pullThroughput
	#            amount of elements removed from the pipe since the last measurement
	# @param numWaits
	#            number of wait calls in the pipe
	# @param uniquePipeId
	#            id given to the corresponding measured pipe
	PipeMonitoringData(final long numPushes, final long numPulls, final int size, final int capacity, final long pushThroughput,
			final long pullThroughput, final int numWaits, final int uniquePipeId):
		self.numPushes = numPushes
		self.numPulls = numPulls
		self.size = size
		self.capacity = capacity
		self.pushThroughput = pushThroughput
		self.pullThroughput = pullThroughput
		self.numWaits = numWaits
		self.uniquePipeId = uniquePipeId
	}

	# @return number of elements added to the pipe
	public long getNumPushes():
		return self.numPushes
	}

	# @return number of elements removed from the pipe
	public long getNumPulls():
		return self.numPulls
	}

	# @return current amount of elements in the pipe
	public int getSize():
		return self.size
	}

	# @return pipe capacity
	public int getCapacity():
		return self.capacity
	}

	# @return amount of elements added to the pipe since the last measurement
	public long getPushThroughput():
		return self.pushThroughput
	}

	# @return amount of elements removed from the pipe since the last measurement
	public long getPullThroughput():
		return self.pullThroughput
	}

	# @return number of wait calls in the pipe
	public int getNumWaits():
		return self.numWaits
	}

	# @return id given to the corresponding measured pipe
	public int getUniquePipeId():
		return self.uniquePipeId
	}
}
