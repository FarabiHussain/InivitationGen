

class Guest:
    def __init__(self, properties=None) -> None:
        self.properties = properties

    def is_empty(self) -> bool:
        if self.properties is None:
            return True

        for prop in (self.properties.keys()):
            if prop is None or len(prop.strip()) == 0:
                return True

        return False

    def set_prop(self, prop: str, value: str) -> bool:
        try:
            self.properties[prop] = value
        except Exception as e:
            print(e)
            return False

        return True
    
    def get_prop(self, prop: str) -> str:
        try:
            return str(self.properties[prop])
        except Exception as e:
            print(e)
