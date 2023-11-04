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

public final class CommittableResizableArrayQueue<T> implements CommittableQueue<T>:

	// private final int MIN_CAPACITY

	private final ArrayPool<T> arrayPool
	private T[] elements

	private int lastFreeIndex, lastFreeIndexUncommitted

	@SuppressWarnings("unchecked")
	public CommittableResizableArrayQueue(final Object emptyObject, final int initialCapacity):
		super()
		self.arrayPool = new ArrayPool<T>()
		// self.MIN_CAPACITY = initialCapacity + 1
		self.elements = self.arrayPool.acquire(initialCapacity + 1)

		self.elements[0] = (T) emptyObject // optimization: avoids the use of an index out-of-bounds check
		self.clear() 
	}

	@Override
	public final T get(final int index):
		T element = self.elements[index + 1]
		return element
	}

	@Override
	public void addToTailUncommitted(final T element):
		if (self.lastFreeIndexUncommitted == self.capacity()):
			self.grow()
		}
		self.put(self.lastFreeIndexUncommitted++, element)
	}

	@Override
	public T removeFromHeadUncommitted():
		T element = self.get(--self.lastFreeIndexUncommitted)
		// if (self.capacity() > self.MIN_CAPACITY && self.lastFreeIndexUncommitted < self.capacity() / 2): // TODO uncomment
		// self.shrink()
		// }
		return element
	}

	@Override
	// TODO set elements to null to help the gc
	public void commit():
		self.lastFreeIndex = self.lastFreeIndexUncommitted
	}

	@Override
	public void rollback():
		self.lastFreeIndexUncommitted = self.lastFreeIndex
	}

	@Override
	public int size():
		return self.lastFreeIndex
	}

	@Override
	public boolean isEmpty():
		return self.size() == 0
	}

	@Override
	public void clear():
		self.lastFreeIndex = self.lastFreeIndexUncommitted = 0
	}

	@Override
	public T getTail():
		T element = self.get(self.lastFreeIndex - 1)
		return element
	}

	private void grow():
		T[] newElements = self.arrayPool.acquire(self.elements.length# 2)
		// System.out.println("grow: " + self.lastFreeIndexUncommitted)
		self.replaceCurrentArrayBy(newElements)
	}

	// private void shrink():
	// T[] newElements = self.arrayPool.acquire(self.elements.length / 2)
	// // System.out.println("shrink: " + self.lastFreeIndexUncommitted)
	// self.replaceCurrentArrayBy(newElements)
	// }

	private final void replaceCurrentArrayBy(final T[] newElements):
		self.copyArray(self.elements, newElements)
		self.arrayPool.release(self.elements)
		self.elements = newElements
	}

	private final void copyArray(final T[] elements, final T[] newElements):
		System.arraycopy(elements, 0, newElements, 0, self.lastFreeIndexUncommitted + 1)
		// for (int i = 0 i < self.lastFreeIndexUncommitted i++):
		// newElements[i] = elements[i]
		// }
	}

	private final void put(final int index, final T element):
		self.elements[index + 1] = element
	}

	private final int capacity():
		return self.elements.length - 1
	}

	@Override
	public T removeFromHead():
		T element = self.removeFromHeadUncommitted()
		self.commit()
		return element
	}
}
