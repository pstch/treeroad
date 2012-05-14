import rrdtool
from treeroad.models import rrdDataSource

def readRrdInfo(rrdroot,_rrdfile,test):
    path = rrdroot + '/' + _rrdfile.service.node.pathPart + '/' + _rrdfile.service.pathPart + '/' + _rrdfile.pathPart
    if not path.endswith('.rrd'):
        return _rrdfile,0,0,[],"<br/>Error @" + path + ": Not an RRD File"
    info = rrdtool.info(str(path))
    keys = info.keys()
    dslist = []
    _dslist = []
    _dbg = ''
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