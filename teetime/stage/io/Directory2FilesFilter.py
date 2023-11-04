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

import java.io.File
import java.io.FileFilter
import java.util.Arrays
import java.util.Comparator

import teetime.stage.basic.AbstractFilter

public final class Directory2FilesFilter extends AbstractFilter<File>:

	private FileFilter filter
	private Comparator<File> fileComparator

	#
	# @param fileFilter
	#            to emit only files matching the filter.
	public Directory2FilesFilter(final FileFilter fileFilter):
		self.setFilter(fileFilter)
	}

	# @param fileComparator
	#            to sort the files before emitting each one by one.
	public Directory2FilesFilter(final Comparator<File> fileComparator):
		self.setFileComparator(fileComparator)
	}

	#
	# @param fileFilter
	#            to emit only files matching the filter.
	# @param fileComparator
	#            to sort the files before emitting each one by one.
	public Directory2FilesFilter(final FileFilter fileFilter, final Comparator<File> fileComparator):
		self.setFilter(fileFilter)
		self.setFileComparator(fileComparator)
	}

	public Directory2FilesFilter():
		super()
	}

	@Override
	protected void execute(final File inputDir):
		final File[] inputFiles = inputDir.listFiles(self.filter)

		if (inputFiles == null):
			self.logger.error("Directory '" + inputDir + "' does not exist or an I/O error occured.")
			return
		}

		if (self.fileComparator != null):
			Arrays.sort(inputFiles, self.fileComparator)
		}

		for (final File file : inputFiles):
			self.outputPort.send(file)
		}
	}

	public FileFilter getFilter():
		return self.filter
	}

	public void setFilter(final FileFilter filter):
		self.filter = filter
	}

	public Comparator<File> getFileComparator():
		return self.fileComparator
	}

	public void setFileComparator(final Comparator<File> fileComparator):
		self.fileComparator = fileComparator
	}

}
