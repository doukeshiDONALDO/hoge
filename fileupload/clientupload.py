# -*- coding: utf-8 -*-
import requests

# ポイント1
#XLSX_MIMETYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
MIMETYPE = 'text/plain'

# <form action="/data/upload" method="post" enctype="multipart/form-data">
#   <input type="file" name="uploadFile"/>
#   <input type="submit" value="submit"/>
# </form>

# main
if __name__ == "__main__":

    # ポイント2
    fileName = 'test.txt'
    fileDataBinary = open(fileName, 'rb').read()
    files = {'uploadFile': (fileName, fileDataBinary, MIMETYPE)}

    # ポイント3
    url = 'http://localhost:3000/data/upload'
    response = requests.post(url, files=files)

    print(response.status_code)
    print(response.content)
