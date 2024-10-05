import sqlalchemy as db
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import Session
from data.models import Base, Room

class DbRepository:
    def __init__(self, url: str) -> None:
        self.engine = db.create_engine(url)
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
            Base.metadata.create_all(self.engine)
            
    def get_free_room(self): 
        with Session(self.engine) as session:
            return session.query(Room).filter(Room.is_busy == 0).one_or_none()
    
    def create_room(self, chat_id:int): 
        with Session(self.engine) as session, session.begin():
            session.add(Room(chat_id_1=chat_id))
            
    def add_user_to_room(self, room_id, chat_id:int):
        with Session(self.engine) as session, session.begin():
            room = session.get(Room, room_id)
            room.chat_id_2 = chat_id
            room.is_busy = True
    
    def get_room_by_chat_id(self, chat_id:int):
        with Session(self.engine) as session:
            return session.query(Room).filter((Room.chat_id_1 == chat_id) | (Room.chat_id_2 == chat_id)).one_or_none()
    
    def delete_room(self, room:Room):
        with Session(self.engine) as session, session.begin():
            session.delete(room)

        
    
            
