import hashlib


def simplify(value):
    try:
        return int(value)
    except:
        return float(value)


class MontageError(Exception):
    pass


class Struct(object):

    def __init__(self, command, string):
        if 'struct' in string:
            string = string[8:-1]

            strings = {}
            while True:
                try:
                    p1 = string.index('"')
                    p2 = string.index('"', p1+1)
                    substring = string[p1+1:p2]
                    key = hashlib.md5(substring).hexdigest()
                    strings[key] = substring
                    string = string[:p1] + key + string[p2+1:]
                except:
                    break

            key = hashlib.md5(substring).hexdigest()

            for pair in string.split(', '):
                key, value = pair.split('=')
                if value in strings:
                    self.__dict__[key] = strings[value]
                else:
                    self.__dict__[key] = simplify(value)

            if self.stat == "ERROR":
                raise MontageError("%s: %s" % (command, self.msg))
        else:
            raise Exception("The following error occured:\n\n" + string)
