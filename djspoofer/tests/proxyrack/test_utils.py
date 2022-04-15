from django.test import TestCase

from djspoofer.remote.proxyrack import const, utils


class UtilTests(TestCase):
    """
    Utility Tests
    """

    def test_proxy_builder(self):
        proxy_builder = utils.ProxyBuilder(
            username='proxyman123',
            password='goodpw567',
            netloc='megaproxy.rotating.proxyrack.net:10000',
            country='US',
            city='Seattle,NewYork,LosAngeles',
            isp='Verizon,Comcast',
            refreshMinutes=10,
            osName=const.ProxyOs.LINUX,
            session='13ac97fe-0f26-45ff-aeb9-2801400326ec',
            proxyIp='184.53.48.165'
        )

        self.assertEquals(
            proxy_builder.http_url,
            ('http://proxyman123;country=US;city=Seattle,NewYork,LosAngeles;isp=Verizon,Comcast;refreshMinutes=10;'
             'osName=Linux;session=13ac97fe-0f26-45ff-aeb9-2801400326ec;proxyIp=184.53.48.165:'
             'goodpw567@megaproxy.rotating.proxyrack.net:10000')
        )
