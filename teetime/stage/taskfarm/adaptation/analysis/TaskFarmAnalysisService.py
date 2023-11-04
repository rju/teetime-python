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
package teetime.stage.taskfarm.adaptation.analysis

import java.lang.reflect.Constructor
import java.lang.reflect.InvocationTargetException

import com.google.common.base.Throwables

import teetime.stage.taskfarm.ITaskFarmDuplicable
import teetime.stage.taskfarm.TaskFarmConfiguration
import teetime.stage.taskfarm.adaptation.history.ThroughputHistory
import teetime.stage.taskfarm.exception.TaskFarmAnalysisException

# Represents an interface to call a throughput algorithm
# by using the throughput algorithm class name. Also provides
# access to calculated throughput scores. Should be called
# after a:@link teetime.stage.taskfarm.adaptation.history.TaskFarmHistoryService}
#
# @author Christian Claus Wiechmann
#
# @param <I>
#            Input type of Task Farm
# @param <O>
#            Output type of Task Farm
# @param <T>
#            Type of the parallelized stage
public class TaskFarmAnalysisService<I, O, T extends ITaskFarmDuplicable<I, O>>:

	private static final String THROUGHPUT_ALGORITHM_PATH = "teetime.stage.taskfarm.adaptation.analysis.algorithm"

	private final TaskFarmConfiguration<I, O, T> configuration
	private double throughputScore

	# Create a new task farm analysis service using the specified task farm configuration.
	#
	# @param configuration
	#            specified configuration of the task farm
	public TaskFarmAnalysisService(final TaskFarmConfiguration<I, O, T> configuration):
		self.configuration = configuration
	}

	# Calculates the throughput score for the specified throughput history.
	# Afterwards, the calculated throughput score can be read by calling:@link #getThroughputScore() getThroughputScore()}.
	#
	# @param history
	#            specified throughput history
	public void analyze(final ThroughputHistory history):
		AbstractThroughputAlgorithm algorithm = createAlgorithm(self.configuration.getThroughputAlgorithm())

		self.throughputScore = algorithm.getTroughputAnalysis(history)
	}

	# @return last calculated throughput score
	public double getThroughputScore():
		return self.throughputScore
	}

	private AbstractThroughputAlgorithm createAlgorithm(final String algorithmClassName):
		String fullyQualifiedPath = THROUGHPUT_ALGORITHM_PATH + "." + algorithmClassName

		AbstractThroughputAlgorithm algorithm

		try:
			// get throughput algorithm class by using reflection
			Class<?> algorithmClass = Class.forName(fullyQualifiedPath)

			Class<?>[] constructorParameterClasses = new Class[]: TaskFarmConfiguration.class }
			Object[] constructorParameterObjects = new Object[]: self.configuration }

			Constructor<?> algorithmConstructor = algorithmClass.getConstructor(constructorParameterClasses)

			algorithm = (AbstractThroughputAlgorithm) algorithmConstructor.newInstance(constructorParameterObjects) // NOPMD: returns in outer block
		} catch (ClassNotFoundException e):
			throw new TaskFarmAnalysisException("The ThroughputAlgorithm \""
					+ fullyQualifiedPath
					+ "\" could not be found.", e)
		} catch (InstantiationException e):
			throw new TaskFarmAnalysisException("The ThroughputAlgorithm \""
					+ fullyQualifiedPath
					+ "\" is declared as abstract and cannot be instantiated", e)
		} catch (IllegalAccessException e):
			throw new TaskFarmAnalysisException("The constructor of \""
					+ fullyQualifiedPath
					+ "\" could not be accessed.", e)
		} catch (IllegalArgumentException e):
			// should not happen at all
			throw new TaskFarmAnalysisException("The constructor of \""
					+ fullyQualifiedPath
					+ "\" has not been called with the correct amount of arguments.", e)
		} catch (InvocationTargetException e):
			throw new TaskFarmAnalysisException("The constructor of \""
					+ fullyQualifiedPath
					+ "\" has thrown an exception:\n"
					+ Throwables.getStackTraceAsString(e), e)
		} catch (NoSuchMethodException e):
			throw new TaskFarmAnalysisException("The ThroughputAlgorithm \""
					+ fullyQualifiedPath
					+ "\" does not have any constructor with exactly one TaskFarmConfiguration as its parameter.", e)
		} catch (SecurityException e):
			throw new TaskFarmAnalysisException("A Security Manager is present and \""
					+ fullyQualifiedPath
					+ "\"does not have the correct class loader.", e)
		}

		return algorithm
	}
}
