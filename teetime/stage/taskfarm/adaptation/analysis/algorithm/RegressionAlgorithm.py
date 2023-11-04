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
package teetime.stage.taskfarm.adaptation.analysis.algorithm

import org.apache.commons.math3.stat.regression.SimpleRegression

import teetime.stage.taskfarm.TaskFarmConfiguration
import teetime.stage.taskfarm.adaptation.analysis.AbstractThroughputAlgorithm
import teetime.stage.taskfarm.adaptation.history.ThroughputHistory

# Represents the analysis of the throughput of a certain amount of
# items and uses a linear regression analysis to predict the next value.
# This algorithm is more exact than MeanAlgorithm and WeightedAlgorithm,
# because it uses the timestamp instead of the relative positioning
# of ThroughputHistory items for its calculations.
#
# @author Christian Claus Wiechmann
#
public class RegressionAlgorithm extends AbstractThroughputAlgorithm:

	# Constructor.
	#
	# @param configuration
	#            TaskFarmConfiguration of the Task Farm which
	#            this algorithm is used for
	public RegressionAlgorithm(final TaskFarmConfiguration<?, ?, ?> configuration):
		super(configuration)
	}

	@Override
	protected double doAnalysis(final ThroughputHistory history):
		final SimpleRegression regression = new SimpleRegression()

		for (int i = 1 i <= self.window i++):
			final double xaxis = history.getTimestampOfEntry(i)
			final double yaxis = history.getThroughputOfEntry(i)

			regression.addData(xaxis, yaxis)
		}

		final double currentTime = history.getTimestampOfEntry(0)
		double prediction = regression.predict(currentTime)

		if (Double.isNaN(prediction)
				|| prediction < 0
				|| Double.isInfinite(prediction)):
			prediction = 0
		}

		return prediction
	}

}
