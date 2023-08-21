import requests
from pprint import pprint
import json
from tqdm import tqdm

# формат запроса API VK: https://api.vk.com/method/<METHOD>?<PARAMS> HTTP/1.1

class VkFotoDownload:
    
    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id
    
    def get_photo(self, count=5):
        url = 'https://api.vk.com/method/photos.get'
       
        photo_input = input('Сколько фоток скачать? (по умолчанию 5, нажмите Enter):')
        try:
            count = int(photo_input)
        except ValueError:
            pass
            
        params = {
            'owner_id' : self.user_id,
            'album_id' : 'profile',
            'access_token' : self.token,
            'extended' : '1',
            'photo_sizes' : '1',
            'count' : count,
            'v' : '5.131'
        }

        result = requests.get(url=url, params=params).json()
        all_photo_count = result['response']['count']
        if count > all_photo_count:
            print(f'ERRORE.., У Вас в ВК {all_photo_count} фото. Попробуйте заново')
            return self.get_photo()
        return result

    
    #Значения type(размер) для фото: s, m, x, o, p, q, r, y, z, w (по возрастанию)
    #Получаем словарь ИМЯ ФОТО (кол-во лайков) : URL (фото с макс. размером) и список для записи в файл .json  
    def get_all_photo(self):
        photo_info = self.get_photo()
        max_size_photo = {}
        file_json = []
        for photo in photo_info['response']['items']:
            for size in photo['sizes'][-1:]:
                photo_info_json = {}
                if photo['likes']['count'] not in max_size_photo.keys():
                    photo_info_json['file_name'] = f"{photo['likes']['count']}.jpg"
                    max_size_photo[photo['likes']['count']] = size['url']
                else:
                    photo_name = photo['likes']['count'] + photo['date']
                    photo_info_json['file_name'] = f"{photo['likes']['count']}_{photo['date']}.jpg"
                    max_size_photo[f"{photo['likes']['count']}_{photo['date']}"]= size['url']
            
            photo_info_json['size'] = size['type']
            file_json.append(photo_info_json)
    
        # Записываем данные о всех скачанных фоторафиях в файл .json    
        with open('photos_vk.json', 'w') as file:
            json.dump(file_json, file, indent=2)
        
        return max_size_photo
    
# URL запроса на Yandex: https://cloud-api.yandex.net/v1/disk/resources?path=vk

class YaDiskUploader:
    
    def __init__(self, OAuth):
        self.OAuth = OAuth
    
    #создаем папку на яндекс диске
    def put_folder_creation(self):
        folder_name = str(input('Ведите имя папки для сохранения фото из ВК: '))
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path' : f'{folder_name}'}
        headers = {'Authorization' : f'OAuth {self.OAuth}'}
        response = requests.put(url=url, params=params, headers=headers).json()
        return folder_name
    
    #сохраняем фото на яндекс диск
    def save_to_disk(self):
        folder_name = self.put_folder_creation()
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        for name, path in max_size_photo.items():
            for i in tqdm(max_size_photo): #прогресс-бар
                pass
            headers = {'Authorization' : f'OAuth {self.OAuth}'}
            params = {
                'url' : path,
                'path' : f'{folder_name}/{name}.jpg'
            }
            
            response = requests.post(url=url, params=params, headers=headers)
            # print(response.json())
        

if __name__ == '__main__':
    id_vk = input('Введите свой ID от VK:')
    user_vk = VkFotoDownload(token_vk, id_vk)
    # pprint(user_vk.get_photo())
    max_size_photo = user_vk.get_all_photo()
    
    user_ya = YaDiskUploader(OAuth_ya)
    user_ya.save_to_disk()