from utils import get_access_token, authors_get, author_post, author_get, author_put, authors_delete


ret = get_access_token("user1", "password1")
access_token = ret.get("access_token")
print(access_token)

ret = authors_get(access_token)
print(ret)

json_data = {"name": "А.С. Пушкин"}
ret = author_post(json_data, access_token)
print(ret)


ret = author_get('1', access_token)
print(ret)
ret = author_get('2', access_token)
print(ret)


json_data = {"name": "А.С. Пушкин", "name_eng": "Alexander Pushkin"}
ret = author_put('2', json_data, access_token)
print(ret)

ret = author_get('2', access_token)
print(ret)


ret = authors_delete('2', access_token)
print(ret)

ret = author_get('2', access_token)
print(ret)
