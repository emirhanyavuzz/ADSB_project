from opensky_api import OpenSkyApi
from datetime import datetime, timedelta
import os

api = OpenSkyApi("taric49","openskyapipasswordtaric66")
# bbox = (min latitude, max latitude, min longitude, max longitude)

#Data of the aircraft that we need
class Data_for_aircraft:
    def __init__(self, icao24 = "", time_position = 0, longitude = 0, latitude = 0, velocity = 0, geo_altitude = 0, angle = 0):
        error_tp = False
        error_longitude = False
        error_latitude = False
        error_velocity = False
        error_geo_altitude = False

        self.icao24 = str(icao24)
        
        if(time_position != None and time_position < 0):
            error_tp = True
            print("time_position error")
        if(longitude != None and longitude<-180 and 180<longitude):
            error_longitude = True
            print("longitude error")
        if(latitude != None and latitude<-90 and 90<latitude):
            error_latitude = True
            print("latitude error")
        if(velocity != None and velocity<0):
            error_velocity = True
            print("velocity error")
        if(geo_altitude != None and geo_altitude<0 and 30.000<geo_altitude):
            error_geo_altitude = True
            print("geo_altitude error")
        if(error_tp or error_longitude or error_latitude or error_velocity or error_geo_altitude):
            raise ValueError()
        
        
        self.time_position = time_position
        self.longitude = longitude
        self.latitude = latitude
        self.velocity = velocity
        self.geo_altitude = geo_altitude
        self.angle = angle
    
    #Manipulation values can be changed
    @staticmethod
    def  Manipulate_Data(icao24 = "", time_position = 0, longitude = 0, latitude = 0, velocity = 0, geo_altitude = 0, angle = 0):
        n_latitude = 0
        n_longitude = 0
        n_velocity = 0
        n_geo_altitude = 0
    
        if(longitude != None):
          modifier_long = 0.97 if longitude>=0 else 1.03
          n_longitude = longitude*modifier_long
        if(latitude != None):
          modifier_lat = 0.97 if latitude>=0 else 1.03
          n_latitude =  latitude*modifier_lat
        if(velocity != None and velocity != 0):
          n_velocity =  velocity*0.97
        if(geo_altitude != None and geo_altitude != 0):
          n_geo_altitude = geo_altitude*0.97
    
          return Data_for_aircraft(icao24, time_position, n_longitude, n_latitude, n_velocity, n_geo_altitude, angle)
    @staticmethod
    def returnAircrafData():
        Aircraft_Tuples = {}
    
        min_latitude = -90
        max_latitude = 90
        min_longitude = -180
        max_longitude = 180
    
        icao24_of_theAircarft = ""
    
    
        # Assume the .txt file same folder with manipulation.py
        #Helper method for Import_UI_variables method
        def Access_File():
            current_folder = os.getcwd()
            file_name = "input.txt"
            current_path_of_file = os.path.join(current_folder, file_name)
            return current_path_of_file
    
    
    
        # read the .txt file line by line and using for class variable decleration
        # declare all the variables from .txt file to global python variables  after calling
        def Import_UI_variables():
                # variable names for global declaration
                variable_names = ["min_latitude", "max_latitude", "min_longitude", "max_longitude", "icao24_of_theAircarft"]
                latitude_values=[]
                longitude_values=[] 
                
                with open(Access_File(), "r") as dosya:
                    icao24_value = ""
                    for i, line in enumerate(dosya):
                        if i<2:
                            deger = float(line.strip())
                            latitude_values.append(deger)
                        elif i<4:
                        # variable names
                            deger = float(line.strip())
                            longitude_values.append(deger)
                        else:
                            deger = line.strip()
                            icao24_value = deger
                
                min_latitude = min(latitude_values)
                max_latitude = max(latitude_values)
                min_longitude = min(longitude_values)
                max_longitude = max(longitude_values)
                return min_latitude, max_latitude, min_longitude, max_longitude, icao24_value
        
    
        (min_latitude, max_latitude , min_longitude , max_longitude, icao24_of_theAircarft) =  Import_UI_variables()
        # I cannot specify time  why?
        state_vectors = api.get_states(0, None, bbox=(min_latitude, max_latitude, min_longitude, max_longitude))
        if(state_vectors != None):
            print(f'TIME: {state_vectors.time}')
            for s in state_vectors.states:
                print(f'ICAO24: {s.icao24} Time_Position: {s.time_position}  Longitude: {s.longitude} Latitude: {s.latitude} Velocity: {s.velocity} Geo_altitude: {s.geo_altitude}')
                
                aircraft = Data_for_aircraft(s.icao24, s.time_position, s.longitude, s.latitude, s.velocity, s.geo_altitude, s.true_track)
                
                manipulated_aircraft = Data_for_aircraft.Manipulate_Data(s.icao24, s.time_position, s.longitude, s.latitude, s.velocity, s.geo_altitude, s.true_track)
                
                if(manipulated_aircraft != None):
                    Aircraft_Tuples[s.icao24] = (aircraft, manipulated_aircraft)
                else:
                    print("Can not manipulate")
        else:
            print("There is no data")
        middle_lat = max_latitude-min_latitude
        middle_long = max_longitude-min_longitude
        return Aircraft_Tuples ,middle_lat, middle_long
    
#  #printing pairs of original and manipulated data
# print("MAIN IN MANIPULATION.PY------------------------------------------------------------------------------------------------------------------")
# Aircraft_Tuples, m1, m2 = Data_for_aircraft.returnAircrafData()
# for key in Aircraft_Tuples:
#     (a,b) = Aircraft_Tuples[key]
    
#     print(f'ICAO24: {a.icao24} Time_Position: {a.time_position}  Longitude: {a.longitude} Latitude: {a.latitude} Velocity: {a.velocity} Geo_altitude: {a.geo_altitude} Angle: {a.angle}')
#     print(f'ICAO24: {b.icao24} Time_Position: {b.time_position}  Longitude: {b.longitude} Latitude: {b.latitude} Velocity: {b.velocity} Geo_altitude: {b.geo_altitude} Angle: {b.angle}')        
#     print()
# #Check if all aircraft data manipulated
# #print(f'Total Aircraft Number :{len(state_vectors.states)} \n Manipulated Aircrafts Number: {len(Aircraft_Tuples)}')
