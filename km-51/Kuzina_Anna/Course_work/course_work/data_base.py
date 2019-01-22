import cx_Oracle
import pandas as pd

user_name = 'my_name'
user_password = 'my_name'
user_server = 'xe'


class Package:
    def __init__(self):
        self.connect = cx_Oracle.connect(user_name, user_password, user_server)
        self.cursor = self.connect.cursor()
        self.status = self.cursor.var(cx_Oracle.STRING)


class UserPackage(Package):
    def registration(self, user_login, user_name, user_password):
        self.cursor.callproc('user_package.add_user', [self.status, user_login, user_name, user_password])
        return self.status.getvalue()

    def login(self, user_login, user_password):
        sql = "SELECT user_package.login(:user_login, :user_password) FROM dual"
        res = pd.read_sql_query(sql, self.connect, params={'user_login': user_login, 'user_password': user_password})
        return res


class GiftPackage(Package):
    mutable = True

    def add(self, gift_name, gift_price, gift_desc):
        self.cursor.callproc('gift_package.add_gift', [self.status, gift_name, gift_price, gift_desc])
        return self.status.getvalue()

    def delete(self, gift_name):
        self.cursor.callproc('gift_package.del_gift', [self.status, gift_name])
        return self.status.getvalue()

    def update(self, gift_name, gift_price, gift_desc):
        self.cursor.callproc('gift_package.update_gift', [self.status, gift_name, gift_price, gift_desc])
        return self.status.getvalue()

    def get_all(self):
        return pd.read_sql_query('select * from gift_view', self.connect)

    def get_keys(self):
        return pd.read_sql_query('select gift_name from gift_view', self.connect).values[:, 0].tolist()

class FeaturePackage(Package):
    mutable = False

    def add(self, feature_name):
        self.cursor.callproc('feature_package.add_feature', [self.status, feature_name])
        return self.status.getvalue()

    def delete(self, feature_name):
        self.cursor.callproc('feature_package.del_feature', [self.status, feature_name])
        return self.status.getvalue()

    def get_all(self):
        return pd.read_sql_query('select * from feature_view', self.connect)

    def get_keys(self):
        return pd.read_sql_query('select feature_name from feature_view', self.connect).values[:, 0].tolist()


class CategoryPackage(Package):
    mutable = False

    def add(self, category_name):
        self.cursor.callproc('category_package.add_category', [self.status, category_name])
        return self.status.getvalue()

    def delete(self, category_name):
        self.cursor.callproc('category_package.del_category', [self.status, category_name])
        return self.status.getvalue()

    def get_all(self):
        return pd.read_sql_query('select * from category_view', self.connect)

    def get_keys(self):
        return pd.read_sql_query('select category_name from category_view', self.connect).values[:, 0].tolist()


class GiftCategoryPackage(Package):
    def add(self, category_name, gift_name):
        self.cursor.callproc('gift_category_package.add_category_to_gift', [self.status, category_name, gift_name])
        return self.status.getvalue()

    def delete(self, gift_name):
        self.cursor.callproc('gift_category_package.del_category_from_gift', [self.status, gift_name])
        return self.status.getvalue()

    def get_gift_list(self, gift_name):
        sql = "SELECT * FROM table(gift_category_package.get_gift_category_list(:gift_name))"
        res = pd.read_sql_query(sql, self.connect, params={'gift_name': gift_name})
        return res


class GiftFeaturePackage(Package):
    def add(self, feature_name, gift_name):
        self.cursor.callproc('gift_feature_package.add_feature_to_gift', [self.status, feature_name, gift_name])
        return self.status.getvalue()

    def delete(self, gift_name):
        self.cursor.callproc('gift_feature_package.del_feature_from_gift', [self.status, gift_name])
        return self.status.getvalue()

    def get_gift_list(self, gift_name):
        sql = "SELECT * FROM table(gift_feature_package.get_gift_feature_list(:gift_name))"
        res = pd.read_sql_query(sql, self.connect, params={'gift_name': gift_name})
        return res

    def get_advice(self, selected_features):
        res_list = []
        for feature in selected_features:
            sql = '''
            SELECT GIFT_VIEW.GIFT_NAME, GIFT_VIEW.GIFT_PRICE, GIFT_VIEW.GIFT_DESC
                FROM GIFT_FEATURE
                    join GIFT_VIEW on GIFT_FEATURE.GIFT_GIFT_NAME = GIFT_VIEW.GIFT_NAME
            where GIFT_FEATURE.FEATURE_FEATURE_NAME = :feature'''
            res_list.append(pd.read_sql_query(sql, self.connect, params={'feature': feature}))
        return pd.concat(res_list, ignore_index=True)

class UserFeaturePackage(Package):
    def add(self, feature_name, user_login):
        self.cursor.callproc('user_feature_package.add_feature_to_user', [self.status, feature_name, user_login])
        return self.status.getvalue()

    def delete(self, feature_name, user_login):
        self.cursor.callproc('user_feature_package.del_feature_from_user', [self.status, feature_name, user_login])
        return self.status.getvalue()

    def get_user_feature_list(self, user_login):
        sql = "SELECT user_feature_package.get_user_feature_list(:user_login) FROM dual"
        res = pd.read_sql_query(sql, self.connect, params={'user_login': user_login})
        return res
