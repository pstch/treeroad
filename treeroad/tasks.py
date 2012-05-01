# Graph tasks
import rrdtool
from treeroad.models import graph

def parseGraphOptions(graph):
    return ""

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
    
    rrdtool.graph(graph.path,*options)
def graphTask():
    graphs = graph.objects.all()
    fails = []
    done = []
    for graphItem in graphs:
        if not drawGraph(graphItem):
            fails.append(graphItem)
        else:
            done.append(done)

    
    