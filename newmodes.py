
from constants import *
class Behaviours():
    def __init__(self):
        self.timer = 0
        self.scatter_mode()
    
    # modes
    def chase_mode(self):
        self.behaviour = CHASE
        self.duration = 20
        self.timer = 0 

    def scatter_mode(self):
        self.behaviour = SCATTER
        self.duration = 12
        self.timer = 0

# updates behaviours
    def update(self,dt):
        # this functions switches between scatter and chase
        self.timer += dt
        if self.timer >= self.duration:
            if self.behaviour == SCATTER:
                self.chase_mode()

            elif self.behaviour == CHASE:
                self.scatter_mode()


class BehaviourManager():
    def __init__(self,ghost):
        self.timer = 0
        self.frightened_duration = 7
        self.behaviour_types = Behaviours()
        self.ghost = ghost 
        self.current_behaviour = self.behaviour_types.behaviour # set to scatter
    

    def get_current_behaviour(self):
        return self.current_behaviour
    
  
    def update(self, dt):
    # Only update Behaviours in SCATTER/CHASE modes
        if self.current_behaviour in [SCATTER, CHASE]:
            self.behaviour_types.update(dt)
            self.current_behaviour = self.behaviour_types.behaviour  # Sync mode

    # Handle FRIGHT mode
        if self.current_behaviour == FRIGHT:
            self.timer += dt
            if self.timer >= self.frightened_duration:

                self.timer = 0
                self.activate_normal_mode()

        if self.current_behaviour == RESPAWN:
            if self.ghost.position == self.ghost.respawn_node.position:
                print("ghost has been respawned")
                self.activate_normal_mode()
                

    def set_fright_mode(self):
        if self.get_current_behaviour() in [SCATTER,CHASE]:
            self.timer = 0
            # self.limiting_time = 7
            self.current_behaviour = FRIGHT

        elif self.get_current_behaviour() == FRIGHT:
            self.timer = 0


    def activate_normal_mode(self):
        self.ghost.restore_normal_behaviour()
        self.behaviour_types.scatter_mode()  # Reset to scatter mode
        self.current_behaviour = SCATTER  # Force scatter mode
        print("Ghost is back to scatter mode")
        
    def activate_respawn_mode(self):
        if self.current_behaviour == FRIGHT:
            self.timer = 0
            self.current_behaviour = RESPAWN