from DBbridge.Escritor import Escritor
import codecs
import json


class FileTweetsWriter(Escritor):

    def __init__(self, file_name):
        super(FileTweetsWriter, self).__init__(1)
        self.file_name = file_name
        self.fout = None

    def escribe(self, data):
        if self.fout is None:
            self.fout = codecs.open(self.file_name, "w", "utf-8")

        for element in data:
            self.fout.write(json.dumps(element))
            self.fout.write("\n")