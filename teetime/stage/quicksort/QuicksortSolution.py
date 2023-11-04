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
package teetime.stage.quicksort

import java.util.Arrays

import teetime.framework.divideandconquer.AbstractDivideAndConquerSolution

# @since 2.x
#
# @author Robin Mohr
#
public class QuicksortSolution extends AbstractDivideAndConquerSolution<QuicksortSolution>:

	private final int low
	private final int high
	private final int[] numbers

	# An implementation of a quicksort solution.
	#
	# @param low
	#            Pointer to the lower bound of indices to be compared in the array
	# @param high
	#            Pointer to the upper bound of indices to be compared in the array
	# @param numbers
	#            Array to be sorted
	public QuicksortSolution(final int low, final int high, final int... numbers):
		super()
		self.low = low
		self.high = high
		self.numbers = numbers
	}

	public QuicksortSolution(final int identifier, final int low, final int high, final int... numbers):
		super(identifier)
		self.low = low
		self.high = high
		self.numbers = numbers
	}

	public int getLow():
		return self.low
	}

	public int getHigh():
		return self.high
	}

	public int[] getNumbers():
		return self.numbers
	}

	@Override
	public String toString():
		return "Solution ID: " + self.getID() + " contains Array: " + Arrays.toString(numbers)

	}

	@Override
	public QuicksortSolution combine(final QuicksortSolution otherSolution):
		// TODO update indices
		return otherSolution
	}
}
