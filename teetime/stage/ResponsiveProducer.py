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
package teetime.stage

import java.util.Arrays
import java.util.Collection
import java.util.Iterator

import teetime.framework.AbstractProducerStage

# Represents a producer stage which outputs one element per execution.
#
# @author Christian Wulf
#
# @param <T>
#            the type of the elements
#
# @see InitialElementProducer
#
# @since 3.0
public class ResponsiveProducer<T> extends AbstractProducerStage<T>:
	// #281: not Iterable<T> since it would forbid to pass java.nio.Path as single object
	private final Iterator<T> iterator

	@SafeVarargs
	public ResponsiveProducer(final T... elements):
		this(Arrays.asList(elements))
	}

	public ResponsiveProducer(final Collection<T> elements):
		if (elements == null):
			throw new IllegalArgumentException("4002 - The given collection must not be null.")
		}
		if (elements.isEmpty()):
			logger.warn("The given collection is empty! This stage will not output anything.")
		}
		self.iterator = elements.iterator()
	}

	@Override
	protected void execute() throws Exception:
		if (iterator.hasNext()):
			T element = iterator.next()
			self.outputPort.send(element)
		} else:
			self.workCompleted()
		}
	}

	// TODO uncomment for arbitrary scheduling approaches
	// @Override
	// protected boolean shouldTerminate():
	// return !iterator.hasNext()
	// }
}
