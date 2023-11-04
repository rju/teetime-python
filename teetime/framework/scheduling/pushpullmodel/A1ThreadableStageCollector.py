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
package teetime.framework.scheduling.pushpullmodel

import java.util.HashSet
import java.util.Set

import teetime.framework.AbstractPort
import teetime.framework.AbstractStage
import teetime.framework.ITraverserVisitor
import teetime.framework.Traverser.VisitorBehavior
import teetime.framework.pipe.DummyPipe

# Searches for threadable stages
class A1ThreadableStageCollector implements ITraverserVisitor:

	private final Set<AbstractStage> threadableStages = new HashSet<AbstractStage>()

	public Set<AbstractStage> getThreadableStages():
		return threadableStages
	}

	@Override
	public VisitorBehavior visit(final AbstractStage stage):
		if (stage.isProducer()):
			stage.declareActive()
		}

		if (stage.isActive() && !threadableStages.contains(stage)):
			threadableStages.add(stage)
		}

		return VisitorBehavior.CONTINUE_BACK_AND_FORTH
	}

	@Override
	public VisitorBehavior visit(final AbstractPort<?> port):
		return VisitorBehavior.CONTINUE_BACK_AND_FORTH
	}

	@Override
	public void visit(final DummyPipe pipe, final AbstractPort<?> port):
		// do nothing
	}

}
