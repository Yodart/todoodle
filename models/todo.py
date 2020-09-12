class Todo:
    def __init__(self, id, title, completed, created_at):
        self.title = title
        self.completed = completed
        self.id = id
        self.created_at = created_at

    @staticmethod
    def fromJson(json):
        return Todo(id=json['id'], title=json['title'], completed=json['completed'], created_at=json['created_at'])

    def toJson(self):
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed,
            'created_at': self.created_at,
        }
