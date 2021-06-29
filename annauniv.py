import requests
import lxml.html as lh
import pandas as pd
import urllib.request
import threading
from bs4 import BeautifulSoup as BS
import multiprocessing
import time
from joblib import Parallel, delayed



class WS:
    def __init__(self,Link=None):
        self.Link = Link
        self.URL  = 'https://www.scimagojr.com/journalsearch.php?q='
        self.num_cores = multiprocessing.cpu_count()
    def Parsing(self):
        '''Parsing of Anna university Annexture table'''
        Soup  = BS(requests.get(self.Link).content,'html.parser')
        Table = Soup.find('table',{"class":"myTable"})
        self.Table_Data = []
        for row in Table.find_all('tr'):
            tmp = []
            column = row.find_all('td')
            for index in range(len(column)):
                tmp.append(column[index].text.strip())
            self.Table_Data.append(tmp)
        self.Table_Data = pd.DataFrame(self.Table_Data)
        return self.Table_Data
    def clean(self):
        """ Cleaning of Data Frame by rename column name and removing certain indexes"""
        self.Table_Data.rename(columns = self.Table_Data.iloc[2],inplace=True)
        self.Table_Data =  self.Table_Data.drop(labels=[0,1,2],axis = 0)
        return self.Table_Data
    def extraction(self):
        '''Extraction of ISSN and modifing DataFrame with added SCOPE of the corresponding table'''
        self.ISSN = self.Table_Data['ISSN']
        self.ISSN = [i.split('\n')[0] for i in self.ISSN]
        self.Link = [self.URL+i for i in self.ISSN]
    def Link_Parsing(self,Link):
        try:
            #print(Link[0])
            response = urllib.request.urlopen(Link[1]).read()
            print('__________________')
            
            soup = BS(response,'html.parser')
            print(Link[0],Link[1],"LINK:->")
            return 'https://www.scimagojr.com/'+soup.find('div', class_='search_results').a['href']
            
        except:
            print(Link[0],Link[1],"LINK:-(")
            return None
    def Scope_Parsing(self,url):
        try:
            print(url[1])
            response = urllib.request.urlopen(url[1]).read()
            print('__________________')
            soup = BS(response,'html.parser')
            print(url,"SCOPE:->")
            return(str(soup.find('div', class_='fullwidth').contents[2]))
            

        except:
          #print(":-(",url)
          #Notaccess.append(url)
          print(url[1],"SCOPE:-(")
          return (None)
        
    def Missing_Link(self):
        self.extraction()
        self.Missing_Index = self.Table_Data["Links"].index[self.Table_Data["Links"].isna()]
        return [self.URL+self.Table_Data["ISSN"][i]  for i in self.Missing_Index]
    def attach_link(self,Missing_Link):
        Missing_Link = pd.DataFrame(Missing_Link, index = self.Missing_Index,columns = ["Links"])
        for index in Missing_Link.index:
            if Missing_Link.loc[index].values == None:
                                    print('None')
            else:
                                    self.Table_Data["Links"][index] = Missing_Link.loc[index].values
                          
    def Missing_Scope_Link(self):
        Missing_Scopes = self.Table_Data["Scope"].index[self.Table_Data["Scope"].isna()]
        self.Missing_Links = self.Table_Data["Links"][Missing_Scopes]
        return self.Missing_Links
    
    def attach_Scope_Data(self,Missing_Data):
        Missing_Data = pd.DataFrame(Missing_Data,index = self.Missing_Links.index,columns = ["Scope"])
        
        for index in Missing_Data.index:
            if Missing_Data.loc[index].values == None:
                print('='*100)
            else:
                #print(Missing_Data.loc[index].values)
                self.Table_Data["Scope"][index] = Missing_Data.loc[index].values
        
    def link_go(self):
        self.Link1 = Parallel(n_jobs=self.num_cores)(delayed(self.Link_Parsing)(j,i) for j,i in enumerate(self.Link))
        
    def scope_go(self):
        self.scope = Parallel(n_jobs=self.num_cores)(delayed(self.Scope_Parsing)(j,i) for j,i in enumerate(self.Link1))