import numpy as np
import pandas as pd 
import typing as tp 
from scipy import stats

class CSVRepo():
    def __init__(self, data):
        self.data = data

    def read(self, path :str):
        with open(path) as f:
            f = f.readlines()[10:]
        return CSVRepo(f)

    def splitting(self):
        return CSVRepo([f.split() for f in self.data])

    def convFloat(self):
        return CSVRepo([map(float, f) for f in self.data])
    
    def createDataFrame(self):
        df = pd.DataFrame(self.data)
        df.columns = ["id", "grainArea", "grainDiameter", "aspectRatio", "majorLength", "minorLength", "GOS", "misorientation"]
        return ebsdData(df)

        

class ebsdData():
    def __init__(self, data):
        self.data = data

    def calcGrainSize(self):
        self.data["grainSize"] = 2 * np.sqrt(self.data["grainArea"] / np.pi) * 1000
        return ebsdData(self.data)

    # average grain size in number fraction
    def calcGSNum(self) -> float:
        return np.mean(self.data["grainSize"])

    # average grain size in area fraction
    def calcGSArea(self) -> float:
        return np.average(self.data["grainSize"], weights=self.data["grainArea"])

    # Calculate standard error of grain size
    def calc_GS_sem(self) -> float:
        return stats.sem(self.data["grainSize"])

    # average grain aspect ratio in number fraction
    def calcGARNum(self) -> float:
        return np.mean(self.data["aspectRatio"])
    
    # average grain aspect ratio in area fraction
    def calcGARArea(self) -> float:
        return np.average(self.data["aspectRatio"], weights=self.data["grainArea"])
    
    # Calculate standard error of grain aspect ratio
    def calc_GAR_sem(self) -> float:
        return stats.sem(self.data["aspectRatio"])


    def calcEquiaxed(self) -> float:
        return np.sum(self.data[self.data["aspectRatio"] >= 0.5]["grainArea"]) / np.sum(self.data["grainArea"])
    
    def calcColmnar(self) -> float:
        return np.sum(self.data[self.data["aspectRatio"] < 0.5]["grainArea"]) / np.sum(self.data["grainArea"])





dd = CSVRepo(0)
dd = dd.read("./N1Ti1F-C14S-01_685C100h.txt")
dd = dd.splitting()
dd = dd.convFloat()
dd = dd.createDataFrame()
dd = dd.calcGrainSize()
gs = dd.calcGSNum()
gsarea = dd.calcGSArea()
equ = dd.calcEquiaxed()
sem = dd.calcGSSEM()
print(sem)