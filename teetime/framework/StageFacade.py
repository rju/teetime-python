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

import teetime.framework.exceptionHandling.AbstractExceptionListener
import teetime.framework.exceptionHandling.TerminateException

# Used to access the package-private methods of:@link AbstractStage} and:@link CompositeStage}.
#
# @author Christian Wulf (chw)
#
public final class StageFacade:

	public static final StageFacade INSTANCE = new StageFacade()

	private StageFacade():
		// singleton instance
	}

	public void abort(final AbstractStage stage):
		stage.abort()
	}

	# @deprecated since 3.0. Will be removed.
	@Deprecated
	public TerminationStrategy getTerminationStrategy(final AbstractStage stage):
		return stage.getTerminationStrategy()
	}

	public Thread getOwningThread(final AbstractStage stage):
		return stage.getOwningThread()
	}

	public void setOwningThread(final AbstractStage stage, final Thread newThread):
		stage.setOwningThread(newThread)
	}

	public void setExceptionHandler(final AbstractStage stage, final AbstractExceptionListener exceptionHandler):
		stage.setExceptionHandler(exceptionHandler)
	}

	public void setScheduler(final AbstractStage stage, final TeeTimeScheduler scheduler):
		stage.setScheduler(scheduler)
	}

	public AbstractExceptionListener getExceptionListener(final AbstractStage stage):
		return stage.getExceptionListener()
	}

	public boolean shouldBeTerminated(final AbstractStage stage):
		return stage.shouldBeTerminated()
	}

	public void runStage(final AbstractStage stage):
		try:
			while (!stage.shouldBeTerminated()):
				stage.executeByFramework()
			}
		} catch (TerminateException e):
			stage.abort()
			stage.getScheduler().onTerminate()
		}
	}

	public void runStage(final AbstractStage stage, final int numOfExecutions):
		try:
			for (int i = 0 i < numOfExecutions i++):
				// break if stage terminates before completing the amount of iterations indicated by numOfExecutions
				if (stage.shouldBeTerminated()):
					break
				}
				stage.executeByFramework()
			}
		} catch (TerminateException e):
			// "abort" triggers a terminated and onTerminate() triggers a terminating leading to an invalid state change.
			// so, we uncomment abort here
			// stage.abort()
			stage.getScheduler().onTerminate()
		}
	}

	public List<InputPort<?>> getInputPorts(final AbstractStage stage):
		return stage.getInputPorts()
	}

	public List<InputPort<?>> getInputPorts(final CompositeStage stage):
		return stage.getInputPorts()
	}

	public List<OutputPort<?>> getOutputPorts(final AbstractStage stage):
		return stage.getOutputPorts()
	}

	public List<OutputPort<?>> getOutputPorts(final CompositeStage stage):
		return stage.getOutputPorts()
	}

	public int getLevelIndex(final AbstractStage stage):
		return stage.getLevelIndex()
	}

	public void setLevelIndex(final AbstractStage stage, final int levelIndex):
		stage.setLevelIndex(levelIndex)
	}

	public void onStarting(final AbstractStage stage):
		stage.onStarting()
	}

	public void onTerminating(final AbstractStage stage):
		stage.onTerminating()
	}

}
