from pymongo import MongoClient 

class dbconnection:
    def __init__(self) -> None:
        connection_string = "mongodb://localhost:27017"
        client = MongoClient(connection_string)
        self.db_marketplace = client['kci_db']

    def insert_many(self, nama_koleksi, dokumen):
        new_product_list = map(dict, set(tuple(x.items()) for x in dokumen))
        print(new_product_list)
        self.db_marketplace.nama_koleksi.insert_many(new_product_list)
        
class dstokopedia(dbconnection):
    def __init__(self) -> None:
        # DbConnection().__init__()
        super().__init__()

    def insert_many(self, dokumen):
        return super().insert_many('tokopedia', dokumen)
    
    def get_all(self):
        return self.db_marketplace.tokopedia.find({})
    
class dsbukalapak(dbconnection):
    def __init__(self) -> None:
        # DbConnection().__init__()
        super().__init__()

    def insert_many(self, dokumen):
        return super().insert_many('bukalapak', dokumen)
    
    def get_all(self):
        return self.db_marketplace.bukalapak.find({})    

class dsshopee(dbconnection):
    def __init__(self) -> None:
        # DbConnection().__init__()
        super().__init__()

    def insert_many(self, dokumen):
        return super().insert_many('shopee', dokumen)
    
    def get_all(self):
        return self.db_marketplace.shopee.find({})    