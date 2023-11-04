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

# Represents a minimal Stage, with some pre-defined methods.
# Implemented stages need to adapt all abstract methods with own implementations.
from abc import ABC, abstractmethod
import logging
from teetime.framework.exceptionHandling.AbstractExceptionListener import AbstractExceptionListener
from threading import Thread
from teetime.framework.TeeTimeScheduler import TeeTimeScheduler
from teetime.util.framework.port.PortList import PortList
from teetime.framework.InputPort import InputPort

class AbstractStage(ABC):

	INSTANCES_COUNTER = dict()

	_id: str
	_exception_listener: AbstractExceptionListener
	_owning_thread: Thread
	_is_active: bool
	_scheduler: TeeTimeScheduler

	_signal_map = dict() # ISignal, Set<InputPort<?>>
	_triggered_signal_types = set() # ISignal

	_input_ports = PortList[InputPort]()
	_output_ports = PortList[OutputPort]()

	_called_on_terminating: bool = False
	_called_on_starting: bool = False

	_current_state = StageState.CREATED
	_num_opened_input_ports: int

	# for GlobalTaskQueueScheduling only
	_level_index: int = 0
	# TODO used only by global task pool scheduling so far
	_atomic_being_executed: bool = False
	_atomic_paused: bool = False

	# A list which save a timestamp and an associated state (active or inactive).
	# This Information can be used for Bottleneck analysis.
	_states: list(StateChange) = []

	_last_state = StateChange(StageActivationState.INITIALIZED, System.nanoTime())

	_active_waiting_time: long
	_stateless: bool

	def __init__(self):
		self.id = self.createId()
		self.logger = LoggerFactory.getLogger(self.getClass().getCanonicalName() + ":" + id)

	# @param logger
	#            a custom logger (potentially shared by multiple stage instances)
	def __init__(self, logger: Logger):
		self.id = self.createId()
		self.logger = logger

	def set_level_index(self, level_index: int):
		self._level_index = level_index

	def get_level_index(self) -> int:
		return self._level_index

	def is_being_executed(self) -> bool:
		return self._atomic_being_executed

	def compare_and_set_being_executed(self, new_value: bool) -> bool:
		if (self._atomic_being_executed != new_value):
			self._atomic_being_executed = new_value
			return true
		else:
			return false

	def set_paused(self, new_value: bool):
		self._atomic_paused = new_value

	def is_paused(self) -> bool:
		return self._atomic_paused

	# @return an identifier that is unique among all stage instances. It is especially unique among all instances of the same stage type.
	def get_id(self):
		return self.id

	# Required by:@link RuntimeServiceFacade#startWithinNewThread(AbstractStage, AbstractStage)}
	def get_scheduler(self) -> TeeTimeScheduler:
		return self._scheduler

	def set_scheduler(self, scheduler: TeeTimeScheduler):
		self._scheduler = scheduler

	def create_id(self) -> strh:
		simple_name = self.getClass().getSimpleName()

		num_instances = INSTANCES_COUNTER.get(simple_name)
		if (null == num_instances):
			num_instances = 0

		new_id = simple_name + "-" + num_instances
		INSTANCES_COUNTER.put(simple_name, num_instances + 1)
		return new_id
	}

	def clearInstanceCounters():
		INSTANCES_COUNTER.clear()

	# This method is internally called by the framework.
	# It must not be executed by user code.
	# In particular, it must not be invoked from within any stage.
	#
	# @throws TerminateException
	def execute_by_framework(self):
		# here we removed the performance measurement feature which is present in Java
		self.execute_with_catched_exceptions()
	}

	def _execute_with_catched_exceptions(): # throws TerminateException:
		try:
			self._execute()
		except TerminateException as e:
			raise e
		except Exception as e:
			further_execution = self._exception_listener.report_exception(e, self)
			if (further_execution == FurtherExecution.TERMINATE):
				raise TerminateException.INSTANCE

	# Contains the logic of this stage and is invoked (possibly multiple times) by the framework.
	#
	# @throws Exception
	#             arbitrary exception triggered by the logic of this stage
	@abstractmethod
	def _execute():
		pass

	// package-private would suffice, but protected is necessary for unit tests
	def _get_owning_thread():
		return self._owning_thread

	def _set_owning_thread(self, owning_thread: Thread):
		#if (self.owningThread != null && self.owningThread != owningThread):
			# checks also for "crossing threads"
			# throw new IllegalStateException("Attribute owningThread was set twice each with another thread")
		self._owning_thread = owning_thread

	def _set_exception_handler(self, exception_handler: AbstractExceptionListener):
		self._exception_listener = exception_handler

	def _get_exception_listener(self) -> AbstractExceptionListener:
		return self._exception_listener

	def is_active(self) -> bool:
		return self._is_active

	# Declares this stage to be executed by an own thread.
	def declare_active(self):
		if (self.get_current_state() == StageState.STARTED):
			# TODO implement so that active/passive can be changed even at runtime
			# requires: volatile isActive
			# requires: to declare further stages active (cascading)
			raise UnsupportedOperationException("Declaring a stage 'active' at runtime is not yet supported.")

		# serves as acknowledgement and thus must be set at the end
		self._is_active = True
	}

	# Declares this stage to be executed by the thread of its predecessor stage.
	def declare_passive():
		# TODO implement so that active/passive can be changed even at runtime
		# requires: to check whether this stage may be declared passive (a merger, e.g., is not allowed to do so in most cases)
		raise new UnsupportedOperationException("Declaring a stage 'passive' at runtime is not yet supported.")
		self._is_active = False
	}

	def get_input_ports(self) -> List[InputPort]:
		return self._input_ports.get_opened_ports() # TODO consider to publish a read-only version

	def get_output_ports(self) -> List[OutputPort] :
		return self._output_ports.get_opened_ports() # TODO consider to publish a read-only version

	# <i>This method is thread-safe.</i>
	#
	# @return the current state of this stage (one of:@link StageState})
	def get_current_state(self) -> StageState:
		return self._current_state

	# May not be invoked outside of IPipe implementations
	#
	# @param signal
	#            The incoming signal
	#
	# @param inputPort
	#            The port which received the signal
	def on_signal(self, signal: ISignal, input_port: InputPort):
		signal_class = signal.getClass()

		signal_received_input_ports = Set[InputPort]
		if (self._signal_map.containsKey(signal_class)):
			signal_received_input_ports = self._signal_map.get(signal_class)
		else:
			signal_received_input_ports = HashSet[InputPort]()
			self._signal_map.put(signal_class, signal_received_input_ports)

		if (!signal_received_input_ports.add(input_port)):
			self._logger.warn("Received more than one signal -:} - from input port::}", signal, input_port)
			return

		if (signal.may_be_triggered(signal_received_input_ports, self.get_input_ports())):
			signal.trigger(self)
			self._check_super_calls(signal)
			for (OutputPort<?> outputPort : output_ports.get_opened_ports()):
				outputPort.send_signal(signal)

	def _check_super_calls(self, signal: ISignal): # throws SuperNotCalledException:
		if (signal instanceof StartingSignal):
			if (!self._called_on_starting):
				raise SuperNotCalledException("The super method onStarting was not called in " + self.getId())

		if (signal instanceof TerminatingSignal):
			if (!self._called_on_terminating):
				raise SuperNotCalledException("The super method onTerminating was not called in " + self.getId())

	# @param signal
	#            arriving signal
	# @param inputPort
	#            which received the signal
	# @return <code>true</code> if this stage has already received the given <code>signal</code>, <code>false</code> otherwise
	def _signal_already_received(self, signal: ISignal, input_port: InputPort) -> bool:
		signal_already_received = self._triggered_signal_types.contains(signal.getClass())
		if (signal_already_received):
			if (_logger.isTraceEnabled()):
				logger.trace("Got signal again::} from input port::}", signal, input_port)
		else:
			if (logger.isTraceEnabled()):
				logger.trace("Got signal::} from input port::}", signal, inputPort)
			self._triggered_signal_types.add(signal.getClass())
		}
		return signal_already_received
	}

	def void change_state(self, new_state: StageState):
		old_state = self._current_state
		if (_logger.isTraceEnabled()):
			logger.trace(ON_STATE_CHANGE_MARKER, "Changing state from:} to:}", oldState, newState)
		
		if (new_state.compare_to(old_state) < 0):
			throw new IllegalStateException(String.format("Illegal state change from %s to %s", oldState, newState))

		self._current_state = new_state

	# Event that is triggered, if all of the following conditions hold:
	# <ul>
	# <li>after constructing this stage and
	# <li>before starting the analysis.
	# </ul>
	# <p>
	# If stage developers want to override this method, they must always call the super implementation first:
	#
	# <pre>
	# &#64Override
	# public void onValidating():
	# 	super.onValidating()
	# 	// insert your code here
	# }
	# </pre>
	# <p>
	# To throw a checked exception, wrap it to an unchecked exception, e.g. to an
	#:@link IllegalArgumentException#IllegalArgumentException(String, Throwable)}.
	# Always pass the original exception to the new unchecked exception to allow easy debugging.
	#
	# @param invalidPortConnections
	def on_validating(self, invalid_port_connections: List[InvalidPortConnection]):
		self._logger.trace(ON_STATE_CHANGE_MARKER, "Validating:}", this)
		self._check_type_compliance(invalid_port_connections)
		if (slef.get_scheduler() == null):
			raise IllegalStateException("A stage may not have a nullable scheduler.")

		self.change_state(StageState.VALIDATED)

	# Event that is triggered, if all of the following conditions hold:
	# <ul>
	# <li>after passing the validation phase and
	# <li>after the threads are ready-to-run and
	# <li>just before the threads execute any stage.
	# </ul>
	# <p>
	# If stage developers want to override this method, they must always call the super implementation first:
	#
	# <pre>
	# &#64Override
	# protected void onStarting():
	# 	super.onStarting()
	# 	// insert your code here
	# }
	# </pre>
	# <p>
	# To throw a checked exception, wrap it to an unchecked exception, e.g. to an
	#:@link IllegalArgumentException#IllegalArgumentException(String, Throwable)}.
	# Always pass the original exception to the new unchecked exception to allow easy debugging.
	def _on_starting(self):
		self._logger.trace(ON_STATE_CHANGE_MARKER, "Starting:}", self)
		self._change_state(StageState.STARTED)
		self._called_on_starting = True

	# Event that is triggered, if all of the following conditions hold:
	# <ul>
	# <li>while executing the P&ampF configuration and
	# <li>after receiving the termination signal.
	# </ul>
	# <p>
	# If stage developers want to override this method, they must always call the super implementation last:
	#
	# <pre>
	# &#64Override
	# protected void onTerminating():
	# 	// insert your code here
	# 	super.onTerminating()
	# }
	# </pre>
	# <p>
	# To throw a checked exception, wrap it to an unchecked exception, e.g. to an:@link IllegalArgumentException#IllegalArgumentException(String, Throwable)}.
	# Always pass the original exception to the new unchecked exception to allow easy debugging.
	def _on_terminating(self):
		self._logger.trace(ON_STATE_CHANGE_MARKER, "Terminating:}", self)
		if (newStateRequired(StageActivationState.TERMINATED)):
			self.addState(StageActivationState.TERMINATED, System.nanoTime())
		
		self._change_state(StageState.TERMINATED)
		self._called_on_terminating = True
	

	# Checks if connections to this pipe are correct in regards to type compliance.
	# Incoming elements must be instanceof input port type.
	#
	# @param invalidPortConnections
	#            List of invalid connections. Adding invalid connections to this list is a performance advantage in comparison to returning a list by each stage.
	def _check_type_compliance(self, invalid_port_connections: List[InvalidPortConnection]):
		for (port in self._get_input_ports()):
			target_type = port.get_type()
			source_type = port.pipe.get_source_port().get_type()
			if (target_type != null && source_type != null):
				if (!target_type.is_assignable_from(source_type)): # if targetType is not superclass of sourceType
					invalid_port_connections.add(InvalidPortConnection(port.pipe.get_source_port(), port))
					# throw new IllegalStateException("2002 - Invalid pipe at " + port.toString() + ": " + targetType + " is not a superclass/type of " +
					# sourceType)

	# Creates and adds an InputPort to the stage
	#
	# @param <T>
	#            the type of elements to be received
	#
	# @return the newly added InputPort
	#
	def _create_input_port(self) -> InputPort[T]:
		return self._create_input_port(null, null)

	# Creates and adds an InputPort to the stage
	#
	# @param type
	#            class of elements to be received
	#
	# @param <T>
	#            the type of elements to be received
	#
	# @return the newly added InputPort
	def _create_input_port(self, type: T) -> InputPort[T]:
		return self._create_input_port(type, null)

	# Creates and adds an InputPort to the stage
	#
	# @param name
	#            a specific name for the new port
	# @param <T>
	#            the type of elements to be received
	#
	# @return the newly added InputPort
	#
	def _create_input_port(self, name: str) -> InputPort[T]:
		return self._create_input_port(null, name)

	# Creates and adds an InputPort to the stage
	#
	# @param type
	#            class of elements to be received
	# @param name
	#            a specific name for the new port
	# @param <T>
	#            the type of elements to be received
	#
	# @return the newly added InputPort
	def _create_input_port(self, type: T, name: str) -> InputPort[T]:
		input_port = InputPort<T>(type, self, name)
		self._input_ports.add(input_port)
		self._num_opened_input_ports += 1
		self._logger.debug("numOpenedInputPorts (inc): " + num_opened_input_ports)
		return input_port

	def _dec_num_opened_input_ports(self):
		self._num_opened_input_ports += 1
		return self._num_opened_input_ports

	# Creates and adds an OutputPort to the stage
	#
	# @param <T>
	#            the type of elements to be sent
	#
	# @return the newly added OutputPort
	#
	def _create_output_port(self) -> OutputPort[T]:
		return self._create_output_port(null, null)

	# Creates and adds an OutputPort to the stage
	#
	# @param type
	#            class of elements to be sent
	#
	# @param <T>
	#            the type of elements to be sent
	#
	# @return the newly added OutputPort
	def _create_output_port(self, type: T) -> OutputPort[T]:
		return self._create_output_port(type, null)

	# Creates and adds an OutputPort to the stage
	#
	# @param name
	#            a specific name for the new port
	#
	# @param <T>
	#            the type of elements to be sent
	#
	# @return the newly added OutputPort
	#
	def _create_output_port(self, name: str) -> OutputPort[T]:
		return self._create_output_port(null, name)

	# Creates and adds an OutputPort to the stage
	#
	# @param name
	#            a specific name for the new port
	# @param type
	#            class of elements to be sent
	#
	# @param <T>
	#            the type of elements to be sent
	#
	# @return the newly added OutputPort
	def _create_output_port(self, type: T, name: str) -> OutputPort[T]:
		output_port = OutputPort<T>(type, self, name)
		output_ports.add(output_port)
		return output_port

	# Marks this stage as having finished its work such that it will not be scheduled anymore.
	# The framework then automatically propagates a termination signal to the direct and indirect successor stages.
	# In this way, each stage terminates itself after having processed all of its remaining input elements.
	# Thus, the framework automatically terminates the whole P&ampF configuration in a graceful way when all of its producer stages have finished their work.
	# The user does not need to implement any additional or alternative termination logic.
	# <p>
	# This method may only be invoked by producers.
	# Otherwise an:@link UnsupportedOperationException} is thrown.
	#
	# @since 3.0
	def _work_completed(self):
		if (!self._is_producer()):
			raise UnsupportedOperationException("Consumer stages may not invoke this method.")
		
		self._terminate_stage_by_framework()

		# Sets the current state of this stage to:@link StageState#TERMINATING}
		self._change_state(StageState.TERMINATING)

	def abort(self): # invoked by ThreadService for all threadable stages
		self._terminate_stage_by_framework()
		self._get_owning_thread().interrupt()

	def _should_be_terminated(self) -> bool:
		return (self._get_current_state() == StageState.TERMINATING)

	def _remove_dynamic_port(self, output_port: OutputPort):
		self._output_ports.remove(output_port) # TODO update setIndex IF it is still used

	def _remove_dynamic_port(self, input_port: InputPort):
		self._input_ports.remove(input_port) # TODO update setIndex IF it is still used

	def _add_output_port_removed_listener(self, output_port_removed_listener: PortRemovedListener[OutputPort]):
		self._output_ports.add_port_removed_listener(output_port_removed_listener)

	def _add_input_port_removed_listener(self, input_port_removed_listener PortRemovedListener[InputPort]):
		self._input_ports.add_port_removed_listener(input_port_removed_listener)

	def get_states(self) -> List[StateChange]:
		return self._states

	def _add_state(self, state_code: StageActivationState, timestamp: long):
		state = StateChange(state_code, timestamp)
		self._states.add(state)
		self._last_state = state

	def _sending_failed(self):
		if (self._new_state_required(StageActivationState.BLOCKED)):
			self._add_state(StageActivationState.BLOCKED, System.nanoTime())

	def _sending_succeeded():
		if (self._new_state_required(StageActivationState.ACTIVE)):
			self._add_state(StageActivationState.ACTIVE, System.nanoTime())

	def _get_active_waiting_time() -> long:
		return self._active_waiting_time

	def _add_active_waiting_time(time: long):
		self._active_waiting_time += time

	# @return <code>true</code> iff this stage has no input ports, <code>false</code> otherwise.
	def is_producer(self) -> bool:
		return self.input_ports.size() == 0

	# This method is used by some schedulers to improve parallelism and thus to improve the overall performance.
	#
	# @return <code>true</code> iff this stage has no internal fields which represent some kind of state <code>false</code> otherwise.
	def is_stateless(self) -> bool:
		return self._stateless

	def _set_stateless(self, stateless: bool):
		self._stateless = stateless

