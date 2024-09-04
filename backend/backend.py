from mbackend.core.fetcher import Fetcher
from mbackend.core.application import Application
from monseigneur.modules.public.sia.alchemy.dao_manager import DaoManager
from monseigneur.modules.public.sia.alchemy.tables import Members,Offices, MemberOffice
from datetime import datetime


class SiaBackend(Application):

    APPNAME = "Application Sia"
    VERSION = '1.0'
    COPYRIGHT = 'Copyright(C) 2012-YEAR LOBSTR'
    DESCRIPTION = "Scraping Backend for Sia.ch"
    SHORT_DESCRIPTION = "Sia Scraping"

    def __init__(self):
        super(SiaBackend, self).__init__(self.APPNAME)
        self.setup_logging()
        self.fetcher = Fetcher()
        self.module = self.fetcher.build_backend("sia", params={})

        self.dao = DaoManager("sia")
        self.session, self.scoped_session = self.dao.get_shared_session()

    def main(self):
        for memberlist_page_no in range(253):
            members = self.module.iter_members(memberlist_page_no=memberlist_page_no)
            for member in members:
                #print(member.__dict__)
                #print(member.url)
                memberdetails = self.module.members_details(member=member)
                print(memberdetails.__dict__)
                if not self.session.query(Members).filter(Members.member_id == member.member_id).count():
                    self.session.add(member)
                    self.session.commit()

        print('---------------------------------------------')
        for offices_list_page_no in range(51):
            offices = self.module.iter_offices(offices_list_page_no=offices_list_page_no)
            for office in offices:
                #print(office.__dict__)
                officesdetails = self.module.offices_details(office=office)
                #print(officesdetails.__dict__)
                if not self.session.query(Offices).filter(Offices.office_id == office.office_id).count():
                    self.session.add(office)
                    self.session.commit()
                    self.session.refresh(office)

                office_database_id = office.id
                members_of_office = self.module.get_member_list()
                print('members_of_office:', members_of_office)
                if members_of_office:
                    for member_of_office in members_of_office:
                        #print('member_of_office:', member_of_office)
                        member_db_row = self.session.query(Members).filter(Members.member_id==member_of_office).first()
                        #print('member_db_row:', member_db_row)
                        if member_db_row:
                            #print(member_of_office)
                            member_database_id = member_db_row.id
                            member_office = MemberOffice(member_id = member_database_id, office_id = office_database_id)
                            self.session.add(member_office)
                            self.session.commit()
                        else:
                            print('Member does not exist')
                else:
                    print('Member does not exist')
        print('---------------------------------------------')
    

if __name__ == '__main__':
    my = SiaBackend()
    my.main()
