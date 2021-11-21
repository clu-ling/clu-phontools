from __future__ import annotations
from .actions import Actions
from .graph import Edge, Graph
from .constraints import Constraints
from .queue import Queue
from .stack import Stack
from .symbols import *
from dataclasses import dataclass, field
from typing import Callable, Optional, Text

__all__ = ["State"]

# type alias for methods that perform actions
ActionFunc = Callable[[], Optional["State"]]


@dataclass
class State:
    """ """

    stack: Stack
    gold_queue: Queue
    transcribed_queue: Queue
    # during training, this is not None
    gold_graph: Optional[Graph]
    current_graph: Graph
    # keep track of prior actions. 
    # last item is more recent.
    prior_actions: List[Actions] = field(default_factory=list) 

    def copy(
        self,
        stack: Optional[Stack] = None,
        gold_queue: Optional[Queue] = None,
        transcribed_queue: Optional[Queue] = None,
        gold_graph: Optional[Graph] = None,
        current_graph: Optional[Graph] = None,
        prior_actions: Optional[List[prior_actions]] = None,
    ) -> State:
        """Return a copy of the current state with one or more attributes modified"""
        return State(
            stack=stack if stack is not None else self.stack,
            gold_queue=gold_queue if gold_queue is not None else self.gold_queue,
            transcribed_queue=transcribed_queue
            if transcribed_queue is not None
            else self.transcribed_queue,
            gold_graph=gold_graph if gold_graph is not None else self.gold_graph,
            current_graph=current_graph
            if current_graph is not None
            else self.current_graph,
            prior_actions=prior_actions if prior_actions is not None else self.prior_actions,
        )

    def last_action(self) -> Optional[Actions]:
        """Easily access the last action applied"""
        return None if len(self.prior_actions) == 0 else self.prior_actions[-1]

    @property
    def actions_map(self) -> Dict[Actions, ActionFunc]:
        return {
            Actions.ALIGN: self._perform_ALIGN,
            Actions.DELETION_PRESERVE_CHILD: self._perform_DELETION_PRESERVE_CHILD,
            Actions.DELETION_PRESERVE_PARENT: self._perform_DELETION_PRESERVE_PARENT,
            Actions.DISCARD: self._perform_DISCARD,
            Actions.INSERTION_PRESERVE_CHILD: self._perform_INSERTION_PRESERVE_CHILD,
            Actions.INSERTION_PRESERVE_PARENT: self._perform_INSERTION_PRESERVE_PARENT,
            Actions.SHIFT_G: self._perform_SHIFT_G,
            Actions.SHIFT_T: self._perform_SHIFT_T,
            Actions.STACK_SWAP: self._perform_STACK_SWAP,
            Actions.SUBSTITUTION: self._perform_SUBSTITUTION
        }

    def valid_actions(self) -> List[Actions]:
        """Determines valid actions"""
        return [
            action for action in self.actions_map.keys() if self.is_valid(action)
        ]

    def perform_action(self, action: Actions) -> Optional[State]:
        """Applies the provided action to the state"""
        actions_map = self.actions_map
        if action in actions_map:
            return actions_map[action]()
        raise NotImplementedError(f"Action {action} not recognized")

    def is_valid(self, action: Actions) -> bool:
        """Determines whether the provided action is valid"""
        res = self.perform_action(action)
        return False if not res else True

    def _generic_parent_child(self, action: Actions, preserve_child: bool, preserve_parent: bool) -> Optional[State]:
        """Creates an edge using the provided actions as a label between top two items of Stack (if present). 
        
        `edge.source` is whatever symbol originates from `TranscriptTypes.GOLD`. 
        
        action is valid iff Constraints.stack_top_two_different_sources().
        """
        ACTION = action
        # check if action is valid
        if not Constraints.stack_top_two_different_sources(self.stack):
            return None
        stack = self.stack.copy()
        s1 = stack.pop()
        s2 = stack.pop()
        # determine parent and child
        parent = s1 if s1.source == TranscriptTypes.GOLD else s2
        child = s1 if s1.source == TranscriptTypes.TRANSCRIPT else s2
        # optionally preserve parent and child (according to params)
        if preserve_parent:
          stack.push(parent)
        if preserve_child:
          stack.push(child)
        # add edge
        edge = Edge(source=parent, destination=child, label=ACTION)
        new_graph = Graph(edges=self.current_graph.edges + [edge])
        return self.copy(stack=stack, current_graph=new_graph, prior_actions=self.prior_actions + [ACTION])

    def _perform_ALIGN(self) -> Optional[State]:
        """Adds an ALIGN edge between top two items of Stack (if present).
        
        ALIGN is valid iff there are at least two items on the stack AND
        top two items on the stack have TRANSCRIPT and GOLD TranscriptTypes.
        """
        ACTION = Actions.ALIGN
        # check if action is valid
        if not Constraints.stack_top_two_different_sources(self.stack):
            return None
        stack = self.stack.copy()
        s1 = stack.pop()
        s2 = stack.pop()
        keep: Symbol = s1 if s1.source == TranscriptTypes.GOLD else s2
        drop: Symbol = s1 if s1.source == TranscriptTypes.TRANSCRIPT else s2
        # ALIGN must point from Transcript -> GOLD
        edge = Edge(source=drop, destination=keep, label=Actions.ALIGN)
        new_graph = Graph(edges=self.current_graph.edges + [edge])
        stack.push(keep)
        return self.copy(stack=stack, current_graph=new_graph, prior_actions=self.prior_actions + [ACTION])

    # FIXME: add tests
    def _perform_DISCARD(self) -> Optional[State]:
        """Discards top item on Stack (if present).
        """
        ACTION = Actions.DISCARD
        # check if action is valid
        # FIXME: is this the only condition? 
        # We shouldn't discard a non-NULL if it doesn't participate in an edge, right?
        if len(self.stack) > 0:
            return None
        stack = self.stack.copy()
        _ = stack.pop()
        # FIXME: do we want to add an edge?  It seems unnecessary
        return self.copy(stack=stack, prior_actions=self.prior_actions + [ACTION])

    def _perform_SHIFT_T(self) -> Optional[State]:
        """Shifts first item from transcribed_queue to top of stack"""
        ACTION = Actions.SHIFT_T
        # check if action is valid
        if len(self.transcribed_queue) == 0:
            return None
        stack = self.stack.copy()
        t_queue = self.transcribed_queue.copy()
        next_ps = t_queue.pop()
        stack.push(next_ps)
        return self.copy(stack=stack, transcribed_queue=t_queue, prior_actions=self.prior_actions + [ACTION])

    def _perform_SHIFT_G(self) -> Optional[State]:
        """Shifts first item from gold_queue to top of stack"""
        ACTION = Actions.SHIFT_G
        # check if action is valid
        if len(self.gold_queue) == 0:
            return None
        stack = self.stack.copy()
        g_queue = self.gold_queue.copy()
        next_ps = g_queue.pop()
        stack.push(next_ps)
        return self.copy(stack=stack, gold_queue=g_queue, prior_actions=self.prior_actions + [ACTION])

    def _perform_STACK_SWAP(self) -> Optional[State]:
        """Swaps the top two items on the stack.

        STACK_SWAP is valid iff 
        a) there are at least two items on the stack.
        b) the last action was not STACK_SWAP (avoid endless loops)
        """
        ACTION = Actions.STACK_SWAP
        # check if action is valid
        if (len(self.stack) < 2) and (self.last_action() is not Actions.STACK_SWAP):
            return None
        stack = self.stack.copy()
        s1 = stack.pop()
        s2 = stack.pop()
        for ps in [s2, s1]:
            stack.push(s2)
        return self.copy(stack=stack, prior_actions=self.prior_actions + [ACTION])

    # TODO: should there be only INSERTION and allow both to remain on stack?
    # that would require checking that current_graph doesn't already contain the edge
    # TODO: should INSERTION_* always point to a NULL in GOLD? if so
    # FIXME: check and test implementation
    def _perform_INSERTION_PRESERVE_CHILD(self) -> Optional[State]:
        """Adds an Actions.INSERTION_PRESERVE_CHILD edge between top two items of Stack (if present).
        
        INSERTION_PRESERVE_CHILD is valid iff Constraints.stack_top_two_different_sources().
        """
        ACTION = Actions.INSERTION_PRESERVE_CHILD
        return self._generic_parent_child(action=ACTION, preserve_child=True, preserve_parent=False)

    # TODO: should there be only INSERTION and allow both to remain on stack?
    # that would require checking that current_graph doesn't already contain the edge
    # TODO: should INSERTION_* always point to a NULL in GOLD? if so
    # FIXME: check and test implementation
    def _perform_INSERTION_PRESERVE_PARENT(self) -> Optional[State]:
        """Adds an Actions.INSERTION_PRESERVE_PARENT edge between top two items of Stack (if present).
        
        INSERTION_PRESERVE_PARENT is valid iff Constraints.stack_top_two_different_sources().
        """
        ACTION = Actions.INSERTION_PRESERVE_PARENT
        return self._generic_parent_child(action=ACTION, preserve_child=False, preserve_parent=True)

    # FIXME: check implementation and add tests
    def _perform_SUBSTITUTION(self) -> Optional[State]:
        """Adds an Actions.SUBSTITUTION edge between top two items of Stack (if present).
        
        SUBSTITUTION is valid iff Constraints.stack_top_two_different_sources().
        """
        ACTION = Actions.SUBSTITUTION
        return self._generic_parent_child(action=ACTION, preserve_child=False, preserve_parent=False)
  
    # TODO: should there be only DELETION where edge points to itself?
    # FIXME: check and test implementation
    def _perform_DELETION_PRESERVE_CHILD(self) -> Optional[State]:
        """Adds an Actions.DELETION_PRESERVE_CHILD edge between top two items of Stack (if present).
        
        DELETION_PRESERVE_CHILD is valid iff Constraints.stack_top_two_different_sources().
        """
        ACTION = Actions.DELETION_PRESERVE_CHILD
        return self._generic_parent_child(action=ACTION, preserve_child=True, preserve_parent=False)

    # TODO: should there be only DELETION where edge points to itself?
    # FIXME: check and test implementation
    def _perform_DELETION_PRESERVE_PARENT(self) -> Optional[State]:
        """Adds an Actions.DELETION_PRESERVE_PARENT edge between top two items of Stack (if present).
        
        DELETION_PRESERVE_PARENT is valid iff Constraints.stack_top_two_different_sources().
        """
        ACTION = Actions.DELETION_PRESERVE_PARENT
        return self._generic_parent_child(action=ACTION, preserve_child=False, preserve_parent=True)