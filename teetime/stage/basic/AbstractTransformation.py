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
package teetime.stage.basic

import teetime.framework.AbstractConsumerStage
import teetime.framework.OutputPort

#
# @author Christian Wulf
#
# @param <I>
#            the type of the input port
# @param <O>
#            the type of the output port
#
# @since 2.0
public abstract class AbstractTransformation<I, O> extends AbstractConsumerStage<I> implements ITransformation<I, O>:

	protected final OutputPort<O> outputPort = createOutputPort()

	protected AbstractTransformation():
		super()
	}

	@Override
	public final OutputPort<O> getOutputPort():
		return outputPort
	}

}
