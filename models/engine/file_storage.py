#!/usr/bin/python3
"""
Handles I/O, writing and reading, of JSON for storage of all class instances
"""
import json
from models import base_model, amenity, city, place, review, state, user
from datetime import datetime

strptime = datetime.strptime
to_json = base_model.BaseModel.to_json


class FileStorage:
    """Handles long term storage of all class instances"""
    CNC = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }
    """CNC - this variable is a dictionary with:
    keys: Class Names
    values: Class type (used for instantiation)
    """
    __file_path = './dev/file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns private attribute: __objects"""
        if cls:
            objects_dict = {}
            for class_id, obj in FileStorage.__objects.items():
                if type(obj).__name__ == cls:
                    objects_dict[class_id] = obj
            return objects_dict
        return FileStorage.__objects

    def new(self, obj):
        """Sets / updates in __objects the obj with key <obj class name>.id"""
        bm_id = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[bm_id] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        fname = FileStorage.__file_path
        d = {}
        for bm_id, bm_obj in FileStorage.__objects.items():
            d[bm_id] = bm_obj.to_json()
        with open(fname, mode='w', encoding='utf-8') as f_io:
            json.dump(d, f_io)

    def reload(self):
        """If file exists, deserializes JSON file to __objects, else nothing"""
        fname = FileStorage.__file_path
        FileStorage.__objects = {}
        try:
            with open(fname, mode='r', encoding='utf-8') as f_io:
                new_objs = json.load(f_io)
        except:
            return
        for o_id, d in new_objs.items():
            k_cls = d['__class__']
            FileStorage.__objects[o_id] = FileStorage.CNC[k_cls](**d)

    def delete(self, obj=None):
        """Deletes obj from __objects if it's inside"""
        try:
            del __objects[obj]
        except:
            return

    def close(self):
        """
        Calls the reload() method for deserialization from JSON to objects
        """
        self.reload()

    def get(self, cls, id):
        """Retrieves object based on class name and ID"""
        class_obj = self.all(cls)
        obj_str = str(cls) + "." + str(id)

        print("docstring test: {}".format(self.all.__doc__)) 
        try:
            return (class_obj[obj_str])
        except:
            return None 

    def count(self, cls=None):
        """Count the number of objects in storage"""
        return (len(self.all(cls)))
