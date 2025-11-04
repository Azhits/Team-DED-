import cv2 as cv
import logging
import os


class Listener:

    def __init__(self, event_logs=None, decision=None):
        self.events = event_logs
        self.decisions = decision

    def to_dataloader(self):
        pass



if __name__ == '__main__':
    listener = Listener()