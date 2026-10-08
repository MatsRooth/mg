% Inline SVG trees for Herculog/prolog-jupyter-kernel.
% Load with consult('../code/inline_tree.pl').
% Graphviz's dot executable must be on the Jupyter server's PATH.
:- module(mg_inline_tree, [inline_tree/1, tree_dot/2]).
:- use_module(library(error)).

% This adapter uses the kernel's existing Graphviz response mechanism.
% It depends on an internal kernel predicate; tree_dot/2 is independent.
inline_tree(Tree) :-
    tree_dot(Tree, Dot),
    ( current_predicate(jupyter_term_handling:assert_success_response/4) ->
        jupyter_term_handling:assert_success_response(
            query, [], '', [print_transition_graph=Dot])
    ; throw(error(existence_error(procedure, jupyter_kernel),
                  context(inline_tree/1, 'Run this in the Prolog Jupyter kernel')))
    ).

% Convert Stabler's Label/Children trees to DOT, preserving child order
% and giving every occurrence its own node (including repeated labels).
tree_dot(Tree, Dot) :-
    must_be(ground, Tree),
    with_output_to(atom(Dot),
        ( writeln('digraph tree {'),
          writeln('  graph [ordering=out, rankdir=TB, nodesep=0.18, ranksep=0.35];'),
          writeln('  node [shape=plaintext, fontname="Times-Roman", fontsize=14];'),
          writeln('  edge [arrowhead=none];'),
          emit_tree(Tree, 0, _),
          writeln('}') )).

emit_tree(Label/Children, Id, Next) :-
    !,
    must_be(list, Children),
    label_text(Label, Text),
    dot_quote(Text, Quoted),
    format('  n~d [label=~w];~n', [Id, Quoted]),
    First is Id+1,
    emit_children(Children, Id, First, Next).
emit_tree(Tree, _, _) :-
    throw(error(type_error(stabler_tree, Tree), context(tree_dot/2, 'Expected Label/Children'))).

emit_children([], _, Next, Next).
emit_children([Tree|Trees], Parent, Id, Next) :-
    format('  n~d -> n~d;~n', [Parent, Id]),
    emit_tree(Tree, Id, After),
    emit_children(Trees, Parent, After, Next).

label_text([], 'ε') :- !.
label_text(Words, Text) :-
    is_list(Words), maplist(atomic, Words), !,
    atomic_list_concat(Words, ' ', Text).
label_text(Label, Text) :-
    with_output_to(atom(Text), write_term(Label, [quoted(false), numbervars(true)])).

% Escape user labels as DOT strings, without treating them as DOT code.
dot_quote(Text, Quoted) :-
    atom_codes(Text, Codes),
    phrase(dot_codes(Codes), Escaped),
    append([34|Escaped], [34], QuotedCodes),
    atom_codes(Quoted, QuotedCodes).
dot_codes([]) --> [].
dot_codes([C|Cs]) --> dot_char(C), dot_codes(Cs).
dot_char(34) --> !, [92,34].
dot_char(92) --> !, [92,92].
dot_char(10) --> !, [92,110].
dot_char(13) --> !, [92,114].
dot_char(9) --> !, [92,116].
dot_char(C) --> [C].
