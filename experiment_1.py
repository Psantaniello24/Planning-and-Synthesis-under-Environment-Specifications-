import spot
import pydot
import networkx as nx
from buddy import bddtrue
from ltlf2dfa.parser.ltlf import LTLfParser
from graphviz import Source

#define formulas 
env_1=spot.formula('[](alive->()(wait->alive))')
env_2=spot.formula('[](alive->()(shoot->(alive || !alive)))')
env_3=spot.formula('[](!alive->()(wait->!alive))')
env_4=spot.formula('[](!alive->()(shoot->!alive))')
env_5=spot.formula('[]((wait & shoot) & (wait->!shoot))')
agent_goal=spot.formula('<>!a')
print(env_1)
print(env_2)
print(env_3)
print(env_4)
print(env_5)
print(agent_goal)

#Example 1


# to parse an LTLf formula :
parser = LTLfParser()
#get the env->goal formula bu composing !env || goal 
formula="!((G(alive -> X(wait -> alive)) & G(alive -> X(shoot -> (alive | !alive))) & G(!alive -> X(wait -> !alive)) & G(!alive -> X(shoot -> !alive)) & G(shoot & wait & (wait -> !shoot)))) || F!a"
formula_goal="F!alive"
formula_p=parser(formula)
formula_2=parser(formula_goal)
print(formula_p)     
print(formula_2)           # prints "G(a -> X (b))"

# now we can directly translate the formula in his DFA
#dfa_a = A.to_dfa()
#dfa_b = B.to_dfa()
#print(dfa_a)
#print(dfa_b)
dfa_1=formula_p.to_dfa()                          # prints the DFA in DOT format > langauge for describing graphs 
dfa_2=formula_2.to_dfa()
print(dfa_1)
print(dfa_2)

#create and visualize graphs

s = Source(dfa_1, filename="test_1.gv", format="png")
s.view()
s = Source(dfa_2, filename="test_2.gv", format="png")
s.view()

graphs_1 = pydot.graph_from_dot_file('test_1.gv')
graphs_2 = pydot.graph_from_dot_file('test_2.gv')

graph_1 = graphs_1[0]
graph_2 = graphs_2[0]

G_1 =nx.DiGraph(nx.nx_pydot.from_pydot(graph_1))
G_2 =nx.Graph(nx.nx_pydot.from_pydot(graph_2))

#creating a game from the dfa

bdict = spot.make_bdd_dict()
game = spot.make_twa_graph(bdict)
game.new_states(n)

for (s, d) in list(G_1.edges()):
  if s=='init':
    s='0'
  if d=='init':
    d='0'
  game.new_edge(int(s),int(d) ,bddtrue)

game.new_edge(2,2 ,bddtrue)
spot.set_state_players(game, [False, True, False])
game.show('.g')

#solve the game 
spot.solve_game(game)
spot.highlight_strategy(game)
game.show('.g')
display(game)

