import cv2 as cv

import os

import state_check.src as state 


class EventsChecker:

    def __init__(self, frame: cv.typing.MatLike, text_coords_dict: dict) -> None:
        self.frame = frame
        self.templates_dir = '../static'
        self.text_coords_dict = text_coords_dict

    def check_invite_in_dungeon(self, event_type: str='invite') -> bool:
        return src.event_listeners.check_clicable_event_button(self.frame, event_type)
    
    def __start_with_squad_complite_flag(self, text) -> bool:
        flag_confirm_squad_level = state.search_text_frame.confirm_squad_level(text)
        return flag_confirm_squad_level
    
    def star_squad_complite_coords(self) -> tuple:
        for text in self.text_coords_dict.keys():
            flag = self.__star_squad_complite_coords(text)
            if flag:
                return self.text_coords_dict[text]
    
