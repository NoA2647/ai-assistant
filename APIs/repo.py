import requests as r
from requests.structures import CaseInsensitiveDict
import os
import json
import logging

logging.basicConfig(filename='log.log',
                    level=logging.DEBUG,
                    format='%(asctime)s | %(name)s | %(levelname)s | %(module)s | %(lineno)d | %(message)s')


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
        response = None
        try:
            response = r.post(self.root + self.auth_url, headers=self.header, json=data).json()
        except Exception as e:
            logging.exception(e)
        logging.debug(f"response of auth namava:\n{response}")
        if response['succeeded']:
            self.header["Cookie"] = "auth_v2=" + response['result']
        else:
            return False

    def info(self):
        response = None
        try:
            response = r.get(self.root + self.info_url, headers=self.header).json()
        except Exception as e:
            logging.exception(e)
        logging.debug(f"response of info namava:\n{response}")
        if response['succeeded']:
            return response['result']
        else:
            return None

    def search(self, parameters, count=5, page=1):
        response = None

        header = CaseInsensitiveDict()
        header["Content-type"] = "application/json"
        header["User-Agent"] = "PostmanRuntime/7.29.0"
        data = f"count={count}&page={page}"
        for parameter in parameters.keys():
            if parameters[parameter] is not None:
                para = parameter + "=" + parameters[parameter]
                data = "&".join([data, para])
        try:
            response = r.get(self.root + self.search_url + data, headers=header).json()
        except Exception as e:
            logging.exception(e)
        logging.debug(f"response of info namava:\n{response}")
        if response['succeeded']:
            if response['result']['result_items'][0]['total'] != 0:
                if response['result']['result_items'][0]['groups']['Media']['total'] != 0:
                    logging.debug(
                        f"items of response of info namava:\n{response['result']['result_items'][0]['groups']['Media']['items']}")
                    return response['result']['result_items'][0]['groups']['Media']['items']
        else:
            return None

    def videoInfo(self, video_id, video_type, video_url):
        film_detail_movie = f"/api/v2.0/medias/{video_id}/single-movie/"
        film_detail_series = f"/api2/movie/{video_id}"

        video_info = {"id": None, "type": None, "name": None, "story": None, "score": None, "trailer": None,
                      "duration": None, "language": [],
                      "subtitle": [], "url": video_url}
        logging.debug(f"request for video_info of namava:\n{video_info}")
        if video_type == "Series":
            response = r.get(self.root + film_detail_series, headers=self.header)
            logging.debug(f"response of video_info namava:\n{response.text}")
            if response.text != "":
                response = response.json()
                video_info['type'] = 'series'
                video_info['id'] = response['PostId']
                video_info['name'] = response['Name']
                for item in response['PostTypeAttrValueModels']:
                    if '????????????' in item['Name']:
                        video_info['score'] = float(item['Value'])
                video_info['story'] = response['ShortDescription']
                logging.debug(f"fill video_info:\n{video_info}")
                return video_info
            else:
                return None

        else:
            response = r.get(self.root + film_detail_movie, headers=self.header).json()
            logging.debug(f"response of video_info namava:\n{response}")
            if response['succeeded'] and response['result'] is not None:
                video_info['type'] = 'movie'
                video_info['id'] = response['result']['id']
                video_info['name'] = response['result']['caption']
                video_info['story'] = response['result']['story']
                video_info['duration'] = response['result']['mediaDuration']
                if response['result']['trailerVideoUrl'] is not None:
                    video_info['trailer'] = self.root + response['result']['trailerVideoUrl']
                for voice in response['result']['voiceList']:
                    video_info['language'].append(voice['languageCulture'])
                for subtitle in response['result']['subtitleList']:
                    video_info['subtitle'].append(subtitle['languageCulture'])
                logging.debug(f"fill video_info:\n{video_info}")
                return video_info
            else:
                return None

    def convertor(self, movie, map):

        data = {}
        logging.info("open namava_api_map.json")
        with open(os.path.join(map.getDataPath(), 'namava_api_map.json')) as f:
            file = json.load(f)

        data['query'] = movie["name"]

        if movie['type'] == "????????":
            data['type'] = 'movie'
        elif movie['type'] == "??????????":
            data['type'] = 'series'
        else:
            data['type'] = 'all'

        if movie['genre'] != (None,):
            data['subcategories'] = ','.join(movie['genre'])

        for lang in file['language'].keys():
            if lang in movie["language"]:
                data['language'] = file['language'][lang]
                break

        if movie["title_group"] == "????????":
            data['searchOrderType'] = 1
        elif movie["title_group"] == "????????":
            data['searchOrderType'] = 4

        if movie["start_date"] != (None,):
            if int(movie["start_date"]) >= 1900:
                startAD = int(movie["start_date"])
                startP = 1279 + int(movie["start_date"]) - 1900
            else:
                startAD = 1900 + int(movie["start_date"]) - 1279
                startP = int(movie["start_date"])
            if int(movie["end_date"]) >= 1900:
                endAD = int(movie["end_date"])
                endP = 1279 + int(movie["end_date"]) - 1900
            else:
                endAD = 1900 + int(movie["end_date"]) - 1279
                endP = int(movie["end_date"])

            if startAD <= endAD:
                data['ADProductionYear'] = str(startAD) + '-' + str(endAD)
                data['PersianProductionYear'] = str(startP) + '-' + str(endP)

        countries = {
            "??????????": "iran",
            "????????????": "amrica",
            "??????": "india",
            "??????": "china",
            "??????": "korea",
            "????????": "japan",
            "??????????": "turkey",
            "??????????": "german",
            "????????????": "france",
            "??????????????": "italia",
            "????????????": "england",
            "??????????????": "spain",
            "????????????????": "denmark",
            "????????": "sweden",
            "??????????": "russia",
            "????????????????": "argentia",
            "??????????": "Mexico",
            "??????????": "brazil",
            "????????????????": "austrilia",
            "????????????": "canada"
        }

        if movie["country_name"] != (None,):
            for count in countries.keys():
                if count in movie["country_name"]:
                    data['CountryProducer'] = countries[count]

        logging.debug(f"convertor of namava, data:\n{data}")
        return data

# videoId = 147019
# token = auth("+989368188589", "namava6276")
# print(videoInfo(147019))
# search({"type":"movie","language":"Persian", "searchOrderType":"2", "dubs":"2"})
