from GUI import *

class Entity:
    def __init__(self, new_props: dict = {}, valid_props: list = []) -> None:
        self.valid_props = valid_props
        self.properties = {}

        if new_props is None:
            return

        for prop in new_props:
            if prop in self.valid_props:
                self.properties[prop] = new_props[prop]
            else:
                print(f"{prop} is not a valid property of Guest object.")


    def is_filled(self) -> tuple:
        if self.properties is None:
            return False

        invalid_props = []

        for prop in self.properties.keys():
            if prop is None or len(self.properties[prop].strip()) == 0:
                invalid_props.append(prop)

        if len(invalid_props) is not 0:
            return (False, invalid_props)

        return (True, None)


    def set(self, prop: str, value: str) -> bool:
        if prop in self.valid_props:
            self.properties[prop] = value
            return True
        else:
            print(f"{prop} is not a valid property of Guest object.")

        return False


    def get(self, prop: str) -> str:
        try:
            return str(self.properties[prop])
        except Exception as e:
            print(e)


    def get_valid_props(self) -> list[str]:
        return self.valid_props


    def __str__(self) -> str:
        output = ""
        for prop in self.valid_props:
            output += f"{prop.ljust(25)}\t{self.properties[prop]}\n"
        output += "\n"

        return output


class Guest(Entity):
    def __init__(self, new_props: dict = None) -> None:
        self.valid_props = [
            "name",
            "birth",
            "citizenship",
            "passport",
            "address",
            "phone",
            "occupation",
            "purpose",
            "arrival",
            "departure",
            "relationship_to_host1",
            "canadian_address",
        ]

        super().__init__(new_props, self.valid_props)

    def is_empty(self) -> bool:
        valid_props = self.get_valid_props()
        valid_props.remove("arrival")
        valid_props.remove("departure")
        valid_props.remove("birth")


class Host(Entity):
    def __init__(self, new_props: dict = None) -> None:
        self.valid_props = [
            "name",
            "birth",
            "status",
            "passport",
            "address",
            "phone",
            "occupation",
            "email",
            "relation_to_other_host",
            "bearer",
            "attached",
        ]

        super().__init__(new_props, self.valid_props)

