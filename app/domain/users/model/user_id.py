from dataclasses import dataclass


@dataclass
class UserId:
    id: str

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
