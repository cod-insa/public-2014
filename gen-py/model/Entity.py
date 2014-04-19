class Entity:
    
    def __init__(self, id):
        self.id = id
        self.is_ai_object = False
        self.exist = True
        
    def get_owner_id(self):
        return self.owner_id
    
    def set_owner_id(self, id):
        self.owner_id = id
        
    def is_owned(self):
        return self.id != 0
    
    def is_friend(self, other):
        return self.id == other.get_owner_id()
    
    def is_enemy(self):
        return self.id > 0 and self.id != other.get_owner_id()
    
    def get_id(self):
        return self.id
    
    def set_ai_object(self, ai):
        self.is_ai_object = ai
        
    def set_existe(self, ex):
        self.exist = ex