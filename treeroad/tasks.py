# Graph tasks
import rrdtool, os
from treeroad.models import graph

def parseGraphOptions(graph):
    return ["--imgformat","PNG"]

def parseDataDefs(defs):
    ret = []
    for definition in defs:
        ret.append(definition.defInstruction())
        subdefs = parseLineDefs(definition.defs.all())
        for subdef in subdefs:
            ret.append(subdef)
    return ret

def parseLineDefs(defs):
    ret = []
    for definition in defs:
        ret.append(definition.defInstruction())
    return ret

def drawGraph(graph):
    if not graph.path:
        return None
    options = []
    for option in parseGraphOptions(graph):
        options.append(str(option))
    for option in parseDataDefs(graph.defs.all()):
        options.append(str(option))
    if graph.active:
        from django.conf import settings
        if hasattr(settings,'RRDROOT'):
            os.chdir(settings.RRDROOT)
        if not os.path.exists(os.path.dirname(graph.path)):
            os.makedirs(os.path.dirname(graph.path))
        if rrdtool.graph(str(graph.path),*options):
            return True
        else:
            return False
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

    
    