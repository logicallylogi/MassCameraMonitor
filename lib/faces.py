from numpy import ndarray, array
import cv2
from face_recognition import face_locations, face_encodings, face_distance
from lib.db import Database

class Face:
    def __init__(self, db:Database, image:array = None, location:list = None,  encoding:ndarray = None):
        self.connection = db
        if location:
            self.location = location
        if encoding:
            self.encoding = encoding
        elif location:
            self.encoding = face_encodings(image, location)[0]
        elif image:
            self.encoding = face_encodings(image)[0]
        else:
            raise TypeError("Not enough information was provided to guess the encoding")
                    
        self.information = self.connection.get_face(face=self.encoding)
        
        if not self.information:
            self.information = self.connection.insert_face(face_data=self.encoding)
            
        self.id = self.information['id']


    def compare(self, knowns:list):
        face_distance(knowns, self.encoding)
        
    def identify(self, frame:array):
        top, right, bottom, left = self.location
        new_frame = cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        new_frame = cv2.rectangle(new_frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        new_frame = cv2.putText(new_frame, self.id, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        return new_frame
        
        
def get_all(image:array, db:Database) -> list:
    output = []
    locations = face_locations(image)
    for location in locations:
        output.append(Face(db, image=image, location=location))
    return output