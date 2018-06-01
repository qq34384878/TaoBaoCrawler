import pymongo

from app.config import MONGO_URL, MONGO_DB, TAOBAO_COLLECTION

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def save_to_mongo(result, collection):
    """

    :param result: 需要入库的数据
    :param collection: 需要入到哪张表
    :return: 入库结果
    """
    try:
        if db[collection].insert(result):
            print('存储到MongoDB成功', result)
    except Exception:
        print('存储到MongoDB失败')


if __name__ == '__main__':
    user = None
    result = db[TAOBAO_COLLECTION].find_one({"id": user, })
    # result = db[TAOBAO_COLLECTION].find_one({"id": user, })
    print(result)
    print(type(result))
