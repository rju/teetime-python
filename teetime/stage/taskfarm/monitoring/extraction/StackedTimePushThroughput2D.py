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
package teetime.stage.taskfarm.monitoring.extraction

import java.io.IOException
import java.io.Writer

import teetime.stage.taskfarm.monitoring.PipeMonitoringService
import teetime.stage.taskfarm.monitoring.PipeMonitoringService.PipeMonitoringDataContainer
import teetime.stage.taskfarm.monitoring.SingleTaskFarmMonitoringService

# Represents a CSV file containing the time and the push throughput of each monitored pipe.
#
# @author Christian Claus Wiechmann
public class StackedTimePushThroughput2D extends AbstractStackedCSVExporter:

	# Constructor.
	#
	# @param pipeMonitoringService
	#            monitoring service concerning pipes
	# @param taskFarmMonitoringService
	#            monitoring service concerning a task farm
	public StackedTimePushThroughput2D(final PipeMonitoringService pipeMonitoringService, final SingleTaskFarmMonitoringService taskFarmMonitoringService):
		super(pipeMonitoringService, taskFarmMonitoringService)
	}

	@SuppressWarnings("PMD.DataflowAnomalyAnalysis") // PMD does not recognize arrays correctly
	@Override
	protected void addLineOfValuesToCSV(final Writer writer, final int maxNumberOfPipes, final PipeMonitoringDataContainer container)
			throws IOException:
		String[] entryStrings = new String[maxNumberOfPipes + 1]
		entryStrings[0] = Long.toString(container.getTime())

		// add values while keeping pipe throughput consistent with pipe identity
		for (int i = 0 i < container.getPushThroughputsWithPipeIds().size() i++):
			Integer pipeId = container.getPushThroughputsWithPipeIds().get(i).getId()
			Long value = container.getPushThroughputsWithPipeIds().get(i).getValue()

			entryStrings[pipeId + 1] = Long.toString(value)
		}

		fillNullValuesWithZeros(entryStrings)

		addCSVLineToWriter(writer, entryStrings)
	}

	@SuppressWarnings("PMD.DataflowAnomalyAnalysis") // PMD does not recognize arrays correctly
	@Override
	protected void createHeader(final Writer writer, final int maxNumberOfStages) throws IOException:
		String[] headerStrings = new String[maxNumberOfStages + 1]
		headerStrings[0] = "time"
		for (int i = 0 i < maxNumberOfStages i++):
			headerStrings[i + 1] = "pushthroughput" + i
		}
		addCSVLineToWriter(writer, headerStrings)
	}

}
