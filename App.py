from manipulation import Data_for_aircraft as dfa
from map import elemanEkle, showMap, setStartingCoordinates, saveMap
import time

Aircraft_Tuples, m1, m2 = dfa.returnAircrafData()
setStartingCoordinates(53, 49)


showMap()

while(True):

    Aircraft_Tuples, m1, m2 = dfa.returnAircrafData()
    

    for key in Aircraft_Tuples:
        (NormalAircraft,ManipulatedAircraft) = Aircraft_Tuples[key]
        print(f"{NormalAircraft.latitude} {ManipulatedAircraft.latitude}")
        elemanEkle(NormalAircraft.latitude, NormalAircraft.longitude, key, NormalAircraft.velocity, NormalAircraft.geo_altitude, 180,False)
        elemanEkle(ManipulatedAircraft.latitude, ManipulatedAircraft.longitude, key+"_M", ManipulatedAircraft.velocity, ManipulatedAircraft.geo_altitude, 180,True)
    saveMap()
    time.sleep(11)
