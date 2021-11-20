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
            stack=stack or self.stack,
            gold_queue=gold_queue or self.gold_queue,
            transcribed_queue=transcribed_queue or self.transcribed_queue,
            gold_graph=gold_graph or self.gold_graph,
            current_graph=current_graph or self.current_graph,
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

    # FIXME: implement me
    def _perform_SHIFT_T(self) -> Optional[State]:
        return None

    # FIXME: implement me
    def _perform_SHIFT_G(self) -> Optional[State]:
        return None

    # FIXME: implement me
    def _perform_STACK_SWAP(self) -> Optional[State]:
        return None

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

    def _perform_ALIGN(self) -> Optional[State]:
        """Adds an ALIGN edge between top two items of Stack (if present)"""
        # create a copy to safely modify
        stack = self.stack.copy()
        if len(stack) < 2:
            return None
        s1 = stack.pop()
        s2 = stack.pop()
        # FIXME: is this the right direction?
        edge = Edge(source=s1, destination=s2, label=Actions.ALIGN)
        new_graph = Graph(edges=self.current_graph.edges + [edge])
        return self.copy(current_graph=new_graph)

    # FIXME: implement me
    def _perform_SUBSTITUTION(self) -> Optional[State]:
        return None

    # FIXME: implement me
    def _perform_DELETION(self) -> Optional[State]:
        return None
