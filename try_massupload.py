from utils import get_access_token, book_upload
import os


ret = get_access_token("user1", "password1", govdatahub="govdatahub.ru")
access_token = ret.get("access_token")
assert len(access_token) == 331, "Error in `get_access_token`"
print(access_token)

# print(os.listdir('/media/pascal65536/1TB/Books/'))

pth = "/media/pascal65536/1TB/Books/"
for root, dirs, files in os.walk(pth):
    for f in files:
        book_path = os.path.join(root, f)
        if book_path.endswith(".pdf"):
            ret = book_upload(book_path, access_token, govdatahub="govdatahub.ru")
            print(ret)
