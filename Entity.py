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


    def is_complete(self) -> tuple[bool, list[str]]:
        if self.properties is None:
            return False

        invalid_props = []

        for prop in self.properties.keys():
            if prop is None or len(self.properties[prop].strip()) == 0:
                invalid_props.append(prop)

        if len(invalid_props) is not 0:
            return (False, invalid_props)

        return (True, invalid_props)
    
    
    def is_prop_blank(self, prop: str = "") -> bool:
        if prop is None or len(self.properties[prop].strip()) == 0:
            return True
        
        return False


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

        # ignore the following datepickers as they default to today's dates
        valid_props = self.get_valid_props()
        valid_props.remove("arrival")
        valid_props.remove("departure")
        valid_props.remove("birth")

        # retrieve unfilled fields 
        empty_fields = self.is_complete()[1]

        # find fields that should be filled
        # if all remaining fields are unfilled, the Guest object is empty
        if len(set(valid_props) - set(empty_fields)) == 0:
            return True

        return False


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


    def is_empty(self) -> bool:
        valid_props = self.get_valid_props()
        valid_props.remove("birth") # defaults to today's dates
        valid_props.remove("bearer") # not needed in host 2
        valid_props.remove("attached") # optional
        valid_props.remove("relation_to_other_host") # not needed when 2nd host does not exist

        # retrieve unfilled fields 
        empty_fields = self.is_complete()[1]

        # find fields that should be filled
        # if all remaining fields are unfilled, the Guest object is empty
        if len(set(valid_props) - set(empty_fields)) == 0:
            return True

        return False

