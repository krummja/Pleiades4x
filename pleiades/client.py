from __future__ import annotations
from typing import Type
import pygame as pg

from pleiades.states.state import State
from pleiades.ui_manager import UIManager


class Client:

    def __init__(self):
        self.states = {}
        self.stack = []
        self.clock = pg.time.Clock()
        self.ui = UIManager(self)

    @property
    def current_state(self):
        return self.stack[-1]

    def initialize(self, key: str, state: Type[State]) -> None:
        self.states[key] = state
        self.push_state(state)

    def push_state(self, state: Type[State]) -> None:
        self.ui.backend.clear_and_reset()
        self.stack.append(state(self))
        self.current_state.on_enter()

    def pop_state(self):
        self.ui.backend.clear_and_reset()
        self.current_state.on_leave()
        self.stack.pop()
        self.current_state.on_enter()

    def clear_stack(self):
        while len(self.stack) > 1:
            self.stack.pop()

    def set_state(self, state: Type[State]):
        self.clear_stack()
        self.push_state(state)

    def run(self):
        running = True
        while running:
            dt = 0.001 * self.clock.tick(60)
            self.current_state.handle_input()
            self.current_state.update(dt)
