"""
Lanes module for Froggit

This module contains the lane classes for the Frogger game. The lanes are the vertical
slice that the frog goes through: grass, roads, water, and the exit hedge.

Each lane is like its own level. It has hazards (e.g. cars) that the frog has to make
it past.  Therefore, it is a lot easier to program frogger by breaking each level into
a bunch of lane objects (and this is exactly how the level files are organized).

You should think of each lane as a secondary subcontroller.  The level is a subcontroller
to app, but then that subcontroller is broken up into several other subcontrollers, one
for each lane.  That means that lanes need to have a traditional subcontroller set-up.
They need their own initializer, update, and draw methods.

There are potentially a lot of classes here -- one for each type of lane.  But this is
another place where using subclasses is going to help us A LOT.  Most of your code will
go into the Lane class.  All of the other classes will inherit from this class, and
you will only need to add a few additional methods.

If you are working on extra credit, you might want to add additional lanes (a beach lane?
a snow lane?). Any of those classes should go in this file.  However, if you need additional
obstacles for an existing lane, those go in models.py instead.  If you are going to write
extra classes and are now sure where they would go, ask on Piazza and we will answer.

Nicholas J. Runje (njr85)
21 December 2020
"""
from game2d import *
from consts import *
from models import *

# PRIMARY RULE: Lanes are not allowed to access anything in any level.py or app.py.
# They can only access models.py and const.py. If you need extra information from the
# level object (or the app), then it should be a parameter in your method.

