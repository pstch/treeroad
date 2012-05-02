# Graph tasks
import rrdtool
from treeroad.models import graph

def parseGraphOptions(graph):
    return ["--img-format","png"]

def parseDataDefs(defs):
    ret = []
    for definition in defs:
        ret.append(str(definition))
        ret.append(parseLineDefs(definition.defs.all()))
    return ret

def parseLineDefs(defs):
    ret = []
    for definition in defs:
        ret.append(str(definition))
    return ret

def drawGraph(graph):
    if not graph.path:
        return None
    options = []
    options.append(parseGraphOptions(graph))
    options.append(parseDataDefs(graph.defs.all()))
    if graph.active:
        rrdtool.graph(str(graph.path),options)
    graph.lastCommandLine = options
def graphTask():
    graphs = graph.objects.all()
    count = len(graphs)
    fails = []
    done = []
    for graphItem in graphs:
        if not drawGraph(graphItem):
            fails.append(graphItem)
        else:
            done.append(done)
    return done, fails, count

    
    