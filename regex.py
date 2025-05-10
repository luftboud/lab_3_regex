"""Module for regex finite state machine"""
from __future__ import annotations
from abc import ABC, abstractmethod


class State(ABC):
    """state for regex finite state machine"""

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def check_self(self, char: str) -> bool:
        """
        function checks whether occured character is handled by current ctate
        """
        pass

    def check_next(self, next_char: str) -> State | Exception:
        """method checks if next character is handled by current state"""
        for state in reversed(self.next_states):
            if state.check_self(next_char):
                return state
        raise NotImplementedError("rejected string")


class StartState(State):
    """state for start of the string"""
    next_states: list[State] = []

    def __init__(self):
        super().__init__()

    def check_self(self, char):
        return super().check_self(char)


class TerminationState(State):
    """
    state for end of the string
    """

    def __init__(self):
        super().__init__()

    def check_self(self, char):
        return True


class DotState(State):
    """
    state for . character (any character accepted)
    """


    def __init__(self):
        super().__init__()
        self.next_states = []

    def check_self(self, char: str):
        return True

class AsciiState(State):
    """
    state for alphabet letters or numbers
    """

    def __init__(self, symbol: str) -> None:
        self.next_states = []
        self.curr_sym = symbol

    def check_self(self, curr_char: str):
        return self.curr_sym == curr_char


class StarState(State):
    """
    state for * character (zero or more characters accepted)
    """

    def __init__(self, checking_state: State):
        self.next_states = []
        self.state = checking_state
        self.next_states.append(checking_state)
        self.next_states.append(self)

    def check_self(self, char):
        for state in self.next_states:
            if isinstance(state, StarState):
                continue
            if state.check_self(char):
                return True
        return False


class PlusState(State):
    """state for + character (at least one character accepted)"""
    def __init__(self, checking_state: State):
        self.next_states = []
        self.state = checking_state
        self.next_states.append(StarState(checking_state))

    def check_self(self, char):
        if not self.state.check_self(char):
            return False
        return True
    def check_next(self, next_char: str):
        for el in self.next_states[1:]:
            self.next_states[0].next_states.append(el)
        for state in reversed(self.next_states):
            if state.check_self(next_char):
                return state
        raise NotImplementedError("rejected string")


class RegexFSM:
    """Class for regex finite state machine"""
    curr_state: State = StartState()

    def __init__(self, regex_expr: str) -> None:

        prev_state = self.curr_state
        tmp_next_state = self.curr_state

        i = 0

        while i < len(regex_expr):
            char = regex_expr[i]

            if i+1 != len(regex_expr):
                next_char = regex_expr[i+1]
                if next_char in ("*", "+"):
                    repeated = self.__init_next_state(char, None, None)
                    tmp_next_state = self.__init_next_state(next_char, prev_state, repeated)
                    prev_state.next_states.append(tmp_next_state)
                    prev_state = tmp_next_state
                    i+= 2
                    continue

            tmp_next_state = self.__init_next_state(char, prev_state, tmp_next_state)
            prev_state.next_states.append(tmp_next_state)
            prev_state = tmp_next_state
            i += 1
        prev_state.next_states.append(TerminationState())

    def __init_next_state(
        self, next_token: str, prev_state: State, tmp_next_state: State
    ) -> State:
        new_state = None

        match next_token:
            case next_token if next_token == ".":
                new_state = DotState()
            case next_token if next_token == "*":
                new_state = StarState(tmp_next_state)

            case next_token if next_token == "+":
                new_state = PlusState(tmp_next_state)

            case next_token if next_token.isascii():
                new_state = AsciiState(next_token)

            case _:
                raise AttributeError("Character is not supported")

        return new_state

    def check_string(self, string):
        """
        function checks if string is accepted by regex
        """
        curr_state = self.curr_state
        try:
            curr_state = curr_state.check_next(string[0])
        except NotImplementedError:
            return False

        for char in string:
            try:
                curr_state = curr_state.check_next(char)
            except NotImplementedError:
                return False
            if not curr_state.check_self(char):
                return False
        try:
            curr_state = curr_state.check_next("")
        except NotImplementedError:
            return False
        return isinstance(curr_state, TerminationState)


if __name__ == "__main__":
    regex_pattern = "a*4.+hi"

    regex_compiled = RegexFSM(regex_pattern)

    print(regex_compiled.check_string("aaaaaa4uhi"))  # True
    print(regex_compiled.check_string("4uhi"))  # True
    print(regex_compiled.check_string("meow"))  # False
    print(regex_compiled.check_string("4ghi")) # True
    print("\n")
    print(regex_compiled.check_string("a4!hi")) # True
    print(regex_compiled.check_string("aaaaahi")) # False
    print(regex_compiled.check_string("aaaaa4....hi")) # True
    print(regex_compiled.check_string("a44hi")) # True
    print("\n")
    print(regex_compiled.check_string("a4.h")) # False
    print(regex_compiled.check_string("aaaa4😎hi")) # True
    print(regex_compiled.check_string("aaa4hi")) # False
    print(regex_compiled.check_string("ahihi")) # False
    print(regex_compiled.check_string("a4wowhi")) # True
