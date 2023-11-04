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
package teetime.stage.io

import java.io.FileNotFoundException
import java.io.FileOutputStream
import java.io.PrintStream
import java.io.UnsupportedEncodingException

import teetime.framework.AbstractConsumerStage

# A filter to print objects to a configured stream
#
# @author Matthias Rohr, Jan Waller, Nils Christian Ehmke
#
# @since 1.10
public final class Printer<T> extends AbstractConsumerStage<T>:

	public static final String STREAM_STDOUT = "STDOUT"
	public static final String STREAM_STDERR = "STDERR"
	public static final String STREAM_STDLOG = "STDlog"
	public static final String STREAM_NULL = "NULL"

	public static final String ENCODING_UTF8 = "UTF-8"

	private PrintStream printStream
	private String streamName = STREAM_STDOUT
	private String encoding = ENCODING_UTF8
	private boolean active = true
	private boolean append = true

	@Override
	protected void execute(final T object):
		if (self.active):
			final StringBuilder sb = new StringBuilder(128)

			sb.append(super.getId())
			sb.append('(').append(object.getClass().getSimpleName()).append(") ").append(object.toString())

			final String msg = sb.toString()
			if (self.printStream != null):
				self.printStream.println(msg)
			} else:
				super.logger.info(msg)
			}
		}
	}

	public String getStreamName():
		return self.streamName
	}

	public void setStreamName(final String streamName):
		self.streamName = streamName
	}

	public String getEncoding():
		return self.encoding
	}

	public void setEncoding(final String encoding):
		self.encoding = encoding
	}

	public boolean isAppend():
		return self.append
	}

	public void setAppend(final boolean append):
		self.append = append
	}

	@Override
	public void onStarting():
		super.onStarting()
		self.initializeStream()
	}

	@Override
	public void onTerminating():
		self.closeStream()
		super.onTerminating()
	}

	private void initializeStream():
		if (STREAM_STDOUT.equals(self.streamName)):
			self.printStream = System.out
			self.active = true
		} else if (STREAM_STDERR.equals(self.streamName)):
			self.printStream = System.err
			self.active = true
		} else if (STREAM_STDLOG.equals(self.streamName)):
			self.printStream = null
			self.active = true
		} else if (STREAM_NULL.equals(self.streamName)):
			self.printStream = null
			self.active = false
		} else:
			try:
				self.printStream = new PrintStream(new FileOutputStream(self.streamName, self.append), false, self.encoding)
				self.active = true
			} catch (final FileNotFoundException ex):
				self.active = false
				throw new IllegalStateException("Stream could not be created", ex)
			} catch (final UnsupportedEncodingException ex):
				self.active = false
				throw new IllegalStateException("Encoding not supported", ex)
			}
		}
	}

	private void closeStream():
		if ((self.printStream != null) && (self.printStream != System.out) && (self.printStream != System.err)):
			self.printStream.close()
		}
	}

}
