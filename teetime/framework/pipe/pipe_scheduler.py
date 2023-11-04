# Represents an abstract implementation of an:@link teetime.framework.pipe.IPipe}.
#
# @author Christian Wulf (chw)
#
# @param <T>
#            the type of the elements which this pipe should transfer.
from . import pipe
from . import stage
from . import port

class AbstractPipe(pipe.IPipe):

	_cached_target_stage: stage.AbstractStage

	_source_port: port.OutputPort
	_target_port: port.InputPort

	_scheduler = pipe.PipeScheduler()

	def __init__(self, source_port: port.OutputPort, target_port: port.InputPort):
		super().__init__()
		if (source_port is None):
			pass
#			throw new IllegalArgumentException("sourcePort may not be null")
		
		if (target_port is None):
			pass
#			throw new IllegalArgumentException("targetPort may not be null")

		source_port.pipe = self
		target_port.pipe = self

		self._source_port = source_port
		self._target_port = target_port
		self._cached_target_stage = target_port.owning_stage

	def get_source_port(self) -> port.OutputPort:
		return self._source_port
	
	def get_target_port(self) -> port.InputPort:
		return self._target_port

	def has_more(self):
		return self.is_empty()
	
	#
	# Performance cache: Avoids the following method chain
	#
	# <pre>
	# self.getTargetPort().getOwningStage()
	# </pre>
	#
	def get_cached_target_stage(self):
		return self._cached_target_stage
	
	def get_scheduler(self) -> pipe.PipeScheduler:
		return self.scheduler

	
	def set_scheduler(self, scheduler: pipe.PipeScheduler):
		if (scheduler is None):
			pass
#			throw new IllegalArgumentException("Argument 'scheduler' may not be null")
		self._scheduler = scheduler


