# import the required modeuls 

# for connetcing to value steam api

import requests
# for creating json file 
import json
import os
# for extract match ID's 
from bs4 import BeautifulSoup

# load constance variable
from constance import key , heros

# for create database for storing matchID
import sqlite3
 


# define class for getting data form value steam api
class DataReciver() :

    def __init__(self) -> None :
        # this 3 variable define to have access to correct api system that we want to use
        # if you want more information rather than game define more options
        self.gameInterface = "IDOTA2Match_570"
        self.gameresource = "GetMatchDetails"
        self.gameVersion = "V001"
    

    def GetMatchDetail(self , matchID : int) -> dict :

        # create url of api
        url = "https://api.steampowered.com/" + self.gameInterface + "/" + self.gameresource + "/" + self.gameVersion +"/?match_id=" + str(matchID)  +"&format=JSON&key=" + key
        # get the data by get request
        data = requests.get(url)
        
        # return data in json format
        return data.json()


# define class to write json file when we capture all the data that we need
class JsonWriter():

    def __init__(self) -> None :

        self.directory = os.getcwd()[:len(os.getcwd()) - 9] + "JsonFiles"
        
    def Write(self , data : dict , filename : str) -> None:
        # create the path of json file
        fullAddress = self.directory + "\\" + filename
        with open(fullAddress , mode = "w") as jsonFile :
            # write the json file
            json.dump(data , jsonFile , indent = 4)
        
        return None


# In this class we will find the match ID's of game that played in high level of dota
class MatchIDFinderByHeroName():

    def __init__(self) -> None:
        self.matchIDSet = set()
    

    def GrabMatchID(self) -> None:

        for heroName in heros :
            print(heroName)
            # create url link for send request to grab data
            urlLink = "https://www.dota2protracker.com/hero/" + heroName.replace(" " , "%20")
            #print(urlLink)
            # get the content of page 
            htmlData = requests.get(urlLink).content
            
            # create BeautifulSoup object
            soup = BeautifulSoup(htmlData , "html.parser")

            # find all a tag with info opendota information
            aTagList = soup.find_all("a" , class_ = "info opendota")
            #print(aTagList)
            for item in aTagList :
                matchID = item["href"].split("/")[-1]
                self.matchIDSet.add(matchID)
                print(matchID)
        return None
    


class DataBaseHandler() :

    def __init__(self):
        self.directory = os.getcwd()[:len(os.getcwd()) - 9] + "MatchIDFiles" + "\\" + "Constance.db"
        self.database = sqlite3.connect(self.directory)
        self.cursor = self.database.cursor()

    
    def CreateTableMatchID(self):
      
        self.database.execute(
            """
            CREATE TABLE MatchID
            (MatchID INT PRIMARY KEY NOT NULL);
            """
        )
        print("data base and table created!")
        return None


    def SaveMatchID(self , matchIDset : set) :

        for item in matchIDset :

            try :
             
                self.cursor.execute("insert into MatchID (MatchID) values (?)" , (item,))
                self.database.commit()
            except:
                print("some problem happen")
        
        return None


    def ReadMatchIDTable(self):

        self.cursor.execute("select * from MatchID")
        matchIDs = self.cursor.fetchall()
        return matchIDs

    
    def CreateTablePlayerName(self):

        self.database.execute(
            """
            CREATE TABLE PlayerName
            (playerName text PRIMARY KEY NOT NULL);
            """
        )      

    def SavePlayerName(self , playerNameset : set) :

        for item in playerNameset :

            try :
             
                self.cursor.execute("insert into PlayerName (playerName) values (?)" , (item,))
                self.database.commit()
            except:
                print("some problem happen")
        
        return None


    def ReadPlayerNameTable(self):
        self.cursor.execute("select * from PlayerName")
        PlayerNames = self.cursor.fetchall()
        return PlayerNames



class PlayerNameFinder():


    def __init__(self) -> None:

        self.playerNameSet = set()


    def GrabPlayerName(self) :

        urlLink = "https://www.dota2protracker.com/"

        htmlData = requests.get(urlLink).content

        soup = BeautifulSoup(htmlData , "html.parser")

        tdTagList = soup.find_all("td" , class_ = "td-player")
        
        for tdTag in tdTagList :

            aTag = tdTag.find("a")
            
            if aTag :
                playerName = aTag["href"].split("/")[-1]
                #print(playerName)
                self.playerNameSet.add(playerName)

        return None


class MatchIDFinderByPlayerName():

    def __init__(self) -> None:
        self.matchIDSet = set()

    def GrabData(self) :
        dataBase = DataBaseHandler()
        
        playerNames = dataBase.ReadPlayerNameTable()
        for playerName in playerNames :
            print(playerName)
            urllink = "https://www.dota2protracker.com/player/" + playerName[0].replace(" " , "%20")

            try :
                htmlData = requests.get(urllink).content

                soup = BeautifulSoup(htmlData , "html.parser")

                aTags = soup.find_all("a" , class_ = "info opendota")

                for aTag in aTags:
                    matchID = aTag["href"].split("/")[-1]
                    print(matchID)
                    self.matchIDSet.add(matchID)
            except :
                pass


                


if __name__ == "__main__" : 
    a = MatchIDFinderByPlayerName()
    a.GrabData()
    

