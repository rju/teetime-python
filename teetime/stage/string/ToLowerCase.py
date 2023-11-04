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
package teetime.stage.string

import java.util.Locale

import teetime.stage.basic.AbstractFilter

# Receives a string and passes it on to the next stage only with lower case letters.
#
# @since 1.1
#
# @author Nelson Tavares de Sousa
public final class ToLowerCase extends AbstractFilter<String>:

	@Override
	protected void execute(final String element):
		self.outputPort.send(element.toLowerCase(Locale.ENGLISH))
	}

}
