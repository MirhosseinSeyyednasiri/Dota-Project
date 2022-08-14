
from utils import DataBaseHandler , DataReciver , MatchIDFinderByHeroName , JsonWriter , PlayerNameFinder , MatchIDFinderByPlayerName




def DataBasePrepare():
    # create object of database to save constanceName
    dataBase = DataBaseHandler()
    try :
       dataBase.CreateTableMatchID()
    except:
        pass

    try :
        dataBase.CreateTablePlayerName()
    except :
        pass

    return dataBase

def MatchDataGather(flag = 0):

    
    dataBase = DataBasePrepare()
    

    matchIDFinderByHero = MatchIDFinderByHeroName()
    matchIDFinderByHero.GrabMatchID()
    
    matchIDFinderByPlayer = MatchIDFinderByPlayerName()
    matchIDFinderByPlayer.GrabData()

    dataBase.SaveMatchID(matchIDFinderByHero.matchIDSet)
    dataBase.SaveMatchID(matchIDFinderByPlayer.matchIDSet)

    print(len(matchIDFinderByHero.matchIDSet.intersection(matchIDFinderByPlayer.matchIDSet)))

    if flag == 1:
        matchIDs = dataBase.ReadMatchIDTable()
        matchDataReciver = DataReciver()
        jsonWirter = JsonWriter()
        for  matchID in matchIDs :

            matchIDDate = matchDataReciver.GetMatchDetail(matchID[0])
            jsonWirter.Write(matchIDDate , str(matchID[0]) + ".json")


def PlayerDataGather():

    dataBase = DataBasePrepare()
    playerNameFinder = PlayerNameFinder()
    playerNameFinder.GrabPlayerName()
    dataBase.SavePlayerName(playerNameFinder.playerNameSet)




if __name__ == "__main__" :
    MatchDataGather()