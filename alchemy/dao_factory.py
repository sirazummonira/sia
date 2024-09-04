from mbackend.alchemy.scoped_dao.dao_factory import DaoFactory

from .tables import create_all

from mbackend.tools.db_tools.decorators import dbconnect, dbconnect_noexpire, dbconnect_noclosing, dbconnect_noclosingandsession, dbconnect_sharedsession
from pytz import timezone
import datetime
from sqlalchemy import and_, or_

from sqlalchemy.orm import scoped_session


class DaoFactory(DaoFactory):

    def __init__(self, database_name, engine_config=None):
        self.timezone = timezone('Europe/Paris')
        super(DaoFactory, self).__init__(database_name, engine_config)
        create_all(self.engine)

    def get_shared_session(self):
        ScopedSession = scoped_session(self.session_factory)
        session = ScopedSession()
        return session, ScopedSession


