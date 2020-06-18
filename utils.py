from telegram import ReplyKeyboardMarkup, KeyboardButton
from clarifai.rest import ClarifaiApp

import settings
import pprint


def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Прислать координаты', request_location=True)

    my_keyboard = ReplyKeyboardMarkup([['/start', '/stop', '/sith'],
                                       [contact_button, location_button, 'Сменить аватар'],
                                      ['Заполнить анкету']])
    return my_keyboard


def is_sword(filename):
    image_has_sword = False
    app = ClarifaiApp(api_key=settings.CLARIFAI_API_KEY)
    model = app.public_models.general_model
    response = model.predict_by_filename(filename, max_concepts=5)

    pp =  pprint.PrettyPrinter(indent=4)
    pp.pprint(response)
    if response['status']['code'] == 10000:
        for concept in response['outputs'][0]['data']['concepts']:
            if concept['name'] == 'sword':
                print("Sword is here!")
                image_has_sword = True
    return image_has_sword


if __name__=="__main__":
    is_sword('sith/undeaddu2.jpg')