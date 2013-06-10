# -*- coding: utf-8 -*-
import mechanize
import cookielib
import error
import re

import core
import models

from lxml import etree

class DeckboxApi(object):
    base = 'http://deckbox.org/accounts/login'

    def __init__(self, username, password, mcmUsername, mcmPassword):
        self.username = username
        self.password = password

        self.br = mechanize.Browser()
        self.cj = cookielib.LWPCookieJar()

        self.br.set_cookiejar(self.cj)

        self.br.set_handle_equiv(True)
        #self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)

        # follows refresh 0 but not hangs on refresh > 0
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; es-VE; rv:1.9.0.1)Gecko/2008071615 Debian/6.0 Firefox/9')]

        # debug
        #self.br.set_debug_http(True)
        #self.br.set_debug_redirects(True)
        #self.br.set_debug_responses(True)

        self.br.open(self.base)
        self.mcm = core.MCMApi(username=mcmUsername,password=mcmPassword)

    def login(self):
        self.br.select_form(nr=0)
        self.br['login'] = self.username
        self.br['password'] = self.password
        self.br.submit()

        r = self.br.response().read()
        m = re.search(r"Username or password is incorrect", r)
        if m:
            raise error.LoginError()

    def get_deck_needs(self, name):
        link = self.br.find_link(text_regex=name)
        self.br.follow_link(link)

        price_total_from = 0.0
        price_total_avg = 0.0

        # read wants lists
        utf8_parser = etree.HTMLParser(encoding='utf-8')
        tree = etree.fromstring(self.br.response().read().decode('utf-8'), parser=utf8_parser)
        wl = models.WantList(0, name)

        print u'Deck: %s\n' %name

        for wlnode in tree.xpath('//table[contains(@class, "deck")]/tr'):
            cnarr = wlnode.xpath('td[contains(@class, "card_name")]')
            if (len(cnarr) > 0 ):
                id = wlnode.attrib['id']
                havearr = wlnode.xpath('td[contains(@id, "card_count_Inventory_' + id + '")]')
                reqarr = wlnode.xpath('td[contains(@id, "card_count_Deck_' + id + '")]')
                cn = etree.tostring(cnarr[0], method="text").strip()
                have = int(etree.tostring(havearr[0], method="text").strip())
                req = int(etree.tostring(reqarr[0], method="text").strip())
                need = max(0, req-have)
                if ( need > 0):
                    price, expansion = self.get_cheapest(cn)
                    card = models.Card("", cn)
                    want = models.Want(card, need)
                    wl.wants.append(want)
                    print u'%d %s (%s) @ \u20ac%.2f = \u20ac%.2f' % (need, cn, expansion, price, price*need)
                    price_total_avg = price_total_avg + price*need

        print u'\nTotal: \u20ac%.2f' % price_total_avg

        # return wl

    def get_cheapest(self, name):
  
        price_avg = None
        expansion = None

        for r in db.mcm.search(name):
            ps = db.mcm.list_prices_summary(r.card)
            if ( price_avg is None or ps.price_avg < price_avg ):
                price_avg = ps.price_avg
                expansion = ps.expansion 

        return price_avg, expansion

if __name__ == '__main__':
    db = DeckboxApi(username='foo',password='bar',mcmUsername='',mcmPassword='')
    db.login()
    db.get_deck_needs('name of the deck')

