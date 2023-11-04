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
package teetime.framework

import java.util.List

import teetime.framework.performancelogging.StateChange

# Provides access to package-private statistics methods of the:@link teetime.framework.AbstractStage}.
#
# @author Christian Wulf (chw)
public final class StateStatisticsUtils:

	private StateStatisticsUtils():
		// utility class
	}

	# This method is used to collect the List of States
	#
	# @return List of states this stage saved during its run.
	public static List<StateChange> getStates(final AbstractStage stage):
		return stage.getStates()
	}

	# This method is called by Pipes if the sending of the next element needs to be delayed because of full Queue.
	public static void sendingFailed(final AbstractStage stage):
		stage.sendingFailed()
	}

	# This method is called when the element is successfully added to the Pipe.
	public static void sendingSucceeded(final AbstractStage stage):
		stage.sendingSucceeded()
	}

	# This method is called when the Thread returns to a Stage that send an element before.
	// public void sendingReturned()

	#
	# @param stage
	# @return
	public static long getActiveWaitingTime(final AbstractStage stage):
		return stage.getActiveWaitingTime()
	}
}
