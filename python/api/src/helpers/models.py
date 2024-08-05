

class BaseModel(object):

    __json_fields_block__ = []

    def to_json(self):
        attributes = filter(lambda a: not a.startswith('__'), dir(self))
        attributes = filter(lambda a: a not in ['to_json'], attributes)
        attributes = filter(lambda a: a not in self.__json_fields_block__, attributes)

        json_dict = {}
        for attribute in attributes:
            json_dict[attribute] = getattr(self, attribute)
        return json_dict
