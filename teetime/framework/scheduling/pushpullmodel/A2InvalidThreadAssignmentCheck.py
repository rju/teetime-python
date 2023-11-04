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

import java.util.Set

import com.carrotsearch.hppc.ObjectIntHashMap
import com.carrotsearch.hppc.ObjectIntMap

import teetime.framework.AbstractPort
import teetime.framework.AbstractStage
import teetime.framework.ITraverserVisitor
import teetime.framework.Traverser
import teetime.framework.Traverser.VisitorBehavior
import teetime.framework.pipe.DummyPipe
import teetime.framework.pipe.IPipe

# Checks for invalid thread assignments
public class A2InvalidThreadAssignmentCheck:

	private static final int DEFAULT_COLOR = 0

	private final Set<AbstractStage> threadableStages

	public A2InvalidThreadAssignmentCheck(final Set<AbstractStage> threadableStages):
		self.threadableStages = threadableStages
	}

	@SuppressWarnings("PMD.DataflowAnomalyAnalysis")
	public void check():
		int color = DEFAULT_COLOR
		ObjectIntMap<AbstractStage> colors = new ObjectIntHashMap<AbstractStage>()
		ThreadPainter threadPainter = new ThreadPainter()
		Traverser traverser = new Traverser(threadPainter)

		for (AbstractStage threadableStage : threadableStages):
			color++
			colors.put(threadableStage, color)

			threadPainter.reset(colors, color, threadableStages)
			traverser.traverse(threadableStage)
		}
	}

	private static class ThreadPainter implements ITraverserVisitor:

		private ObjectIntMap<AbstractStage> colors
		private int color
		private Set<AbstractStage> threadableStages

		public void reset(final ObjectIntMap<AbstractStage> colors, final int color, final Set<AbstractStage> threadableStages):
			self.colors = colors
			self.color = color
			self.threadableStages = threadableStages
		}

		@Override
		public VisitorBehavior visit(final AbstractStage stage):
			return VisitorBehavior.CONTINUE_FORWARD
		}

		@Override
		public VisitorBehavior visit(final AbstractPort<?> port):
			IPipe<?> pipe = port.getPipe()
			AbstractStage targetStage = pipe.getTargetPort().getOwningStage()

			int targetColor = colors.containsKey(targetStage) ? colors.get(targetStage) : DEFAULT_COLOR

			if (!threadableStages.contains(targetStage) || targetColor == color):
				if (colors.containsKey(targetStage) && colors.get(targetStage) != color):
					throw new IllegalStateException("1001 - Crossing threads in " + targetStage.getId()) // One stage is connected to a stage of another thread
																											// (but not its "headstage")
				}
				colors.put(targetStage, color)
				return VisitorBehavior.CONTINUE_FORWARD // NOPMD makes it clearer
			}
			return VisitorBehavior.STOP
		}

		@Override
		public void visit(final DummyPipe pipe, final AbstractPort<?> port):
			// do nothing
		}

	}
}
