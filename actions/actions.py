import requests
import re
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset

class ActionDetectLanguage(Action):
    def name(self) -> Text:
        return "action_detect_language"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '')
        arabic_pattern = re.compile(r'[\u0600-\u06FF]')
        
        if arabic_pattern.search(user_message):
            language = "ar"
        else:
            language = "en"
        
        return [SlotSet("language", language)]

class ActionGetWeather(Action):
    def name(self) -> Text:
        return "action_get_weather"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        location = tracker.get_slot("location")
        language = tracker.get_slot("language") or "en"
        
        if not location:
            if language == "ar":
                dispatcher.utter_message(text="من فضلك أخبرني اسم المدينة")
            else:
                dispatcher.utter_message(text="Please tell me the city name")
            return []
        
        city_translation = {
            "القاهرة": "Cairo", "الأسكندرية": "Alexandria", "الجيزة": "Giza",
            "الأقصر": "Luxor", "أسوان": "Aswan", "شرم الشيخ": "Sharm el Sheikh",
            "الغردقة": "Hurghada", "مرسى علم": "Marsa Alam", "دهب": "Dahab"
        }
        
        city = city_translation.get(location, location)
        api_key = "36a25cd28648d49f90a5fef4aa56de94"
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ar"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                
                if language == "ar":
                    message = f"الطقس في {location}: {description}، درجة الحرارة {temp}°C"
                else:
                    message = f"Weather in {city}: {description}, temperature {temp}°C"
                
                dispatcher.utter_message(text=message)
            else:
                if language == "ar":
                    dispatcher.utter_message(text=f"ما لقيتش مدينة باسم '{location}'")
                else:
                    dispatcher.utter_message(text=f"Couldn't find city '{city}'")
        except:
            if language == "ar":
                dispatcher.utter_message(text="خطأ في الاتصال بخدمة الطقس")
            else:
                dispatcher.utter_message(text="Weather service error")
        
        return [SlotSet("location", location)]

class ActionResetSlots(Action):
    def name(self) -> Text:
        return "action_reset_slots"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [AllSlotsReset()]