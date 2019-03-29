

def debug(*args):
    print("==[ DEBUG ]===>", *args)

class ID_Verifier:
    def __init__(self):
        self.ids = []

    def check(self, id):
        assert id not in self.ids, "This ID is already in use."
        self.ids.append(id)
        self.ids.sort()
        return id

    def debug(self, name=""):
        debug(str(name)+":", self.ids)
