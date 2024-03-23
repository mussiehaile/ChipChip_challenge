from dataclasses import dataclass, field

@dataclass
class ConfigStaticFiles:
    DB_DATABASE:str ="my_db"
    DB_USER:str ="user"
    DB_PASSWORD:str="xxx"
    vegitable_discription: str = f"Vegetables are parts of plants that are consumed by humans or other animals as food."
    fruit_discription:str = f"Fruits are The sweet and fleshy product of a tree or other plant that contains seed and can be eaten as food."
