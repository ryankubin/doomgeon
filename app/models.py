import json
from random import randint, choice

from app import db
from app import app, mapFunctions
from sqlalchemy.orm import relationship

# Represents the adventurer exploring the dungeon.  
class Player(db.Model):
    __table_args__ = {'extend_existing': True }
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    currentRoom = db.Column(db.Integer, nullable=True)
    
    dungeons = db.relationship('DungeonMap', backref='owner', lazy='dynamic')
    
    def __repr__(self):
        return '<Player {0}>'.format(self.name)
    
    # Returns dictionary of all relevant player information
    def getStatus(self):
        cRoom = DungeonRoom.query.filter_by(id=self.currentRoom).first()         
        return {"map": {"adjacent_rooms": cRoom.getNeighborsJSON(), "currentRoom" : cRoom.getJSON(), "floor": "{0}".format(cRoom.floor)}, "name":"{0}".format(self.name)}
    
    # Returns the dungeon being attempted
    def getDungeon(self):
        return DungeonMap.query.filter_by(owner=self).first()
    
    # Creates a dungeon to explore, along with all of its rooms.  Will add the adventurer to the beginning room.
    def createDungeon(self, floor):
        try:
            map = DungeonMap(owner = self, floor = floor, rooms = '{}')
            db.session.add(map)
            db.session.commit()
            rooms = []
            # Create a semi random set of rooms
            for i in range(0, randint(10,20)):
                roomName = mapFunctions.getRoomName(map)
                newRoom = DungeonRoom(lair = map, floor = 1, name = roomName)
                # Save after every iteration to avoid duplicate names
                rooms.append(newRoom)
                db.session.add(newRoom)
                db.session.commit()
            map.addRooms(rooms)
            
            # Add player to last room created          
            self.currentRoom = newRoom.id
            db.session.add(self)
            db.session.commit()
            
            # Add edges to rooms.  Ennsure each room has at least two connections, and no more than four
            for room in rooms:
                neighbors = room.getNeighbors()
                if len(neighbors) <= 1:
                    for i in range(randint(1,3)):
                        vertices_added = False
                        count = 0
                        while vertices_added == False:
                            randomRoom = rooms[randint(0,len(rooms)-1)]
                            rNeighbors = randomRoom.getNeighbors()
                            if randomRoom != room and randomRoom not in rNeighbors and len(rNeighbors) < 3:
                                map.addEdge(room, randomRoom)
                                vertices_added = True
                            # Add breakout condition in case no suitable partner is found
                            elif count >= len(rooms):
                                vertices_added = True
                            count = count + 1
                            
            return True
        except:
            # If there are any issues, tear down any objects that may have been created
            self.deleteDungeon()
            db.session.delete(self)
            db.session.commit()
            
            return False
            
    # Deletes a dungeon that is no longer in use
    def deleteDungeon(self):
        playerMap = DungeonMap.query.filter_by(player_id = self.id).first()
        for room in DungeonRoom.query.filter_by(lair=playerMap):
            db.session.delete(room)
        if playerMap:
            db.session.delete(playerMap)            
        db.session.commit()
        return {"quest ended": "You have come to end of your journey today, but your legacy will live on!"}

# The dungeon itself    
class DungeonMap(db.Model):
    __table_args__ = {'extend_existing': True }
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    rooms = db.Column(db.String, default='{}')
    floor = db.Column(db.Integer, default=1)
    
    areas = db.relationship('DungeonRoom', backref='lair', lazy='dynamic')
    events = db.relationship('DungeonEvent', backref='lair', lazy='dynamic')
     
    def __repr__(self):
        return '<Player Map {0} Floor {1}>'.format(self.owner.name, self.floor)
    
    # Adds rooms to a dungeon
    def addRooms(self, rooms):
        for room in rooms:
            if isinstance(room, DungeonRoom):
                rooms_json = json.loads(self.rooms)
                rooms_json[room.name] = room.neighbors
                self.rooms = json.dumps(rooms_json)
                
        db.session.add(self)
        db.session.commit()
        
    # Adds connections between rooms
    def addEdge(self, room_from, room_to):
        if isinstance(room_from, DungeonRoom) and isinstance(room_to, DungeonRoom):
            room_from.addNeighbors([room_to])
            self.addRooms([room_from, room_to])
            return True
        else:
            return False
    
    # Reveals details about the dungeons rooms and all of their connections
    def adjacencyList(self):
        rooms_json = json.loads(self.rooms)
        if len(rooms_json) >= 1:
                return [str(key) + ":" + str(rooms_json[key]) for key in rooms_json.keys()]  
        else:
            return dict()

# The dungeons constituent parts    
class DungeonRoom(db.Model):
    __table_args__ = {'extend_existing': True }
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    dungeon_id = db.Column(db.Integer, db.ForeignKey('dungeon_map.id'))
    floor = db.Column(db.Integer)
    neighbors = db.Column(db.String(256), default='')
    
    events = db.relationship('DungeonEvent', backref='location', lazy='dynamic')
    
    def __repr__(self):
        return '<Room %r>' % (self.name)
    
    # Returns all neighboring rooms            
    def getNeighbors(self):
        #Superficially fixes a bug by removing duplicate connections, don't have time to find real issue with multiple instances of the same neighbors
        neighbor_ids = set(self.neighbors.split(','))
        neighbor_objs = []
        for id in neighbor_ids:
            neighbor_objs.append(DungeonRoom.query.filter_by(id=id).first())
        return neighbor_objs
    
    # Returns details concerning the room as a dictionary
    def getJSON(self):
        return {"id":"{0}".format(self.id), "name":"{0}".format(self.name)}
    
    # Returns details concerning all adjacent rooms as a dictionary    
    def getNeighborsJSON(self):
        neighbors = self.getNeighbors()
        dNeighbors = []
        for neighbor in neighbors:
            dNeighbors.append(neighbor.getJSON())
        return dNeighbors
    
    # Adds a neighboring room as a connection        
    def addNeighbors(self, neighbors):
        for neighbor in neighbors:
            if isinstance(neighbor, DungeonRoom):
                if neighbor.id not in self.neighbors.split(','):
                    if self.neighbors:
                        self.neighbors = self.neighbors + ',{0}'.format(neighbor.id)
                    else:
                        self.neighbors = str(neighbor.id)
                    if neighbor.neighbors:
                        neighbor.neighbors = neighbor.neighbors + ',{0}'.format(self.id)
                    else:
                        neighbor.neighbors = str(self.id)
                    # Save changes between iterations to ensure no duplicates
                    db.session.add(neighbor)
                    db.session.add(self)
                    db.session.commit()                    
            else:
                return False
            return True
        
# Events that can occur in each room of the dungeon
class DungeonEvent(db.Model):
    __table_args__ = {'extend_existing': True }
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('dungeon_room.id'))
    map_id = db.Column(db.Integer, db.ForeignKey('dungeon_map.id'))
    type = db.Column(db.String(256))
    details = db.Column(db.String)
    
    def __repr__(self):
        return '<Event {0} Room {1}>'.format(self.type, self.location.name)