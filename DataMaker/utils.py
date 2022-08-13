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
        self.directory = os.getcwd()[:len(os.getcwd()) - 9] + "MatchIDFiles" + "\\" + "MatchID.db"
        self.database = sqlite3.connect(self.directory)
        self.cursor = self.database.cursor()

    
    def CreateTable(self):
      
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
        print(matchIDs)
        return matchIDs


a = DataBaseHandler()
a.ReadMatchIDTable()