"""
Subcontroller module for Froggit

This module contains the subcontroller to manage a single level in the Froggit game.
Instances of Level represent a single game, read from a JSON.  Whenever you load a new
level, you are expected to make a new instance of this class.

The subcontroller Level manages the frog and all of the obstacles. However, those are
all defined in models.py.  The only thing in this class is the level class and all of
the individual lanes.

This module should not contain any more classes than Levels. If you need a new class,
it should either go in the lanes.py module or the models.py module.

Nicholas J. Runje (njr85)
21 December 2020
"""
from game2d import *
from consts import *
from lanes  import *
from models import *

# PRIMARY RULE: Level can only access attributes in models.py or lanes.py using getters
# and setters. Level is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Level(object):
    """
    This class controls a single level of Froggit.

    This subcontroller has a reference to the frog and the individual lanes.  However,
    it does not directly store any information about the contents of a lane (e.g. the
    cars, logs, or other items in each lane). That information is stored inside of the
    individual lane objects.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lesson 27 for an example.  This class will be similar to that
    one in many ways.

    All attributes of this class are to be hidden.  No attribute should be accessed
    without going through a getter/setter first.  However, just because you have an
    attribute does not mean that you have to have a getter for it.  For example, the
    Froggit app probably never needs to access the attribute for the Frog object, so
    there is no need for a getter.

    The one thing you DO need a getter for is the width and height.  The width and height
    of a level is different than the default width and height and the window needs to
    resize to match.  That resizing is done in the Froggit app, and so it needs to access
    these values in the level.  The height value should include one extra grid square
    to suppose the number of lives meter.
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE
    # Attribute _startingfrogx: The x-coordinate starting position for
    #                           self._frog
    # Invariant: _startingfrogx is a float
    #
    # Attribute _startingfrogy: The y-coordinate starting position for
    #                           self._frog
    # Invariant: _startingfrogy is a float

    # Attribute _cooldownperiod: Indicates time left before Frog can move again
    # Invariant: _cooldownperiod is a float

    # Attribute _iscollidingwithexit: Indicates if Frog collides with lilipad
    # Invariant: _iscollidingwithexit is a boolean

    # Attribute _iscollidingwithhedgelane: If Frog collides Hedge lane
    # Invariant: _iscollidingwithhedgelane is a boolean

    # Attribute _justaddedFROGSAFEobject: Whether safe Frog just added
    # Invariant: _justaddedFROGSAFEobject is a boolean

    # Attribute _wongame: Indicates whether game is won
    # Invariant: _wongame is a boolean

    # Attribute _iscollidingwithwaterlane: If Frog collides Water lane
    # Invariant: _iscollidingwithwaterlane is a boolean

    # Attribute _iscollidingwithlog: If Frog collides with log obstacle
    # Invariant: _iscollidingwithlog is a boolean

    # Attribute _frog: Frog object to draw
    # Invariant: _frog is a valid Frog class object containing GImage

    # Attribute _lanes: Contains list of different types of lane classes
    # Invariant: _lanes is a list or None

    # Attribute _livescounter: Contains list of GImage lives objects
    # Invariant: _livescounter is a list

    # Attribute _livesleft: Indicates how many lives left for player
    # Invariant: _livesleft is an integer

    # Attribute _livestext: Contains title indicating lives
    # Invariant: _livestext is a valid GLabel object

    # Attribute _height: Indicates pixel height of the level
    # Invariant: _height is an integer

    # Attribute _width: Indicates pixel width of the level
    # Invariant: _width is an integer

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getFrogVisible(self):
        """
        Returns whether or not the frog is visible
        """
        return self._frog.visible

    def setFrogVisible(self,value):
        """
        Sets whether the frog is visible through the self._frog.visible attribute

        Parameter value: Sets whether frog is visible
        Precondition: value an boolean
        """
        self._frog.visible = value

    def setFrogOriginalLocation(self):
        """
        Sets the frog to the original location described in JSON file
        """
        self._frog.x = self._startingfrogx
        self._frog.y = self._startingfrogy
        # print('Setting original location')

    def getFrogLives(self):
        """
        Returns how many frog lives left
        """
        return self._livesleft

    def setFrogLives(self,value):
        """
        Sets how many frogs lives are left

        Parameter value: Sets how many lives left in game
        Precondition: value an integer
        """
        self._livesleft = value

    def setFrogIscollidingWithExit(self,value):
        """
        Sets the self._iscollidingwithexit attribute

        Parameter value: Sets whether frog is collding with an exit
        Precondition: value an boolean
        """
        self._iscollidingwithexit = value

    def getFrogIsCollidingWithExit(self):
        """
        Returns whether frog is colliding with exit
        """
        return self._iscollidingwithexit

    def getWonGame(self):
        """
        Returns whether the user won the game
        """
        return self._wongame

    # INITIALIZER (standard form) TO CREATE THE FROG AND LANES

    def __init__(self,json_dict,level_width,level_height):
        """
        Initializes the lane position, background, and objects

        Parameter json_dict: Contains JSON file for level
        Preconditon: json_dict is a valid JSON file

        Parameter level_width: Indicates width of level
        Precondition: level_width is an integer

        Parameter level_height: Indicates height of the level
        Precondition: level_height is an integer
        """
        # CREATE THE FROG
        x_pos = (json_dict['start'][0]) * GRID_SIZE + (GRID_SIZE)/2
        y_pos = (json_dict['start'][1]) * GRID_SIZE + (GRID_SIZE)/2
        self._startingfrogx = x_pos
        self._startingfrogy = y_pos

        self._frog = Frog(x_pos,y_pos)
        self._frog.visible = True

        # CREATE THE LANES
        self._lanes = []
        self._classifylanes(json_dict)

        self._livescounter = self._livesCounterList(level_width,level_height)
        self._livesleft = 3
        self._livestext = GLabel(text="LIVES:",font_name=ALLOY_FONT,\
        linecolor='#349441',font_size=ALLOY_SMALL)
        self._livestext.x = self._livescounter[0].x - 120
        self._livestext.top = level_height - 6

        self._height = level_height
        self._width = level_width

        self._cooldownperiod = FROG_SPEED
        self._iscollidingwithexit = False
        self._iscollidingwithhedgelane = False
        self._justaddedFROGSAFEobject = False
        self._wongame = False
        self._iscollidingwithwaterlane = False
        self._iscollidingwithlog = False
    # UPDATE METHOD TO MOVE THE FROG AND UPDATE ALL OF THE LANES
    def update(self,dt,input):
        """
        Updates the frog movement and lanes

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Attribute input: The user input, used to control the frog and change state
        Invariant: input is an instance of GInput and is inherited from GameApp
        """
        self._methodBeginningReset()

        self._cooldownperiod = self._cooldownperiod - dt

        currentX = self._frog.x
        currentY = self._frog.y

        # print((currentX,currentY))

        ############### Handles lane changes ###################
        for lane in self._lanes:
            # Update the obstacles
            obstacles_list = lane.getObjs()
            buffer_size = lane.getBuffer()
            try:
                speed = lane.getSpeed()
                lane.update(dt,obstacles_list,speed,self._width,buffer_size,\
                self._frog)
            except:
                pass

            # Check for cars
            self._methodCheckForCars(lane)

            # Check for Hedge exits
            self._methodCheckForHedge(lane,currentX,currentY)

            # Check for Water lane
            self._methodCheckWaterLane(lane,currentX,currentY,dt)
        ########################################################

        # Moves the Frog
        self._methodMoveFrogAndReset(currentX,currentY,input)

    # DRAW METHOD TO DRAW THE FROG AND THE INDIVIDUAL LANES
    def draw(self,view):
        """
        Draws the lanes.

        Paramter view: Indicates which window to draw
        Precondition: view is a valid view object
        """
        # Needs to draw the lanes when called in Froggit class
        for lane in self._lanes:
            lane.draw(view)
        if self._frog.visible == True:
             self._frog.draw(view)
        for num in range(self.getFrogLives()):
            for life in self._livescounter[:num+1]:
                life.draw(view)
        self._livestext.draw(view)


    # ANY NECESSARY HELPERS (SHOULD BE HIDDEN)
    def _methodMoveFrogAndReset(self,currentX,currentY,input):
        """
        Updates position of Frog and checks if colliding with Hedge

        Parameter currentX: Indicates current x-position of Frog
        Precondition: currentX is a float

        Parameter currentY: Indicates current y-position of Frog
        Precondition: currentY is a float

        Parameter input: Allows the Frog to move
        Precondition: input is valid instance of input from GameApp
        """
        if (self._cooldownperiod <= 0) and (self._iscollidingwithexit == False):
            self._moveFrogWASD(input,currentX,currentY)
            self._moveFrogArrowKeys(input,currentX,currentY)
            self._cooldownperiod = FROG_SPEED

        if (self._iscollidingwithhedgelane == True) and \
        (self._iscollidingwithexit == False):
            self._frog.y = currentY - GRID_SIZE
            self._iscollidingwithhedgelane = False

        if (self._iscollidingwithwaterlane == True) and \
        (self._iscollidingwithlog == False):
            self.setFrogVisible(False)
            self.setFrogLives(self.getFrogLives() - 1)

    def _methodBeginningReset(self):
        """
        Resets the collision properties from previous frames
        """
        self._iscollidingwithlog = False
        self._iscollidingwithwaterlane = False
        if (self._justaddedFROGSAFEobject == True):
            self._methodFROGSAFEreset()

    def _methodCheckWaterLane(self,lane,currentX,currentY,dt):
        """
        Checks for properties of the Water class

        Parameter lane: Indicates which lane
        Precondition: lane is a valid type of lane object from lanes.py

        Parameter currentX: Indicates current x-position of Frog
        Precondition: currentX is a float

        Parameter currentY: Indicates current y-position of Frog
        Precondition: currentY is a float
        """
        if isinstance(lane,Water):
            if self._frog.collides(lane.getTile()):
                self._iscollidingwithwaterlane = True
                for log in lane.getListofLogs():
                    if log.contains((currentX,currentY)):
                        self._iscollidingwithlog = True
                        if self._iscollidingwithlog == True:
                            log_speed = lane.getSpeed()
                            log_movement = log_speed * dt

                            if (log_movement > 0):
                                self._frog.x += log_movement
                            if (log_movement < 0):
                                self._frog.x += log_movement

    def _classifylanes(self,json_dict):
        """
        Loops through dictionary to return lanes

        Parameter json_dict: the dictionary to loop through
        Precondition: json_dict is a valid JSON file
        """
        bottom_num = 0

        for num_lane in range(len(json_dict['lanes'])):
            if json_dict['lanes'][num_lane]['type'] == 'grass':
                lane_object = Grass(json_dict,num_lane,bottom_num)
                self._lanes.append(lane_object)
            elif json_dict['lanes'][num_lane]['type'] == 'road':
                lane_object = Road(json_dict,num_lane,bottom_num)
                self._lanes.append(lane_object)
            elif json_dict['lanes'][num_lane]['type'] == 'water':
                lane_object = Water(json_dict,num_lane,bottom_num)
                self._lanes.append(lane_object)
            elif json_dict['lanes'][num_lane]['type'] == 'hedge':
                lane_object = Hedge(json_dict,num_lane,bottom_num)
                self._lanes.append(lane_object)
            bottom_num += 64

    def _methodCheckForHedge(self,lane,currentX,currentY):
        """
        Checks for collision with Hedge lane

        Parameter lane: Indicates which lane
        Precondition: lane is a valid type of lane object from lanes.py

        Parameter currentX: Indicates current x-position of Frog
        Precondition: currentX is a float

        Parameter currentY: Indicates current y-position of Frog
        Precondition: currentY is a float
        """
        if isinstance(lane,Hedge):
            if lane.getTile().collides(self._frog):
                self._iscollidingwithhedgelane = True

            for hedge_instance in lane.getObjs():
                if (hedge_instance.contains((currentX,currentY))):
                    if hedge_instance.source == 'exit.png':
                        lane.addtolistofFROGSafe((currentX,currentY))
                        self._iscollidingwithexit = True
                        self._justaddedFROGSAFEobject = True
                        self.setFrogVisible(False)

                if hedge_instance.source == 'open.png':
                    if (hedge_instance.contains((currentX,currentY))):
                        self._iscollidingwithexit = False
                        self._iscollidingwithhedgelane = False

                if (lane.getLengthofFROGSAFEobjects() \
                == lane.getLengthofLilipads()):
                    self._wongame = True

            for frogsafe_instance in lane.getListofFROGSAFEobjects():
                if frogsafe_instance.collides(self._frog):
                    self._iscollidingwithhedgelane = True
                    self._iscollidingwithexit = False

    def _methodCheckForCars(self,lane):
        """
        Checks for collision with frog and cars

        Parameter lane: Indicates which lane
        Precondition: lane is a valid type of lane object from lanes.py
        """
        if isinstance(lane,Road):
            cars_list = lane.getObjs()
            for car in cars_list:
                if self._frog.collides(car):
                    self.setFrogVisible(False)
                    self.setFrogLives(self.getFrogLives() - 1)
                    # print('Withdrawing one')
                    # print(car)

    def _methodFROGSAFEreset(self):
        """
        Resets attributes to original values after Frog reaches safety
        """
        self._justaddedFROGSAFEobject = False
        self._iscollidingwithhedgelane = False
        self._iscollidingwithexit = False
        self._cooldownperiod = FROG_SPEED
        self._iscollidingwithwaterlanebutnotlog = False

    def _livesCounterList(self,level_width,level_height):
        """
        Returns a list of GImage froghead live indicators

        Parameter level_width: Indicates level width
        Precondition: level_width is a float

        Parameter level_height: Indicates level height
        Precondition: level_height is a float
        """
        return [GImage(x=level_width-(GRID_SIZE/2)-(GRID_SIZE*2),\
        y=level_height-(GRID_SIZE/2), width = GRID_SIZE, height = GRID_SIZE, \
        source='froghead.png'),GImage(x=level_width-(GRID_SIZE/2)-GRID_SIZE,\
        y=level_height-(GRID_SIZE/2), width = GRID_SIZE, height = GRID_SIZE, \
        source='froghead.png'),GImage(x=level_width-(GRID_SIZE/2),\
        y=level_height-(GRID_SIZE/2), width = GRID_SIZE, height = GRID_SIZE, \
        source='froghead.png')]

    def _moveFrogWASD(self,input,currentX,currentY):
        """
        Moves the frog with the WASD keys

        Parameter input: Allows the Frog to move
        Precondition: input is valid instance of input from GameApp

        Parameter currentX: Indicates current x-position of Frog
        Precondition: currentX is a float

        Parameter currentY: Indicates current y-position of Frog
        Precondition: currentY is a float
        """
        if input.is_key_down('w') and input.is_key_down('s'):
            pass
        elif input.is_key_down('a') and input.is_key_down('d'):
            pass
        elif input.is_key_down('w') and input.is_key_down('a'):
            pass
        elif input.is_key_down('w') and input.is_key_down('d'):
            pass
        elif input.is_key_down('a') and input.is_key_down('s'):
            pass
        elif input.is_key_down('s') and input.is_key_down('d'):
            pass
        else:
            if input.is_key_down('w') and (currentY + GRID_SIZE <= \
            self._height-GRID_SIZE):
                self._frog.y = currentY + GRID_SIZE
                self._frog.angle = FROG_NORTH
            if input.is_key_down('s') and (currentY - GRID_SIZE >= 0):
                self._frog.y = currentY - GRID_SIZE
                self._frog.angle = FROG_SOUTH
            if input.is_key_down('a') and (currentX - GRID_SIZE >= 0):
                self._frog.x = currentX - GRID_SIZE
                self._frog.angle = FROG_WEST
            if input.is_key_down('d') and (currentX + GRID_SIZE <= self._width):
                self._frog.x = currentX + GRID_SIZE
                self._frog.angle = FROG_EAST

    def _moveFrogArrowKeys(self,input,currentX,currentY):
        """
        Moves the frog with the WASD keys

        Parameter input: Allows the Frog to move
        Precondition: input is valid instance of input from GameApp

        Parameter currentX: Indicates current x-position of Frog
        Precondition: currentX is a float

        Parameter currentY: Indicates current y-position of Frog
        Precondition: currentY is a float
        """
        if input.is_key_down('up') and input.is_key_down('down'):
            pass
        elif input.is_key_down('left') and input.is_key_down('right'):
            pass
        elif input.is_key_down('up') and input.is_key_down('left'):
            pass
        elif input.is_key_down('up') and input.is_key_down('right'):
            pass
        elif input.is_key_down('left') and input.is_key_down('down'):
            pass
        elif input.is_key_down('down') and input.is_key_down('right'):
            pass
        else:
            if input.is_key_down('up') and (currentY + GRID_SIZE <= \
            self._height-GRID_SIZE):
                self._frog.y = currentY + GRID_SIZE
                self._frog.angle = FROG_NORTH
            if input.is_key_down('down') and (currentY - GRID_SIZE >= 0):
                self._frog.y = currentY - GRID_SIZE
                self._frog.angle = FROG_SOUTH
            if input.is_key_down('left') and (currentX - GRID_SIZE >= 0):
                self._frog.x = currentX - GRID_SIZE
                self._frog.angle = FROG_WEST
            if input.is_key_down('right') and (currentX + GRID_SIZE \
            <= self._width):
                self._frog.x = currentX + GRID_SIZE
                self._frog.angle = FROG_EAST
