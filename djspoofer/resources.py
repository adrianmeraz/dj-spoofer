from import_export import resources

from .models import Proxy


class ProxyAdminResource(resources.ModelResource):

    class Meta:
        model = Proxy
        fields = ('url', 'mode', 'country', 'city')
