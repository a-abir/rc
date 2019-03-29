import time

import dill as pickle
import pathfinder as pf

from networktables import NetworkTables
from networktables.util import ntproperty


from pathfinder.followers import EncoderFollower


class RemotePath:
    '''
    This is used to send paths back and forth between
    the roborio and driverstation
    '''


    # MAX_V = 4 # feet/second
    # MAX_A = 1 # feet/second^2
    MAX_V = 2 # feet/second
    MAX_A = 1 # feet/second^2
    # MAX_V = 0.5 # feet/second
    # MAX_A = 0.5 # feet/second^2


    SENT_PATH = ntproperty("/SmartDashboard/SENT_PATH", bytes(0), writeDefault=True)
    RECEIVED_TRAJECTORY = ntproperty("/SmartDashboard/RECEIVED_TRAJECTORY", bytes(0), writeDefault=True)
    FINISHED_GENERATING_TRAJECTORY = ntproperty("/SmartDashboard/FINISHED_GENERATING_TRAJECTORY", 1, writeDefault=True)
        
    def start_compute_server(self):
        '''
        This is run on the desktop to manage
        generating the paths for the bot
        '''
        print("STARTING REMOTE PATH COMPUTE SERVER")
        while True:
            if not self.is_finished_generating():
                print("GENERATING PATH")
                start = time.time()
                _, trajectory = pf.generate(
                    self.get_path_to_generate(), 
                    pf.FIT_HERMITE_CUBIC,
                    pf.SAMPLES_HIGH,
                    dt=0.05,
                    max_velocity=self.MAX_V,
                    max_acceleration=self.MAX_A,
                    max_jerk=60.0
                )
                
                trajectory = pf.modifiers.TankModifier(trajectory)

                self.write_to_trajectory(trajectory)
                print("DONE IN {} SECONDS".format(time.time() - start))

    def generate_remote_path(self, path):
        '''
        This function sends off a path to the desktop
        to be intercepted by the compute path function

        this function returns the generated path when it is done
        '''
        self.write_to_path(path)

        while not self.is_finished_generating():
            pass # wait for path to finish generating
            # time.sleep(2)
            # print("WAITING")
        
        trajectory = self.get_finished_trajectory()

        return trajectory

    def is_finished_generating(self):
        '''
        has the desktop sent the finished signal?
        '''
        return self.FINISHED_GENERATING_TRAJECTORY
        
    def get_path_to_generate(self):
        '''
        unpickle the received path
        '''
        try:
            result = []
            waypoints = pickle.loads(self.SENT_PATH)
            print("RECEIVED PATH TO GENERATE")
            for waypoint in waypoints:
                result.append(pf.Waypoint(*waypoint))
            print("TRAJ:", result)
            return result 
        except Exception as e:
            print("ERROR:", e)
            return None
        
    def get_finished_trajectory(self):
        '''
        unpickle the finished trajectory
        '''
        try:
            result = pickle.loads(self.RECEIVED_TRAJECTORY)
            print("RECEIVED FINISHED TRAJECTORY:", result)
            return result
        except:
            return None
        
    def write_to_path(self, path):
        '''
        write the path to be generated to the dashboard
        '''
        self.SENT_PATH = pickle.dumps(path)
        print("WAITING FOR TRAJECTORY TO FINISH")
        self.FINISHED_GENERATING_TRAJECTORY = 0

    def write_to_trajectory(self, trajectory):
        '''
        write the finished trajectory to the dashboard
        '''
        self.RECEIVED_TRAJECTORY = pickle.dumps(trajectory)
        print("FINISHED GENERATING TRAJECTORY")
        self.FINISHED_GENERATING_TRAJECTORY = 1