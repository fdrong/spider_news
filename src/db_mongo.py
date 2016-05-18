#coding=utf-8

import pymongo


class MongoDB(object):
    def __init__(self, config):
        # self.connection = pymongo.Connection(host=host, port=port, slave_okay=slaveOk)
        self.connection = pymongo.MongoClient(host=config.Host, port=config.Port)
        self.db = self.connection[config.DbName]
        if config.User and config.PassWd:
            self.db.authenticate(config.User, config.PassWd)

    def insert(self, collection, dic):
        self.db[collection].insert(dic)

    def count(self, collection, dic):
        return self.db[collection].find(dic).count()

    def find(self, collection, dict_search):
        cursor = self.db[collection].find(dict_search)
        return cursor

    def find_one(self, collection, dict_search):
        dict_value = self.db[collection].find_one(dict_search)
        return dict_value

    def remove(self, collection, dic):
        self.db[collection].remove(dic)

    def ensure_index(self, collection, lst_tuple):
        self.db[collection].ensure_index(lst_tuple)

    def drop_index(self, collection, lst_tuple):
        self.db[collection].drop_index(lst_tuple)

    def update(self, collection, dict_key, document, multi=False):
        self.db[collection].update(dict_key, document, multi=multi)

    def change_db(self, database):
        """
        切换数据库
        """
        self.db = self.connection[database]
        
    def find_sort(self, collection, dict_search, field, sortflag='asc'):
        if sortflag == 'desc':
            cursor = self.db[collection].find(dict_search).sort(field, pymongo.ASCENDING)
        else:
            cursor = self.db[collection].find(dict_search).sort(field, pymongo.DESCENDING)
        return cursor

    def rename_column(self, collection, sourcename, currentname):
        self.db[collection].update({}, {"$rename":{sourcename:currentname}}, False, True)
    
    def group_by(self, collection="", key={}, condition={}, initial={"count": 0},
                    reduce="function(obj, prev){prev.count++;}"):

        cursor = self.db[collection].group(key, condition, initial, reduce)
        return cursor

    @staticmethod
    def get_collectionnames(self):
        return self.db.collection_names()

    @staticmethod
    def get_db(self):
        return self.db


# def test():
#     mdb = db_mongodb('183.57.42.116', 27017, "crawl_data")
#     tt = mdb.db_find_one("chinaweath_20141016", {"cpdjbm":"C1010314005453"})
#     print tt
#     lt = mdb.db_group_by("news_content", {"main_id":1})
#     print lt
# test()