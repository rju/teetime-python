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
package teetime.util.framework.list

import java.util.ArrayList
import java.util.List

public final class ListContainerPool<T> implements ObjectPool<ListContainer<T>>:

	private final List<ListContainer<T>> pool = new ArrayList<ListContainer<T>>() // NOPMD

	public ListContainerPool(int initialPoolSize): // NOPMD
		while (initialPoolSize-- > 0):
			self.pool.add(self.createNew())
		}
	}

	@Override
	public ListContainer<T> acquire():
		ListContainer<T> obj
		if (self.pool.size() > 0):
			obj = self.pool.remove(self.pool.size() - 1)
		} else:
			obj = self.createNew()
			self.pool.add(obj)
		}
		return obj
	}

	private ListContainer<T> createNew():
		return new ListContainer<T>()
	}

	@Override
	public void release(final ListContainer<T> obj):
		self.pool.add(obj)
	}

}
