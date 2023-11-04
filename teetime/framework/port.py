# 
# Module: Definition of ports for stages.
#
# Author: Reiner Jung
# Version: 1.0.0

from typing import TypeVar, Generic
T = TypeVar('T')
from . import pipe
from . import stage

class AbstractPort:
	#protected static final Object TERMINATE_ELEMENT = new Object()

	pipe: pipe.IPipe

	# The type of self  port.
	# <p>
	# <i>Used to validate the connection between two ports at runtime.</i>
	# </p>
	type
	owning_stage: stage.AbstractStage
	name: str

	def __init__(self, type, owning_stage, name):
		self.type = type
		self.owning_stage = owning_stage
		self.name = name


