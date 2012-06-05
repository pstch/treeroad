# Code from : https://github.com/jsocol/django-adminplus
# Forked to : https://github.com/pstch/django-adminplus
# License ref in LICENSE
from django.contrib.admin.sites import AdminSite
from django.utils.text import capfirst


VERSION = (0, 1, 5)
__version__ = '.'.join([str(x) for x in VERSION])


class AdminSitePlus(AdminSite):
    """Extend AdminSite to allow registering custom admin views."""
    index_template = 'treeroad/admin/index.html'  # That was easy.
    custom_views = []

    def register_view(self, path, view, name=None, label=None):
        """Add a custom admin view.

        * `path` is the path in the admin where the view will live, e.g.
            http://example.com/admin/somepath
        * `view` is any view function you can imagine.
        * `name` is an optional pretty name for the list of custom views. If
            empty, we'll guess based on view.__name__.
        """
        self.custom_views.append((path, view, name, label))
        print 'HAHAHA: ' + str(label)

    def get_urls(self):
        """Add our custom views to the admin urlconf."""
        urls = super(AdminSitePlus, self).get_urls()
        from django.conf.urls.defaults import patterns, url
        for path, view, name, label in self.custom_views:
            urls += patterns('',
                url(r'^%s$' % path, self.admin_view(view)),
            )
        return urls

    def index(self, request, extra_context=None):
        """Make sure our list of custom views is on the index page."""
        if not extra_context:
            extra_context = {}
        custom_list = []
        for path, view, name, label in self.custom_views:
            if not name:
                name = capfirst(view.__name__)
            custom_list.append((path, name, label))
        # Sort views alphabetically.
        custom_list.sort(key=lambda x: x[1])
        extra_context.update({
            'custom_list': custom_list
        })
        return super(AdminSitePlus, self).index(request, extra_context)