# -*- coding: utf-8 -*-

# Copyright(C) 2018 Sasha Bouloudnine

from monseigneur.core.tools.backend import Module
from .browser import SiaBrowser

__all__ = ['SiaModule']


class SiaModule(Module):
    NAME = 'sia'
    MAINTAINER = u'Jamal'
    EMAIL = '{first}.{last}@lobstr.io'
    BROWSER = SiaBrowser

    def iter_members(self, memberlist_page_no):
        return self.browser.iter_members(memberlist_page_no)
    def members_details(self, member):
        return self.browser.members_details(member)
    def iter_offices(self, offices_list_page_no):
        return self.browser.iter_offices(offices_list_page_no)
    def offices_details(self, office):
        return self.browser.offices_details(office)
    def get_member_list(self):
        return self.browser.get_member_list()