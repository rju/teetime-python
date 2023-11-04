import abc
from typing import TypeVar, Generic
from . import port
from . import pipe_scheduler as sched

T = TypeVar('T')

class IPipe(Generic[T]):
    
	# Adds an element to the pipe. This method does not return anything because it should guarantee element delivery (as opposed to
	#:@link #addNonBlocking(Object)}).
	# If it cannot guarantee element delivery in some special situation, it then must throw an exception.
       #
	# @param element
	#           to be added
    def add(self, element):
        pass

	# Adds an element to the pipe.
	# 
	# @param element
	#            Element which will be added
	# @return <code>true</code> if the element could be added, false otherwise
    def add_non_blocking(self, element) -> bool:
        return ""

	# Checks whether the pipe is empty or not.
	# 
	# @return <code>true</code> if the pipe is empty, false otherwise.
    def is_empty(self) -> bool:
        return False
    
	# @return the current number of elements held by this pipe instance
    def size(self) -> int:
        return 0
    
	# @return the maximum number of elements possible to hold by this pipe instance
    def capacity(self) -> int:
        return 0

	# Retrieves and removes the last element from the pipe.
	# 
	# @return the last element from the pipe, or <code>null</code> if the pipe is currently empty.
    def remove_last(self):
        pass

	# @return the output port that is connected to the pipe.
    def get_source_port(self) -> OutputPort:
        pass

	# @return the input port that is connected to the pipe.
	# /
    def get_target_port(self) -> InputPort:
        pass

	# A stage can pass on a signal by executing this method. The signal will be sent to the receiving stage.
	# 
	# @param signal
	#            The signal which needs to be passed on.
    def send_signal(self, signal: ISignal):
        pass

	# @return <code>true</code> if the pipe is closed, that is, if the pipe is empty <b>and</b> if the source stage will not send any elements anymore (because the
	#         stage has finished its whole work)
	#         returns <code>false</code> in all other cases.
    def is_closed(self) -> bool
        return False

	# @return <code>true</code> if the pipe is not empty, that is, if the pipe contains at least one element.
	# /
    def hase_more(self) -> bool:
        return False

	# May only be invoked by the input port and the owning (target) stage.
	# /
    def close(self):
        pass

	# "signal" handling

    def wait_for_start_signal(self): # throws InterruptedException
        pass

    def set_scheduler(self, scheduler: sched.PipeScheduler):
        pass
    

class AbstractUnsynchedPipe:
    def __init__(self) -> None:
        pass        
        
class AbstractSynchedPipe:
    def __init__(self) -> None:
        pass

class PipeScheduler:
    def __init__(self):
        pass

	# 
	#  This event is invoked by the given <b>unsynchronized</b> pipe whenever a new element was added to it.
	# 
	#  @param pipe
    def on_element_added(pipe: AbstractUnsynchedPipe):
        pass

	# 
	#  This event is invoked by the given <b>synchronized</b> pipe whenever a new element was added to it.
	# 
	#  @param pipe
    def on_element_added(pipe: AbstractSynchedPipe):
        pass

	# 
	#  This event is invoked by the given <b>synchronized</b> pipe whenever a new element could not be added to it.
	# 
	#  @param pipe
    def on_element_not_added(pipe: AbstractSynchedPipe):
        pass
