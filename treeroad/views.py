# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
import rrdtool

from os import path
from os import listdir
from treeroad.models import domain, node, service, rrdFile, rrdDataSource

def parseTree(request, test=1):
    from django.conf import settings
    
    if not hasattr(settings,'RRDROOT'):
        return HttpResponse("<h1>RRDROOT variable not referenced.</h1>")

    rrdroot = settings.RRDROOT + '/'

    if not path.isdir(rrdroot):
        return HttpResponse("<h1>Directory " + rrdroot + " not found</h1>")
    
    # path_items : Directories
    # path_item : Directory
    # _item : Object
    # items : Object list
    # item : Object model
    
    domains = []
    nodes = []
    services = []
    rrdfiles = []
    datasources = []
    
    _dbg = ''
    
    skipped_domains = 0
    skipped_nodes = 0
    skipped_services = 0
    skipped_rrdfiles = 0
    skipped_datasources = 0
    
    found_domains = 0
    found_nodes = 0
    found_services = 0
    found_rrdfiles = 0
    found_datasources = 0
    # Heavy fail inside this block. I first put the if clause checking if the object already exists before the .save() routine. This made the application go crazy one existing item had missing childrens. The childs were referrencing the object that I did not create because it already existed. So I moved the if clause at the beginning of each "for" iteration. Now when an object already exists, the script skips it AND ALL OF ITS CHILDS. This is quite bad. This is why I should have kept the first setup but with changing which parent the childs are referring too... TODO
    # Above fixed at 20/4 20:46 -- Happy 420
    # Still failing at 20:50
    # Fixed at 20:53
    # Works. Add only non-existing items. Even when the parent is already existing \o/.
    path_nodes = listdir(rrdroot)
    for path_node in path_nodes:
        _node = None
        if not path_node.find('.') == -1:
            _path = path_node.split('.')
            found_domains += 1
            if domain.objects.filter(name=_path[-1]):
                _dom = domain.objects.filter(name=_path[-1])[0]
                skipped_domains += 1
            else:
                _dom = domain(name=_path[-1])
                if not test:
                    _dom.save()
            domains.append(_dom)
            _node = node(name=_path[-2],pathPart=path_node,domain=_dom)
        else:
            _node = node(name=path_node,pathPart=path_node)
        nodes.append(_node)
        found_nodes += 1
        if not node.objects.filter(pathPart=path_node):
            if not test:
                _node.save()
        else:
            _node = node.objects.filter(pathPart=path_node)[0]
            skipped_nodes += 1 
        path_services = listdir(rrdroot+path_node)
        for path_service in path_services:
            _service = service(name=path_service,node=_node,pathPart=path_service)
            services.append(_service)
            found_services += 1
            if not service.objects.filter(pathPart=path_service,node=_node):
                if not test:
                    _service.save()
            else:
                _service = service.objects.filter(pathPart=path_service,node=_node)[0]
                skipped_services += 1
            path_rrdfiles = listdir(rrdroot+path_node+'/'+path_service)
            for path_rrdfile in path_rrdfiles:
                _rrdfile = rrdFile(pathPart=path_rrdfile,service=_service)
                rrdfiles.append(_rrdfile)
                found_rrdfiles += 1
                if not rrdFile.objects.filter(pathPart=path_rrdfile,service=_service):
                    if not test:
                        _rrdfile.save()
                else:
                    _rrdfile = rrdFile.objects.filter(pathPart=path_rrdfile,service=_service)[0]
                    skipped_rrdfiles += 1
                
                _rrdfile, _skipped_datasources, _found_datasources, _datasources, __dbg = readRrdInfo(rrdroot,_rrdfile,test)
                
                skipped_datasources += _skipped_datasources
                found_datasources += _found_datasources
                datasources += _datasources
                _dbg += __dbg
    
    return render_to_response("treeroad/parseTree.html", {'domains' : domains,
                                                          'found_domains' : found_domains,
                                                          'skipped_domains' : skipped_domains,
                                                          'nodes' : nodes ,
                                                          'skipped_nodes' : skipped_nodes,
                                                          'found_nodes' : found_nodes,
                                                          'services' : services,
                                                          'skipped_services' : skipped_services,
                                                          'found_services' : found_services,
                                                          'rrdfiles' : rrdfiles,
                                                          'skipped_rrdfiles' : skipped_rrdfiles,
                                                          'found_rrdfiles' : found_rrdfiles,
                                                          'datasources' : datasources,
                                                          'skipped_datasources' : skipped_datasources,
                                                          'found_datasources' : found_datasources,
                                                          'test' : test,
                                                          'debug' : _dbg })
def readRrdInfo(rrdroot,_rrdfile,test):
    path = rrdroot + '/' + _rrdfile.service.node.pathPart + '/' + _rrdfile.service.pathPart + '/' + _rrdfile.pathPart
    info = rrdtool.info(str(path))
    keys = info.keys()
    dslist = []
    _dslist = []
    _dbg = ''
    _dbg += """<br>Testing """ + str(_rrdfile) + " for a DS"
    for key in keys:
        if key.startswith('ds['):
            ds_name = key.split('.')[0][3:-1]
            try:
                dslist.index(ds_name)
            except ValueError:
                dslist.append(ds_name)
    found = len(dslist)
    skip = 0
    for ds in dslist:
        if not rrdDataSource.objects.filter(rrdFile=_rrdfile,name=ds):
            _ds = rrdDataSource(name=ds,rrdFile=_rrdfile)
            _dslist.append(_ds)
            if not test:
                _ds.save()
        else:
            skip += 1
    return (_rrdfile,skip,found,_dslist,_dbg)
            