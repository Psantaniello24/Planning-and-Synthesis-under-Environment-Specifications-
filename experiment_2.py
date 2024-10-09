import spot
import pydot
import networkx as nx
from buddy import bddtrue
from ltlf2dfa.parser.ltlf import LTLfParser
from graphviz import Source


#Example 2
env_1=spot.formula('!RobotOut & Dust')
env_2=spot.formula('[]((!RobotOut & clean_dust)-> (()(!RobotOut & !Dust)))')
env_3=spot.formula('[](get_out->(Dust<->()Dust) & ()RobotOut)')
agent_goal=spot.formula('<>(RobotOut & !Dust)')
print(env_1)
print(env_2)
print(env_3)
#print(env_4)
#print(env_5)
print(agent_goal)

# to parse an LTLf formula :
parser = LTLfParser()

formula="!((dust & !robotout & G((!robotout & clean_dust) -> X(!dust & !robotout)) & G(get_out -> ((dust <-> X dust) & X robotout))))|| F(!dust & robotout) "
formula_goal="F(!dust & robotout)"
#formula_p=parser("G!synack -> G!ack")
formula_p=parser(formula)
formula_2=parser(formula_goal)
#print(formula_a)
#print(formula_b)      
print(formula_p)    

dfa_1=formula_p.to_dfa()                          # prints the DFA in DOT format > langauge for describing graphs 
dfa_2=formula_2.to_dfa()
print(dfa_1)
print(dfa_2)

s = Source(dfa_1, filename="test_1.gv", format="png")
s.view()
s = Source(dfa_2, filename="test_2.gv", format="png")
s.view()
graphs_1 = pydot.graph_from_dot_file('test_1.gv')
graphs_2 = pydot.graph_from_dot_file('test_2.gv')
graph_1 = graphs_1[0]
graph_2 = graphs_2[0]
G_1 =nx.DiGraph(nx.nx_pydot.from_pydot(graph_1))
G_2 =nx.nx_pydot.from_pydot(graph_2)

#creating a game from the dfa

bdict = spot.make_bdd_dict();
game = spot.make_twa_graph(bdict)
#game.new_states(G_1.number_of_edges())
game.new_states(6)
print(G_1.number_of_edges())
list(G_1.edges())
for (s, d) in ((0,1), (1, 2), 
               (1, 3), (1, 4),
               (1, 5), (2, 2),
               (3, 3), (3, 2), (3, 5),
               (3, 4),(4,2),(4,3),
               (4, 4), (5, 3),
               (5, 2),(5,5)):
  game.new_edge(s, d, bddtrue)

for (s, d) in list(G_1.edges()):
  if s=='init':
    s='0'
  if d=='init':
    d='0'
  if s!=d:  
   game.new_edge(int(s),int(d) ,bddtrue)

for (s, d) in list(G_1.edges()):
  if s!='init' and d!='init':
   game.new_edge(int(s)-1,int(d)-1 ,bddtrue)

spot.set_state_players(game, [True,False,True,False,False,True])
game.show('.g')
spot.solve_game(game) #False
spot.highlight_strategy(game)
game.show('.g')
