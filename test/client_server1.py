
import ivy_module
from ivy_compiler import ivy_from_string
from tk_ui import new_ui

prog = """#lang ivy1

type client
type server

relation c(X : client,Y : server)
relation s(X : server)

init (s(W) & ~c(X,Y))
individual x : client,y : server,z : client

derived foo(X:client,Y:server) = c(X,Y) & ~s(Y)

action connect = {
  x := *;
  y := *;
  assume s(y) & ~c(x,Z);
  c(x,y) := true;
  s(y) := false
}

action disconnect = {
  x := *;
  y := *;
  assume c(x,y);
  c(x,y) := false;
  s(y) := true
}

action error = {
  x := *;
  y := *;
  z := *;
  assume x ~= z & c(x,y) & c(z,y)
}

# concept c1(X,Y,Z) = (c(X,Z) * ~X = Y * c(Y,Z))

conjecture (X = Z | ~c(X,Y) | ~c(Z,Y))
"""

with ivy_module.Module():
    main_ui = new_ui()
    ui = main_ui.add(ivy_from_string(prog))
    ui.execute_action(ui.node(0),"connect")
    cg = ui.view_state(ui.g.states[1])
    cg.materialize_edge((cg.relation('c(X,Y)'),cg.node('client'),cg.node('server')))
    cg.split(cg.relation('s'),cg.node('=b'))
    cg.materialize(cg.node('=b','s'))
    main_ui.answer('Refine')
    cg.reverse()
    cg.backtrack()
    cg.recalculate()
    ui.execute_action(ui.node(1),"connect")
    ui.mark_node(ui.node(1))
    ui.cover_node(ui.node(2))
#    ui.mainloop()


