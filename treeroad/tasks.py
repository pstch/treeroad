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
    options = ['--start',str(graph.start),'--end',str(graph.end)]
    for option in parseGraphOptions(graph):
        options.append(str(option))
    for option in parseDataDefs(graph.defs.all()):
        options.append(str(option))
    if graph.active:
        from django.conf import settings
        if hasattr(settings,'RRDROOT'):
            os.chdir(settings.RRDROOT)
        if not os.path.exists(os.path.dirname(graph.path)):
            os.makedirs(os.path.dirname(settings.PNGROOT + graph.path)) # FIXME: Doesn't work. No errors reported. Reported in Git commit
        if rrdtool.graph(settings.PNGROOT + str(graph.path),*options):
            graph.lastCommandLine = options
            graph.save()
            return True
        else:
            graph.lastCommandLine = options
            graph.save()
            return False
    
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

    
    