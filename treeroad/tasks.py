# Graph tasks
import rrdtool, os
from treeroad.models import graph
from django.conf import settings

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

def drawThumb(graph):
    if not graph.thumbPath:
        return None
    options = ['--only-graph','--start',str(graph.start),'--end',str(graph.end),'--width','270','--height','40']
    for option in parseGraphOptions(graph):
        options.append(str(option))
    for option in parseDataDefs(graph.defs.all()):
        options.append(str(option))
    if hasattr(settings,'RRDROOT'):
        os.chdir(settings.RRDROOT)
    rrdtool.graph(settings.PNGROOT + str(graph.thumbPath),*options)
def drawGraph(graph,thumb=False):
    if not graph.path:
        return None
    options = ['--title',str(graph.name),'--start',str(graph.start),'--end',str(graph.end),'--width',str(graph.width),'--height',str(graph.height)]
    for option in parseGraphOptions(graph):
        options.append(str(option))
    for option in parseDataDefs(graph.defs.all()):
        options.append(str(option))
    if graph.active:
        if hasattr(settings,'RRDROOT'):
            os.chdir(settings.RRDROOT)
        if not os.path.exists(os.path.dirname(settings.PNGROOT + graph.path)):
            os.makedirs(os.path.dirname(settings.PNGROOT + graph.path))
        if graph.drawThumbnail:
            drawThumb(graph)
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

    
    