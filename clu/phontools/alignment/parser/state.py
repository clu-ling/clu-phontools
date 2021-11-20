from __future__ import annotations
from .actions import Actions
from .graph import Edge, Graph
from .queue import Queue
from .stack import Stack
from .symbols import *
from dataclasses import dataclass
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

    def copy(
        self,
        stack: Optional[Stack] = None,
        gold_queue: Optional[Queue] = None,
        transcribed_queue: Optional[Queue] = None,
        gold_graph: Optional[Graph] = None,
        current_graph: Optional[Graph] = None,
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
        )

    @property
    def actions_map(self) -> Dict[Actions, ActionFunc]:
        return {
            Actions.ALIGN: self._perform_ALIGN,
            Actions.DELETION: self._perform_DELETION,
            Actions.DELETION_PRESERVE_COPY_CHILD: self._perform_DELETION_PRESERVE_COPY_CHILD,
            Actions.DELETION_PRESERVE_COPY_PARENT: self._perform_DELETION_PRESERVE_COPY_PARENT,
            Actions.DISCARD_G: self._perform_DISCARD_G,
            Actions.DISCARD_T: self._perform_DISCARD_T,
            Actions.INSERTION_PRESERVE_COPY_CHILD: self._perform_INSERTION_PRESERVE_COPY_CHILD,
            Actions.INSERTION_PRESERVE_COPY_PARENT: self._perform_INSERTION_PRESERVE_COPY_PARENT,
            Actions.SHIFT_G: self._perform_SHIFT_G,
            Actions.SHIFT_T: self._perform_SHIFT_T,
            Actions.STACK_SWAP: self._perform_STACK_SWAP,
            Actions.SUBSTITUTION: self._perform_SUBSTITUTION,
        }

    def valid_actions(self) -> List[Actions]:
        """Determines valid actions"""
        return [
            action for action, func in self.actions_map.items() if func() is not None
        ]

    def perform_action(self, action: Actions) -> Optional[State]:
        """Applies the provided action to the state"""
        actions_map = self.actions_map
        if action in actions_map:
            return actions_map[action]()
        raise NotImplementedError(f"Action {action} not recognized")

    # FIXME: implement me
    def _perform_DELETION(self) -> Optional[State]:
        return None

    # FIXME: implement me
    def _perform_DISCARD_T(self) -> Optional[State]:
        return None

    # FIXME: implement me
    def _perform_DISCARD_G(self) -> Optional[State]:
        return None

    def is_valid_SHIFT_T(self) -> bool:
        """SHIFT_T valid iff len(transcribed_queue) > 0"""
        return len(self.transcribed_queue) > 0

    def _perform_SHIFT_T(self) -> Optional[State]:
        """Shifts first item from transcribed_queue to top of stack"""
        if not self.is_valid_SHIFT_T():
            return None
        stack = self.stack.copy()
        t_queue = self.transcribed_queue.copy()
        next_ps = t_queue.pop()
        stack.push(next_ps)
        return self.copy(stack=stack, transcribed_queue=t_queue)

    def is_valid_SHIFT_G(self) -> bool:
        """SHIFT_G valid iff len(gold_queue) > 0"""
        return len(self.gold_queue) > 0

    def _perform_SHIFT_G(self) -> Optional[State]:
        """Shifts first item from gold_queue to top of stack"""
        if not self.is_valid_SHIFT_G():
            return None
        stack = self.stack.copy()
        g_queue = self.gold_queue.copy()
        next_ps = g_queue.pop()
        stack.push(next_ps)
        return self.copy(stack=stack, gold_queue=g_queue)

    def is_valid_STACK_SWAP(self) -> bool:
        """STACK_SWAP is valid iff there are at least two items on the stack."""
        return len(self.stack) >= 2

    def _perform_STACK_SWAP(self) -> Optional[State]:
        """Swaps the top two items on the stack"""
        if not self.is_valid_STACK_SWAP():
            return None
        stack = self.stack.copy()
        s1 = stack.pop()
        s2 = stack.pop()
        for ps in [s2, s1]:
            stack.push(s2)
        return self.copy(stack=stack)

    # FIXME: implement me
    def _perform_INSERTION_PRESERVE_COPY_CHILD(self) -> Optional[State]:
        return None

    # FIXME: implement me
    def _perform_INSERTION_PRESERVE_COPY_PARENT(self) -> Optional[State]:
        return None

    # FIXME: implement me
    def _perform_DELETION_PRESERVE_COPY_CHILD(self) -> Optional[State]:
        return None

    # FIXME: implement me
    def _perform_DELETION_PRESERVE_COPY_PARENT(self) -> Optional[State]:
        return None

    def is_valid_ALIGN(self) -> bool:
        """ALIGN is valid iff there are at least two items on the stack AND
        top two items on the stack have TRANSCRIPT and GOLD TranscriptTypes.
        """
        stack = self.stack.copy()
        if len(stack) >= 2:
            s1 = stack.pop()
            s2 = stack.pop()
            # TODO: do we want to enforce an order here?
            return set([TranscriptTypes.GOLD, TranscriptTypes.TRANSCRIPT]) == set(
                [s1.source, s2.source]
            )
        return False

    def _perform_ALIGN(self) -> Optional[State]:
        """Adds an ALIGN edge between top two items of Stack (if present)"""
        # check if action is valid
        if not self.is_valid_ALIGN():
            return None
        stack = self.stack.copy()
        s1 = stack.pop()
        s2 = stack.pop()
        keep: ParseSymbol = s1 if s1.source == TranscriptTypes.GOLD else s2
        drop: ParseSymbol = s1 if s1.source == TranscriptTypes.TRANSCRIPT else s2
        # ALIGN must point from Transcript -> GOLD
        edge = Edge(source=drop, destination=keep, label=Actions.ALIGN)
        new_graph = Graph(edges=self.current_graph.edges + [edge])
        stack.push(keep)
        return self.copy(stack=stack, current_graph=new_graph)

    # FIXME: implement me
    def _perform_SUBSTITUTION(self) -> Optional[State]:
        return None

    # FIXME: implement me
    def _perform_DELETION(self) -> Optional[State]:
        return None