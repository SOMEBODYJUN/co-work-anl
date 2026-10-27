"""Compile a complete labeled policy to the quotient by identical cover sets.

The representative of an equivalence class depends on the complete history.
In the currently prescribed class it is the prescribed original label itself.
This is essential; a globally fixed representative need not preserve its path.
"""
from collections import defaultdict

def cover_classes(weights, topics):
    """Return the projection and its classes for compressed unit customers.

    weights maps a nonzero membership bitmask to its nonnegative multiplicity.
    Only positive multiplicities affect equality of actual cover sets.
    """
    keys={}
    projection=[]
    groups=[]
    for j in range(topics):
        key=tuple(sorted(b for b,v in weights.items() if v>0 and b&(1<<j)))
        if key not in keys:
            keys[key]=len(groups);groups.append([])
        cl=keys[key];projection.append(cl);groups[cl].append(j)
    return tuple(projection),tuple(tuple(g) for g in groups)

def quotient_policy(actions, players, projection):
    """Return (complete quotient actions, complete history lift).

    actions is a dictionary {ordered_original_history: original_label}, or a
    callable with that contract. projection[j] is the cover-equivalence class
    of original label j. Its image must be {0,...,q-1}.
    The supplied original policy need not be an SPE for compilation to run;
    the preservation theorem requires that separate hypothesis.
    """
    groups=defaultdict(list)
    for label,cl in enumerate(projection):groups[cl].append(label)
    assert set(groups)==set(range(len(groups)))
    get_action=actions if callable(actions) else actions.__getitem__
    compiled={};lifts={():()}
    def visit(H,h):
        if len(H)==players:return
        a=get_action(h); prescribed_class=projection[a]
        compiled[H]=prescribed_class
        for cl in range(len(groups)):
            rep=a if cl==prescribed_class else groups[cl][0]
            child=H+(cl,);lift=h+(rep,)
            lifts[child]=lift;visit(child,lift)
    visit((),())
    return compiled,lifts

def quotient_weights(weights,projection):
    """Preserve all unit customers while rewriting their membership bitmasks."""
    ans=defaultdict(int)
    for b,v in weights.items():
        if not v:continue
        out=0
        for j,cl in enumerate(projection):
            if b&(1<<j):out|=1<<cl
        ans[out]+=v
    return dict(ans)

def project_history(history,projection):
    return tuple(projection[a] for a in history)
