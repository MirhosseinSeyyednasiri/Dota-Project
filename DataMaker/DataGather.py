from utils import DataBaseHandler , DataReciver , MatchIDFinderByHeroName , JsonWriter


def DataGather():

    
    dataBase = DataBaseHandler()
    #dataBase.CreateTable()

    MatchIDFinder = MatchIDFinderByHeroName()
    MatchIDFinder.GrabMatchID()

    dataBase.SaveMatchID(MatchIDFinder.matchIDSet)



    
#    matchIDs = dataBase.ReadMatchIDTable()
#    matchDataReciver = DataReciver()
#    jsonWirter = JsonWriter()
#    for  matchID in matchIDs :

#        matchIDDate = matchDataReciver.GetMatchDetail(matchID[0])
#        jsonWirter.Write(matchIDDate , str(matchID[0]) + ".json")






if __name__ == "__main__" :
    DataGather()