# Regex Finite State Machine

This project implements a simple Finite State Automaton (FSA) in Python that evaluates strings against a simplified regular expression.

### 🧠 Core Features
- Custom implementation of state classes:
  - `StartState`, `AsciiState`, `DotState`, `StarState`, `PlusState`, `TerminationState`
- Manual parsing of regex to build state transitions
- Support for basic quantifiers: `*`, `+`
- Character-by-character input validation via `check_self` and `check_next` methods

### 🚀 How to Use
Run the `regex.py` script directly. It will evaluate a series of test strings and print whether they match the expression.

```bash
python regex.py
```
### 📚 Note
This project is educational and demonstrates how FSAs work under the hood. It does not support full RegEx syntax.
___
Created with too much logic and too little sleep.


📄 [Project Report (PDF)](./report.pdf)