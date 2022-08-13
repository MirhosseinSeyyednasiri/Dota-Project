from utils import DataBaseHandler , DataReciver , MatchIDFinderByHeroName , JsonWriter


def DataGather():

    
    dataBase = DataBaseHandler()
    #dataBase.CreateTable()

    MatchIDFinder = MatchIDFinderByHeroName()
    MatchIDFinder.GrabMatchID()

    dataBase.SaveMatchID(MatchIDFinder.matchIDSet)



    
    matchIDs = dataBase.ReadMatchIDTable()
    matchDataReciver = DataReciver()
    jsonWirter = JsonWriter()
    for  matchID in matchIDs :

        matchIDDate = matchDataReciver.GetMatchDetail(matchID)
        jsonWirter.Write(matchIDDate , str(matchID) + ".json")






if __name__ == "__main__" :
    DataGather()