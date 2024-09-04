# -*- coding: utf-8 -*-

# Copyright(C) 2018 Sasha Bouloudnine

from monseigneur.core.browser import PagesBrowser, URL
from .pages import MemberListPage, MemberPage, OfficeListPage, OfficePage
import pandas as pd
import re
import time

__all__ = ['SiaBrowser']


class SiaBrowser(PagesBrowser):

    BASEURL = 'https://www.sia.ch/'

    memberlist_page= URL("https://www.sia.ch/fr/affiliation/liste-des-membres/membres-individuels/nc/1/\?tx_updsiafeuseradmin_pi1%5BdisplaySearchResult%5D=1&tx_updsiafeuseradmin_pi1%5Bpointer%5D=(?P<memberlist_page_no>\d+)", MemberListPage)

    member_details_page = URL("https://www.sia.ch/(?P<language>.+)/affiliation/liste-des-membres/membres-individuels/m/(?P<member_id>\d+)/", MemberPage)

    officelist_page = URL("https://www.sia.ch/fr/affiliation/liste-des-membres/membres-bureaux/nc/1/\?tx_updsiafeuseradmin_pi1%5BdisplaySearchResult%5D=1&tx_updsiafeuseradmin_pi1%5Bpointer%5D=(?P<officelist_page_no>\d+)", OfficeListPage)

    office_details_page = URL("https://www.sia.ch/(?P<language>.+)/affiliation/liste-des-membres/membres-bureaux/m/(?P<office_id>\d+)/", OfficePage)

    def __init__(self, *args, **kwargs):
        zip_lang = 'zip_language.xlsx'
        self.df = pd.read_excel(zip_lang)
        super(SiaBrowser, self).__init__(*args, **kwargs)

    def iter_members(self, memberlist_page_no):
        #time.sleep(1)
        self.memberlist_page.go(memberlist_page_no=memberlist_page_no)
        assert self.memberlist_page.is_here()
        return self.page.iter_members()

    def members_details(self, member):
        #zip = self.page.get_zip()
        #lang= self.page.get_lang(zip)
        #member_id = re.findall(r'(\d+)', member.url)[0]
        member_id = member.member_id
        language = member.language.lower()
        #time.sleep(1)
        self.member_details_page.go(language=language, member_id = member_id)
        member.url = self.url
        #print('Hello:', self.member_details_page)
        assert self.member_details_page.is_here()
        return self.page.get_members_details(obj=member)

    def iter_offices(self, officelist_page_no):
        #time.sleep(1)
        self.officelist_page.go(officelist_page_no=officelist_page_no)
        assert self.officelist_page.is_here()
        return self.page.iter_offices()

    def offices_details(self, office):
        #office_id = re.findall(r'(\d+)', office.url)[0]
        office_id = office.office_id
        language = office.language.lower()
        #time.sleep(1)
        self.office_details_page.go(language=language, office_id = office_id)
        office.url = self.url
        #print('Hello:', self.office_details_page)
        assert self.office_details_page.is_here()
        return self.page.get_offices_details(obj=office)

    def get_member_list(self):
        assert self.office_details_page.is_here()
        return self.page.get_member_list()
