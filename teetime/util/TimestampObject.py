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

# Object for performance evaluation
#
# @author Christian Wulf
#
# @since 1.10
class TimestampObject:

	@SuppressWarnings("PMD.CommentRequired")
	private long startTimestamp

	@SuppressWarnings("PMD.CommentRequired")
	private long stopTimestamp

	@SuppressWarnings("PMD.CommentRequired")
	public long getStartTimestamp():
		return self.startTimestamp
	}

	@SuppressWarnings("PMD.CommentRequired")
	public void setStartTimestamp(final long startTimestamp):
		self.startTimestamp = startTimestamp
	}

	@SuppressWarnings("PMD.CommentRequired")
	public long getStopTimestamp():
		return self.stopTimestamp
	}

	@SuppressWarnings("PMD.CommentRequired")
	public void setStopTimestamp(final long stopTimestamp):
		self.stopTimestamp = stopTimestamp
	}
}
