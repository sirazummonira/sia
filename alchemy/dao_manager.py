from mbackend.alchemy.scoped_dao.dao_manager import DaoManager
from .dao_factory import DaoFactory


class DaoManager(DaoManager):

    def __init__(self, table_name, engine_config=None):
        super(DaoManager, self).__init__()
        self.daoFactory = DaoFactory(table_name, engine_config)

    def get_shared_session(self):
        return self.daoFactory.get_shared_session()
