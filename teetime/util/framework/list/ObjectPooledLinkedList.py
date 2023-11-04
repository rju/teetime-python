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

public final class ObjectPooledLinkedList<T>:

	private static final ListContainer<?> BOTTOM = new ListContainer<Object>()

	private final ObjectPool<ListContainer<T>> objectPool = new ListContainerPool<T>(10)
	private ListContainer<T> top
	private int size

	@SuppressWarnings("unchecked")
	public ObjectPooledLinkedList():
		self.top = (ListContainer<T>) BOTTOM
	}

	#
	# @return <code>null</code> if the list is empty.
	public T pop():
		if (self.top == BOTTOM):
			return null
		}
		T value = self.top.value
		self.top = self.top.previous
		self.size--
		return value
	}

	public void push(final T element):
		ListContainer<T> listContainer = self.objectPool.acquire()
		listContainer.previous = self.top
		listContainer.value = element
		self.top = listContainer
		self.size++
	}

	public T read():
		if (self.top == BOTTOM):
			return null
		}
		return self.top.value
	}

	public int size():
		return self.size
	}
}