class Lane(object):         # You are permitted to change the parent class if you wish
    """
    Parent class for an arbitrary lane.

    Lanes include grass, road, water, and the exit hedge.  We could write a class for
    each one of these four (and we will have classes for THREE of them).  But when you
    write the classes, you will discover a lot of repeated code.  That is the point of
    a subclass.  So this class will contain all of the code that lanes have in common,
    while the other classes will contain specialized code.

    Lanes should use the GTile class and to draw their background.  Each lane should be
    GRID_SIZE high and the length of the window wide.  You COULD make this class a
    subclass of GTile if you want.  This will make collisions easier.  However, it can
    make drawing really confusing because the Lane not only includes the tile but also
    all of the objects in the lane (cars, logs, etc.)
    """
    pass
    # LIST ALL HIDDEN ATTRIBUTES HERE
    # Attribute _tile: GTile corresponding with respective JSON lane type
    # Invariant: _tile is a valid GTile object

    # Attribute _objs: Contains a list of obstacles specified in JSON file
    # Invariant: _objs is a valid list containing GImage objects

    # Attribute _speed: Indicates speed of lane obstacles per JSON file
    # Invariant: _speed is a flaot

    # Attribute _bufffer: Contains the specified buffer zone in JSON file
    # Invariant: _buffer is a float

    # Attribute _iscolliding: Indicates whether frog is collding with obstacle
    # Invariant: _iscolliding is a boolean

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getTile(self):
        """
        Returns tile
        """
        return self._tile

    def getObjs(self):
        """
        Returns self._objs
        """
        return self._objs

    def setObjs(self,value):
        """
        Sets the obstacles for the lane.
        """
        self._objs = value

    def getSpeed(self):
        """
        Returns the speed of the objects
        """
        return self._speed

    def getBuffer(self):
        """
        Returns the size of the buffer
        """
        return self._buffer

    def getIsColldingWithCar(self):
        """
        Returns whether frog is collding with car
        """
        return self._iscolliding

    # INITIALIZER TO SET LANE POSITION, BACKGROUND,AND OBJECTS
    def __init__(self,json_dict, num_lane, bottom_num):
        """
        Initializes all the lane objects

        Parameter json_dict: JSON dictionary for level
        Preconditon: json_dict is a valid JSON file

        Parameter num_lane: Indicates which lane is being targeted
        Precondition: num_lane is an integer

        Parameter bottom_num: Indicates the horizontal bottom of lane
        Precondition: bottom_num is an integer
        """
        this_game_width = json_dict['size'][0] * GRID_SIZE

        self._tile = GTile(x = (this_game_width)/2, bottom = bottom_num, \
        height = 64, width = this_game_width,\
        source = str(json_dict['lanes'][num_lane]['type'])+'.png')

        self._objs = []

        try:
            for object_num in range(len(json_dict['lanes'][num_lane]\
            ['objects'])):
                x_grid = json_dict['lanes'][num_lane]['objects']\
                [object_num]['position']
                x_pos = x_grid * GRID_SIZE + (GRID_SIZE)/2
                y_grid = num_lane
                y_pos = y_grid * GRID_SIZE + (GRID_SIZE)/2

                type_of_image = json_dict['lanes'][num_lane]['objects']\
                [object_num]['type']
                type_of_image = type_of_image+'.png'
                gimage_object = GImage(x=x_pos,y=y_pos,source=type_of_image)
                self._objs.append(gimage_object)

                if json_dict['lanes'][num_lane]['type'] not in ['grass','hedge']:
                    if json_dict['lanes'][num_lane]['speed'] < 0:
                        check = 180
                        gimage_object.angle = check
                    else:
                        pass
        except:
            self._objs.append(None)

        try:
            self._speed = json_dict['lanes'][num_lane]['speed']
        except:
            pass

        self._buffer = json_dict['offscreen']

        self._iscolliding = False

    # ADDITIONAL METHODS (DRAWING, COLLISIONS, MOVEMENT, ETC)
    def update(self,dt,obstacles_list,speed,level_width,buffer_size,frog=None):
        """
        Updates the movement of the objects

        Parameter dt: Indicates how much time per frame
        Precondition: dt is a float

        Parameter obstacles_list: Contains list of obstacle for given lane
        Precondition: obstacles_list is a list of valid GImage objects

        Parameter speed: Indicates specified lane speed in JSON level file
        Preconditon: speed is a float

        Parameter level_width: Indicates pixel width of the level
        Precondition: level_width is a float

        Parameter buffer_size: Indicates size of buffer specified in JSON file
        Precondition: buffer_size is a float

        Parameter frog: The game frog
        Precondition: frog is a valid Frog class containing GImage object
        """
        obstacle_movement = speed * dt

        #Calculate movment per pixel
        for obstacle in obstacles_list:
            obstacle.x = obstacle.x + obstacle_movement
            if (speed > 0) and (obstacle.x > level_width + \
            (buffer_size*GRID_SIZE)):
                obstacle.x = 0 - (buffer_size*GRID_SIZE)
            elif (speed < 0) and (obstacle.x < 0 - (buffer_size*GRID_SIZE)):
                obstacle.x = level_width + (buffer_size*GRID_SIZE)

            if obstacle.collides(frog):
                if obstacle.source in ['car1.png','car2.png','car3.png',\
                'car4.png','car5.png','car6.png']:
                    self._iscolliding = True
                else:
                    self._iscolliding = False
            else:
                self._iscolliding = False

    def draw(self,view):
        """
        Draws the lanes

        Paramter view: Indicates which window to draw
        Precondition: view is a valid view object
        """
        self._tile.draw(view)

        i = 0
        for object in self._objs:
            if self._objs[i] != None:
                object.draw(view)
            i += 1

    def _FrogIsColldingWithCar(self,value):
        """
        Returns whether the frog is currently collding with a car object

        Parameter value: Sets whether frog is colliding with a car object
        Precondition: value is a boolean
        """
        if value == True:
            return True
        else:
            return False


