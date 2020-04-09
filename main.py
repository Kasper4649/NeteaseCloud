import execjs
import requests


def get_data(d):
    e = "010001"
    f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4" \
        "ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cf" \
        "e4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
    g = "0CoJUm6Qyw8W8jud"

    with open("CryptoJS.js", "r", encoding="utf-8") as file:
        js = file.read()

    res = execjs.compile(js).call("d", d, e, f, g)
    return res


def get_response(url, res):
    data = {
        "params": res["encText"],
        "encSecKey": res["encSecKey"]
    }
    response = requests.post(url, data=data)
    return response.json()


def get_songs(url):
    search_keyword = input("搜索内容：")
    d = '{"hlpretag":"<span class=\\"s-fc7\\">","hlposttag":"</span>","s":"' + search_keyword + \
        '","type":"1","offset":"0","total":"true","limit":"30","csrf_token":""}'
    res = get_data(d)
    songs = get_response(url, res)["result"]["songs"]
    return songs


def get_song(url, _id):
    d = '{"ids":"[' + str(_id) + ']","level":"standard","encodeType":"aac","csrf_token":""}'
    data = get_data(d)

    res = get_response(url, data)
    download_url = res["data"][0]["url"]
    download_id = res["data"][0]["id"]

    if download_url is not None:
        with open(str(download_id) + ".m4a", "wb") as f:
            f.write(requests.get(download_url).content)
    else:
        print("无下载地址：", download_id)


def main():
    search_url = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="
    song_url = "https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token="

    songs = get_songs(search_url)

    for song in songs:
        get_song(song_url, song["id"])


if __name__ == '__main__':
    main()
