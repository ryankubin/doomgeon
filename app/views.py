from flask import Flask, jsonify, abort, request, make_response
from app import app, db, mapFunctions
from .models import Player, DungeonRoom, DungeonMap, DungeonEvent

'''
Start quest.  Creates a new quest and begins the adventure
:param str playerName: Name of the player beginning the quest.  Returns an error if not included
Sample request:
    {
        "player": {
            "name": "Sir Foo, of Bar"
        }
    }
'''
@app.route('/quest/start', methods=['POST'])
def start_quest():
    try:
        # Check to see if request has been sent with json parameters.  If not, return 400 error
        if not request.is_json:
            return make_response(jsonify({'error': 'Unable to decode JSON'}), 400)
        data = request.get_json()
        
        # Check to see if player data json is formatted properly
        try:
            playerName = data['player']['name']
            player = Player.query.filter_by(name=playerName).first()
        except:
            return make_response(jsonify({'name': 'required key not provided'}), 422) 
                       
        # Check to see if quest already exists for player.  If so, return 422 error
        if player and player.getDungeon():
            return make_response(jsonify({'error': 'This adventurer has already begun his quest!'}), 422)
        
        # Create a new player if one does not exist
        if not player:
            player = Player(name=playerName)
            db.session.add(player)
            db.session.commit()
        # Create the dungeon; if there are issues, raise a 500 error
        if not player.createDungeon(floor = 1):
            abort(500)
        cRoom = DungeonRoom.query.filter_by(id=player.currentRoom).first()
        
        # Create API response
        message = 'You enter the dimly lit dungeon through the entrance of the {0}'.format(cRoom.name)
        return make_response(jsonify({'message': message, 'player': player.getStatus()}), 201)    
    except:
        abort(500)

'''
End quest.  Terminates the player session and removes all trace of the cartography experiment
:param str playerName: Name of the player ending the quest.  Returns an error if not included
Sample request:
    {
        "player": {
            "name": "Sir Foo, of Bar"
        }
    }
'''
@app.route('/quest/end', methods=['DELETE'])
def end_quest():
    try:
        # Check to see if request has been sent with json parameters.  If not, return 400 error
        if not request.is_json:
            return make_response(jsonify({'error': 'Unable to decode JSON'}), 400)
        data = request.get_json()
        # Attempt to parse request for required parameters.  If not included, return 400 error
        try:
            player = Player.query.filter_by(name=data['player']['name']).first()
            # End the provided players quest
            return make_response(jsonify(player.deleteDungeon()), 204)
        except:
            return make_response(jsonify({'error': 'Provided parameters are incorrect.  Please supply a valid player_name'}), 404)
    except:
        abort(500)

'''
Change Rooms.  Triggers movement of player to any adjacent room
:param int room_id: Id of room to move to.  Returns an error if not included in url string
:param string player_name:  Used to confirm selected room is a viable movement option.  Returns an error if not included as a json parameter
    {
        "player": {
            "name": "Sir Foo, of Bar"
        }
    }
'''
@app.route('/player/move/<room_id>', methods=['GET'])
def move_rooms(room_id):
    # Check to see if room id is an integer
    try:
        room_id = int(room_id)
    except:
        return make_response(jsonify({'error': 'Provided parameters are incorrect.  Please room_id must be an integer'}), 400)
    try:
        # Check if request has been sent with json parameters.  If not, return 400 error
        if not request.is_json:
            return make_response(jsonify({'error': 'Provided parameters are incorrect.  Please provide both room_id and player_name'}), 400)
        data = request.get_json()
        
        # Attempt to parse request for required parameters.  If not included, return 400 error
        try:
            player = Player.query.filter_by(name=data['player']['name']).first()
            if not player:
               return make_response(jsonify({'error': 'Provided parameters are incorrect.  Please provide both room_id and player_name'}), 400)
        except:
            return make_response(jsonify({'error': 'Provided parameters are incorrect.  Please provide both room_id and player_name'}), 400)

        # Check to see if that room is a valid movement option for the given player.  If not, return 422 error and all available paths
        currentRoom = DungeonRoom.query.filter_by(id=player.currentRoom).first()
        potentialRoom = DungeonRoom.query.filter_by(id=room_id).first()
        if potentialRoom in currentRoom.getNeighbors():
            player.currentRoom = potentialRoom.id
            # If the room does not yet have an event, create a new one for it
            if not potentialRoom.events.all():
                eventDetails = mapFunctions.getEventType(potentialRoom)
                newEvent = DungeonEvent(location=potentialRoom, lair = potentialRoom.lair, type = eventDetails[0], details = eventDetails[1])
                db.session.add(newEvent)
            db.session.add(player)
            db.session.commit()
            
            # Create API response        
            return make_response(jsonify({"event":newEvent.details, "message":"You are now in the {0}".format(potentialRoom.name), "player": player.getStatus()}), 200)            
        else:
            return make_response(jsonify({"message": "There is no path in that direction. Choose another path.", "player": player.getStatus()}), 422)
    except:
        abort(500)

'''
Get player status.  This includes current room, adjacent rooms, floor number, and player name
:param str player_name: Id of room to move to.  Returns an error if not included in url string

'''
@app.route('/player/status/<player_name>', methods=['GET'])
def player_status(player_name):
    try:
        # Check to see if player exists
        player = Player.query.filter_by(name=player_name).first()
       
        if player:
            # Check to see if that player has begun their quest
            map = DungeonMap.query.filter_by(player_id=player.id).first()
            if not map:
                return make_response(jsonify({'error': 'Provided player has not yet begun his journey','player_name':player_name}), 404)        
            
            # Create API response
            return jsonify(player.getStatus())            
        else:
            return make_response(jsonify({'error': 'Provided player name not found','player_name':player_name}), 404)
    except:
        abort(500)

'''
Error handling for internal service errors
'''
@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)
    
    
    
    