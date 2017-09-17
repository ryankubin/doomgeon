from app import app, models
import random
from numpy.random import choice

# Get a randomly generated room name, which is unique for that dungeon
def getRoomName(map):
    possiblePrefixes = ['Cavern', 'Cell', 'Entrance', 'Hall', 'Reliquary', 'Crypt', 'Mauseleum', 'Sanctum', 'Temple', 'Cave', 'Forest', 'Glade', 'Lair', 'Chamber']    
    possibleSuffixes = ['Despair', 'Cacophany', 'Terror', 'Sanguination', 'Malice', 'Horror', 'Goosebumps', 'that reminds you of that one ex', 'Insanity', 'Existential Terror', 'the Mad', 'Unimaginable Creatures', 'Silence', 'Uncomfortable Silences']
    
    unique = False
    while unique == False:
        possibleName = '{0} of {1}'.format(random.choice(possiblePrefixes), random.choice(possibleSuffixes))
        if not models.DungeonRoom.query.filter_by(lair=map, name=possibleName).first():
            unique = True
    return possibleName

# Get a randomly generated event; will check to see if stairs have been created for that map, and adjust weightings upwards until they have                
def getEventType(room):
    possibleEvents = ['maiden', 'monster', 'stairs', 'treasure']
    eventDetails = {"monster":['Hydra', 'Manticore', 'Demon Bats', 'Furry Trouble'],
                    "maiden":['Surprise Medusa!', 'Vampire seductress', 'Scared Princess'],
                    "stairs":['Stairway Up'],
                    "treasure":['Mimic!', 'Gold Coin', 'Holy Grail', 'Cursed Sword']}
 
    
    map = room.lair
    currentRooms = map.areas.all()
    numRooms = len(currentRooms)
    currentEvents = map.events.all()
    numEvents = len(currentEvents)
    stairEvent = map.events.filter_by(type='stairs').first()
    
    if not stairEvent:
        if numRooms*.2 <= numEvents < numRooms*.4:
            stairWeight = .25
        elif numRooms*.4 <= numEvents < numRooms*.6:
            stairWeight = .50
        elif numRooms*.6 <= numEvents < numRooms*.8:
            stairWeight = .75
        elif numRooms*.8 <= numEvents < numRooms*.6:
            stairWeight = 1          
        else:
            stairWeight = .05
    else:
        stairWeight = 0
        
    unallocatedWeight = 1 - stairWeight
    eventWeights = [ unallocatedWeight*.05, unallocatedWeight*.85, stairWeight, unallocatedWeight*.1]
    
    event = choice(possibleEvents, p = eventWeights)
    return [ event, "You've found a {0}.  Upon further inspection, it looks to be a {1}.".format(event, random.choice(eventDetails[event]))]
    
    
    
    