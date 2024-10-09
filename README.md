# Planning-and-Synthesis-under-Environment-Specifications-

Description of the implementation of the Algorithm:

- Parse Environment and Agent goal formula using SPOT

- Compute NOT environment OR goal formula

- Parse NOT environment OR goal formula using SPOT

- Transform the formula into a DFA using LTLf2DFA tool(output in .DOT format)

- From .DOT format to Networkx Directed graph passing through Pydot

- Setup the Reachability game over the agent using SPOT support for games, and the DFA as Arena of the game

- Solve the game for the agent

- If the agent is winning, meaning that the initial state is a winning state for the agent, return a strategy as solution