class Grass(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a 'safe' grass area.

    You will NOT need to actually do anything in this class.  You will only do anything
    with this class if you are adding additional features like a snake in the grass
    (which the original Frogger does on higher difficulties).
    """
    pass

    # ONLY ADD CODE IF YOU ARE WORKING ON EXTRA CREDIT EXTENSIONS.


class Road(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a roadway with cars.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, roads are different
    than other lanes as they have cars that can kill the frog. Therefore, this class
    does need a method to tell whether or not the frog is safe.
    """
    pass

    # DEFINE ANY NEW METHODS HERE


class Water(Lane):
    """
    A class representing a waterway with logs.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, water is very different
    because it is quite hazardous. The frog will die in water unless the (x,y) position
    of the frog (its center) is contained inside of a log. Therefore, this class needs a
    method to tell whether or not the frog is safe.

    In addition, the logs move the frog. If the frog is currently in this lane, then the
    frog moves at the same rate as all of the logs.
    """
    # DEFINE ANY NEW METHODS HERE
    def getListofLogs(self):
        """
        Returns a list of Log obstacles
        """
        return self._objs

class Hedge(Lane):
    """
    A class representing the exit hedge.

    This class is a subclass of lane because it does want to use a lot of the features
    of that class. But there is a lot more going on with this class, and so it needs
    several more methods.  First of all, hedges are the win condition. They contain exit
    objects (which the frog is trying to reach). When a frog reaches the exit, it needs
    to be replaced by the blue frog image and that exit is now "taken", never to be used
    again.

    That means this class needs methods to determine whether or not an exit is taken.
    It also need to take the (x,y) position of the frog and use that to determine which
    exit (if any) the frog has reached. Finally, it needs a method to determine if there
    are any available exits at all; once they are taken the game is over.

    These exit methods will require several additional attributes. That means this class
    (unlike Road and Water) will need an initializer. Remember to user super() to combine
    it with the initializer for the Lane.
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE
    # Attribute _listOfLilipads: List of of lilipads objects
    # Invariant: _listOfLilipads is a list containing GImage objects

    # Attribute _numberoflilipads: Indicates length of lilipads list
    # Invariant: _numberoflilipads is a float

    # Attribute _listofFROGSAFEobjectsLOCATIONS: tuple list of safe locations
    # Invariant: _listofFROGSAFEobjectsLOCATIONS is a valid list

    # Attribute _listofFROGSAFEobjects: list of GImage FROG_SAFE objects
    # Invariant: _listofFROGSAFEobjects is a valid list

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM
    def getListofLilipads(self):
        """
        Returns self._listOfLilipads
        """
        return self._listOfLilipads

    def getLengthofLilipads(self):
        """
        Returns the length of self._listOfLilipads
        """
        return len(self._listOfLilipads)

    def getLengthofFROGSAFEobjects(self):
        """
        Returns length of self._listofFROGSAFEobjects
        """
        return len(self._listofFROGSAFEobjects)

    def getListofFROGSAFEobjects(self):
        """
        Returns a list of FROG_SAFE objects
        """
        return self._listofFROGSAFEobjects


    # INITIALIZER TO SET ADDITIONAL EXIT INFORMATION
    def __init__(self,json_dict, num_lane, bottom_num):
        """
        Initializes the Hedge lane

        This file inherits the Lane class and creates attributes which are specific
        to Hedge class.

        Parameter json_dict: Contains the JSON level file
        Preconditon: json_dict is a valid JSON

        Paramter num_lane: Indicates which number lane in JSON being worked on
        Preconditon: num_lane is a float

        Parameter bottom_num: Indicates bottom position of GTile object
        Precondition: bottom_num is an integer
        """
        super().__init__(json_dict, num_lane, bottom_num)

        self._listOfLilipads = self._listOfLilipads(self._objs)
        self._numberoflilipads = len(self._listOfLilipads)
        self._listofFROGSAFEobjectsLOCATIONS = []
        self._listofFROGSAFEobjects = []

    # ANY ADDITIONAL METHODS
    def draw(self,view):
        """
        Draws the view for hedge

        Paramter view: Indicates which window to draw
        Precondition: view is a valid view object
        """
        super().draw(view)

        for safefrog_instance in self._listofFROGSAFEobjects:
            safefrog_instance.draw(view)

    def addtolistofFROGSafe(self,tuple):
        """
        Makes a list of FROG_SAFE GImage objects

        Paramter tuple: Tuple of current Frog location
        Precondition: tuple is a valid tuple containg Frog's x and y-positions
        """
        self._listofFROGSAFEobjectsLOCATIONS.append(tuple)
        frogsafe_object = GImage(x=(tuple[0]), y=(tuple[1]),source='safe.png')
        frogsafe_object.angle = FROG_SOUTH
        self._listofFROGSAFEobjects.append(frogsafe_object)

    def _listOfLilipads(self,list):
        """
        Returns a list of the lilipad locations (excluding the 'open.png')

        Paramter list: A list of lilipad locations
        Precondition: list is a valid list containing GImage objects
        """
        pass

        # print(list)
        list_of_lilipads = []
        for hedge_instance in list:
            if hedge_instance.source != 'open.png':
                # print(hedge_instance.x)
                tuple = (hedge_instance.x,hedge_instance.y)
                # print(tuple)
                list_of_lilipads.append(tuple)

        return list_of_lilipads

# IF YOU NEED ADDITIONAL LANE CLASSES, THEY GO HERE
