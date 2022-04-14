from django.test import TestCase

from proxyrack import const, utils


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
            osName=const.ProxyOs.MAC_OS_X,
            session='13ac97fe-0f26-45ff-aeb9-2801400326ec',
        )

        self.assertEquals(
            proxy_builder.full_str,
            ('proxyman123;country=US;city=Seattle,NewYork,LosAngeles;isp=Verizon,Comcast;refreshMinutes=10;'
             'osName=Mac OS X;session=13ac97fe-0f26-45ff-aeb9-2801400326ec:'
             'goodpw567@megaproxy.rotating.proxyrack.net:10000')
        )
