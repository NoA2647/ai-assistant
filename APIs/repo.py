import requests as r
from requests.structures import CaseInsensitiveDict


class Namava:
    def __init__(self):
        self.root = "https://www.namava.ir"
        self.auth_url = "/api/v1.0/accounts/login/by-phone"
        self.info_url = "/api/v1.0/users/info"
        self.profile_url = "/api/v2.0/users/profiles"
        self.search_url = "/api/v3.0/search/advance?"
        self.header = CaseInsensitiveDict()
        self.header["Content-type"] = "application/json"
        self.header["User-Agent"] = "PostmanRuntime/7.29.0"

    def auth(self, username, password):
        data = {"UserName": username,
                "Password": password}

        response = r.post(self.root + self.auth_url, headers=self.header, json=data).json()
        if response['succeeded']:
            self.header["Cookie"] = "auth_v2=" + response['result']
        else:
            return False

    def info(self):
        response = r.get(self.root + self.info_url, headers=self.header).json()
        if response['succeeded']:
            return response['result']
        else:
            return None

    def search(self, parameters, count=20, page=1):
        header = CaseInsensitiveDict()
        header["Content-type"] = "application/json"
        header["User-Agent"] = "PostmanRuntime/7.29.0"
        data = f"count={count}&page={page}"
        for parameter in parameters.keys():
            if parameters[parameter] is not None:
                para = parameter + "=" + parameters[parameter]
                data = "&".join([data, para])
        response = r.get(self.root + self.search_url + data, headers=header).json()

        if response['succeeded']:
            return response['result']['result_items'][0]['groups']['Media']['items']
        else:
            return None

    def videoInfo(self, video_id):
        film_detail = f"/api/v2.0/medias/{video_id}/single-movie/"

        video_info = {"id": None, "caption": None, "story": None, "trailer": None, "duration": None, "language": [],
                      "subtitle": []}

        response = r.get(self.root + film_detail, headers=self.header).json()
        if response['succeeded']:
            video_info['id'] = response['result']['id']
            video_info['caption'] = response['result']['caption']
            video_info['story'] = response['result']['story']
            video_info['duration'] = response['result']['mediaDuration']
            video_info['trailer'] = self.root + response['result']['trailerVideoUrl']
            for voice in response['result']['voiceList']:
                video_info['language'].append(voice['languageCulture'])
            for subtitle in response['result']['subtitleList']:
                video_info['subtitle'].append(subtitle['languageCulture'])

            return video_info
        else:
            return None

    # videoId = 147019
    # token = auth("+989368188589", "namava6276")
    # print(videoInfo(147019))
    # search({"type":"movie","language":"Persian", "searchOrderType":"2", "dubs":"2"})
