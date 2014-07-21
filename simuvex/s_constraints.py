#!/usr/bin/env python

from .s_state import SimStatePlugin

import logging
l = logging.getLogger("simuvex.constraints")


class SimConstraints(SimStatePlugin):
	def __init__(self, solver=None):
		SimStatePlugin.__init__(self)
		self._stored_solver = solver

	@property
	def _solver(self):
		if self._stored_solver is not None:
			return self._stored_solver

		if o.CONSTRAINT_SETS in self.state.options:
			self._stored_solver = self.state.claripy.composite_solver()
		else:
			self._stored_solver = self.state.claripy.solver()
		return self._stored_solver

	#
	# Various passthroughs
	#

	def add(self, *constraints): return self._solver.add(*constraints)
	def satisfiable(self): return self._solver.satisfiable()
	def check(self): return self._solver.check()
	def downsize(self): return self._solver.downsize()
	def eval(self, *args, **kwargs): return self._solver.eval(*args, **kwargs)
	def max(self, *args, **kwargs): return self._solver.max(*args, **kwargs)
	def min(self, *args, **kwargs): return self._solver.min(*args, **kwargs)
	def solution(self, *args, **kwargs): return self._solver.solution(*args, **kwargs)

	def simplify(self):
		if o.SPLIT_CONSTRAINTS in self.state.options and o.CONSTRAINT_SETS in self.state.options:
			return self._solver.simplify(split=True)
		else: return self._solver.simplify()


	#
	# Branching stuff
	#

	def copy(self):
		return SimConstraints(self._solver.branch())

	def merge(self, others, merge_flag, flag_values): # pylint: disable=W0613


		#import ipdb; ipdb.set_trace()

		self._stored_solver = self._solver.merge([ oc._solver for oc in others ], merge_flag, flag_values)
		#import ipdb; ipdb.set_trace()
		return [ ]

SimStatePlugin.register_default('constraints', SimConstraints)
import simuvex.s_options as o
