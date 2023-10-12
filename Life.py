from sys import stdout
from typing import Union
import random
import time
class StringPlus:
    def __init__(self,inputString:str):
        self.__string = inputString
    @property
    def String(self) -> str:
        return self.__string
    @String.setter
    def String(self,inputString:str):
        self.__string = inputString
    def ignoreFormat(self) -> str:
        return self.String.casefold().replace(" ","")
    def printSlow(self):
        for i in self.String.upper():
            stdout.write(i)
            stdout.flush()
            time.sleep(0.01)
        del self
    def inputSlow(self) -> str:
        self.printSlow()
        StringPlus.barrier()
        returnValue = input()
        StringPlus.barrier()
        return returnValue
    @staticmethod
    def barrier():
        StringPlus("|-----------------|\n").printSlow()
class SystemFunctions:
    @staticmethod
    def weightedRandomChoice(inputList:tuple,inputAmount:int) -> list:  #((option,weight),(option,weight))
        optionList = []
        probabilityTuple = []
        for i,o in inputList:
            optionList.append(i)
            probabilityTuple.append(o)
        return random.choices(optionList,weights=tuple(probabilityTuple),k=inputAmount)
    @staticmethod
    def minMax(inputValue:Union[int,float],minVal:Union[int,float],maxVal:Union[int,float]) -> Union[int,float]:
        return minVal if inputValue < minVal else maxVal if inputValue > maxVal else inputValue
class GameObject:
    def __init__(self,inputDictionary:dict):
        if inputDictionary != {}:
            self.__name = inputDictionary["Name"]
            self.__price = inputDictionary["Price"]
            self.__quantity = 1
            self.__demandPrice = inputDictionary["Price"]
    @property
    def Name(self) -> str:
        return self.__name
    @property
    def Price(self) -> float:
        return self.__price
    @property
    def Quantity(self) -> int:
        return self.__quantity
    @Quantity.setter
    def Quantity(self,inputQuantity:int):
        self.__quantity = int(SystemFunctions.minMax(inputQuantity,0,float("inf")))
    @property
    def DemandPrice(self) -> float:
        return self.__demandPrice
    @DemandPrice.setter
    def DemandPrice(self,inputDemandPrice:float): 
        self.__demandPrice = SystemFunctions.minMax(inputDemandPrice,1,float("inf"))
class Pets(GameObject):
    def __init__(self,inputDictionary:dict):
        super().__init__(inputDictionary)
        Pets.hungryPrice = 7.0 if not hasattr(Pets,"hungryPrice") else Pets.hungryPrice
        Pets.thirstyPrice = 7.0 if not hasattr(Pets,"thirstyPrice") else Pets.thirstyPrice
        if inputDictionary != {}:
            self.__level = 0
            self.__nickname = ""
            self.__happiness = 0.0
            self.__isHungry = False
            self.__isThirsty = False
            self.__isEquipped = False
    @staticmethod
    def __repr__() -> str:
        return "Pets"
    @property
    def Level(self) -> int:
        return self.__level
    @Level.setter
    def Level(self,inputLevel:int):
        self.__level = int(SystemFunctions.minMax(inputLevel,1,float("inf")))
    @property
    def Nickname(self) -> str:
        return self.__nickname
    @Nickname.setter
    def Nickname(self,inputNickname:str):
        self.__nickname = inputNickname
    @property
    def Happiness(self) -> float:
        return self.__happiness
    @Happiness.setter
    def Happiness(self,inputHappiness:float):
        self.__happiness = SystemFunctions.minMax(inputHappiness,0,100)
    @property
    def IsHungry(self) -> bool:
        return self.__isHungry
    @IsHungry.setter
    def IsHungry(self,inputIsHungry:bool):
        self.__isHungry = inputIsHungry
    @property
    def IsThirsty(self) -> bool:
        return self.__isThirsty
    @IsThirsty.setter
    def IsThirsty(self,inputIsThirsty:bool):
        self.__isThirsty = inputIsThirsty
    @property
    def IsEquipped(self) -> bool:
        return self.__isEquipped
    @IsEquipped.setter
    def IsEquipped(self,inputIsEquipped:bool):
        self.__isEquipped = inputIsEquipped
    @staticmethod
    def handleMultiplePets(inputPet:'Pets',optionList:list,functionToBeCalled) -> bool:                                     # TODO: MAKE DECORATOR
        while True:
            try:
                StringPlus(f"you have multiple of {inputPet.Name}\n").printSlow()
                for i in optionList:
                    StringPlus(f" - {i.Name} (LVL {i.Level}{' - EQUIPPED' if i.IsEquipped else ''})\n").printSlow()
                petChoice = StringPlus("Which one? (LVL)\n").inputSlow()
                if StringPlus(petChoice).ignoreFormat() == "x":
                    return False
                else:
                    petChoice = int(petChoice)
            except ValueError:
                StringPlus(f"that isn't an integer\n").printSlow()
                StringPlus.barrier()
            for i in optionList:
                if i.Level == petChoice:
                    functionToBeCalled(i)
                    return True
            StringPlus(f"no pet had a level of {petChoice}\n")
            StringPlus.barrier()
    def display(self):
        displayName = f"|--{self.Name} ({self.Level})--|" if self.Nickname == "" else f"|--{self.Nickname} ({self.Name}) ({self.Level})--|"
        [StringPlus(f"{i}\n").printSlow() for i in (displayName,f"happiness: {self.Happiness} / 100",f" - {'hungry' if self.IsHungry else 'full'}",f" - {'thirsty' if self.IsThirsty else 'hydrated'}")]
    def randomTask(self):
        def handleHunger(inputHunger:bool):
            self.IsHungry = inputHunger
        def handleThirst(inputThirst:bool):
            self.IsThirsty = inputThirst
        if SystemFunctions.weightedRandomChoice(((True,3),(False,5)),1)[0]:     # TODO: MAKE MORE READABLE
            SystemFunctions.weightedRandomChoice(((handleHunger,1),(handleThirst,1)),1)[0]()
    def feed(self,inputFood:'Consumables') -> float:
        returnPrice = 0.0
        if inputFood.AffectsFeed:
            self.IsHungry = False
            returnPrice += Pets.hungryPrice
        if inputFood.AffectsDrink:
            self.IsThirsty = False
            returnPrice += Pets.thirstyPrice
        self.Happiness += inputFood.HappinessEffect
        StringPlus(f"you fed {self.Name} {inputFood.Name}\n").printSlow()
        StringPlus.barrier()
        return returnPrice
    def equipUnequip(self,inputEquipUnequip:bool):
        StringPlus(f"{self.Name} was {'equipped' if inputEquipUnequip else 'unequipped'}\n").printSlow()
        self.IsEquipped = inputEquipUnequip
        StringPlus.barrier()
class Consumables(GameObject):
    def __init__(self,inputDictionary:dict):
        super().__init__(inputDictionary)
        if inputDictionary != {}:
            self.__happinessEffect = inputDictionary["Happiness Effect"]
            self.__affectsFeed = inputDictionary["Affects Feed"]
            self.__affectsDrink = inputDictionary["Affects Drink"]
            self.__consumeFunction = inputDictionary["Consume Function"]
    @staticmethod
    def __repr__() -> str:
        return "Consumables"
    @property
    def HappinessEffect(self) -> float:
        return self.__happinessEffect
    @HappinessEffect.setter
    def HappinessEffect(self,inputHappinessEffect:float):
        self.__happinessEffect = inputHappinessEffect
    @property
    def AffectsFeed(self) -> bool:
        return self.__affectsFeed
    @property
    def AffectsDrink(self) -> bool:
        return self.__affectsDrink
    @property
    def ConsumeFunction(self):
        return self.__consumeFunction
    @ConsumeFunction.setter
    def ConsumeFunction(self,inputConsumeFunction):
        self.__consumeFunction = inputConsumeFunction
    def consume(self) -> dict:
        StringPlus(f"consuming {self.Name}...\n").printSlow()
        self.ConsumeFunction()
        StringPlus(f"{self.Name} was consumed\n").printSlow()
        [StringPlus(f" + {i}\n") for i in (f"{self.HappinessEffect} Happiness",)]
        StringPlus.barrier()
        return {"Happiness Effect":self.HappinessEffect}
class ConsumablesOptions:
    @staticmethod
    def eat():
        pass
class Collectables(GameObject):
    def __init__(self,inputDictionary:dict):
        super().__init__(inputDictionary)
    @staticmethod
    def __repr__() -> str:
        return "Collectables"
class Npc():
    def __init__(self,inputDictionary:dict):
        self.__name = inputDictionary["Name"]
        self.__stock = inputDictionary["Stock"]
        self.changeStockPrices()
        self.__intelligence = random.randint(inputDictionary["Minimum Intelligence"],inputDictionary["Maximum Intelligence"])
        self.__maxIntellignece = inputDictionary["Maximum Intelligence"]
        self.__emotionalIntelligence = random.randint(inputDictionary["Minimum Emotional Intelligence"],inputDictionary["Maximum Emotional Intelligence"])
        self.__maxEmotionalIntellignece = inputDictionary["Maximum Emotional Intelligence"]
        self.__balance = random.randint(inputDictionary[0],inputDictionary[1])
    @property
    def Name(self) -> str:
        return self.__name
    @property
    def Stock(self) -> list:
        return self.__stock
    @property
    def Intelligence(self) -> int:
        return self.__intelligence
    @property
    def MaxIntelligence(self) -> int:
        return self.__maxIntellignece
    @property
    def EmotionalIntelligence(self) -> int:
        return self.__emotionalIntelligence
    @property
    def MaxEmotionalIntelligence(self) -> int:
        return self.__maxEmotionalIntellignece
    @property
    def Balance(self) -> float:
        return self.__balance
    @Balance.setter
    def Balance(self,inputBalance:float):
        self.__balance = inputBalance
    def calculateSellPrice(self,inputItem:GameObject) -> float:
        offset = (2,4) if self.Intelligence > self.EmotionalIntelligence else (-2,2)
        return (inputItem.Price * (1 + (self.Intelligence / (1.5 * self.MaxIntelligence)))) + random.randint(offset[0],offset[1])
    def calculateDemandPrice(self,inputItem:GameObject) -> float:
        offset = (-4,0) if self.Intelligence > self.EmotionalIntelligence else (0,5)
        return (inputItem.Price * (1 + (self.Intelligence / (1.5 * self.MaxIntelligence)))) + random.randint(offset[0],offset[1])
    def changeStockPrices(self):
        for i in self.Stock:
            i.DemandPrice = self.calculateSellPrice(i)
class GameData:
    # PETS
    dog = {"Name":"Dog","Price":15.0,"Type":Pets}
    # CONSUMABLES
    apple = {"Name":"Apple","Price":1.5,"Type":Consumables,"Happiness Effect":1.0,"Affects Feed":True,"Affects Drink":False,"Consume Function":ConsumablesOptions.eat}
    # NPCS
    tempTemplate = {"Name":"STR","Stock":[],"Minimum Intelligence":0,"Maximum Intelligence":0,"Minimum Emotional Intelligence":0,"Maximum Emotional Intelligence":0,"Balance":(0,0)}
class Player:
    def __init__(self,name):
        self.__name = name
        self.__balance = 25.0
        self.__inventory = {Pets:[],Consumables:[],Collectables:[]}
        self.__happiness = 0.0
        self.__intelligence = 0.0
        self.__socialness = 0.0
        self.__equippedPet = None
    @property
    def Name(self) -> str:
        return self.__name
    @Name.setter
    def Name(self,inputName:str):
        self.__name = inputName
    @property
    def Balance(self) -> float:
        return self.__balance
    @Balance.setter
    def Balance(self,inputBalance:float):
        self.__balance = inputBalance
    @property
    def Inventory(self) -> dict:
        return self.__inventory
    @property
    def Happiness(self) -> float:
        return self.__happiness
    @Happiness.setter
    def Happiness(self,inputHappiness:float):
        self.__happiness = SystemFunctions.minMax(inputHappiness,0,100)
    @property
    def Intelligence(self) -> float:
        return self.__intelligence
    @Intelligence.setter
    def Intelligence(self,inputIntelligence:float):
        self.__intelligence = SystemFunctions.minMax(inputIntelligence,0,100)
    @property
    def Socialness(self) -> float:
        return self.__socialness
    @Socialness.setter
    def Socialness(self,inputSocialness:float):
        self.__socialness = SystemFunctions.minMax(inputSocialness,0,100)
    @property
    def EquippedPet(self) -> Union[Pets,None]:
        return self.__equippedPet
    @EquippedPet.setter
    def EquippedPet(self,inputPet:Union[Pets,None]):
        self.__equippedPet = inputPet
    def addToInventory(self,inputObject:GameObject) -> None:
        if inputObject.__class__ in (Consumables,Collectables):
            for i in self.Inventory[type(inputObject)]:
                if i.Name == inputObject.Name:
                    i.Quantity += 1
                    return
        self.Inventory[type(inputObject)].append(inputObject)
    def removeFromInventory(self,inputObject:GameObject,inputAge:Union[None,int]) -> bool:
        if inputObject.__class__ in (Consumables,Collectables):
            for i in self.Inventory[inputObject.__class__]:
                if i.Name == inputObject.Name:
                    i.Quantity -= 1
                    if i.Quantity <= 0:
                        self.Inventory[inputObject.__class__].remove(i) 
                        del i
                    return True
            return False
        elif inputObject.__class__ == Pets:
            petList = [i for i in self.Inventory[Pets] if ((i.Name,i.Age) == (inputObject.Name,inputAge))]
            if len(petList) != 0:
                self.Inventory[Pets].remove(petList[0])
                self.EquippedPet = None if (self.EquippedPet.Name,self.EquippedPet.Age) == (inputObject.Name,inputAge) else self.EquippedPet
                return True
            else:
                return False
    def displayBalance(self):
        StringPlus(f"your balance is: $ {self.Balance}\n").printSlow()
        StringPlus.barrier()
    def displayInventory(self,invFilter:Union[GameObject,None]) -> bool:
        if invFilter == None:
            if [self.Inventory[i] for i in self.Inventory] != [[] for i in range(len(self.Inventory))]:
                for i in self.Inventory:
                    if self.Inventory[i] != []:
                        StringPlus(f"|--{i({})}--|\n").printSlow()
                        [StringPlus(f" - {o.Name} ({f'LVL {o.Level} - EQUIPPED' if ((o.__class__,self.EquippedPet) == (Pets,o)) else f'LVL {o.Level}' if (o.__class__ == Pets) else o.Quantity if (o.__class__ in (Consumables,Collectables)) else ''})\n").printSlow() for o in self.Inventory[i]]
                StringPlus.barrier()
                return True
            else:
                StringPlus("your inventory is empty\n").printSlow()
                StringPlus.barrier()
                return False
        elif issubclass(invFilter,GameObject):
            if self.Inventory[invFilter] != []:
                StringPlus(f"|--{invFilter({})}--|\n").printSlow()
                [StringPlus(f" - {i.Name} ({f'LVL {i.Level} - EQUIPPED' if ((invFilter,self.EquippedPet) == (Pets,i)) else f'LVL {i.Level}' if (invFilter == Pets) else i.Quantity if (invFilter in (Consumables,Collectables)) else ''})\n").printSlow() for i in self.Inventory[invFilter]]
                StringPlus.barrier()
                return True
            else:
                StringPlus(f"you have no {invFilter({})}\n").printSlow()
                StringPlus.barrier()
                return False
    def consume(self,inputConsumable:Consumables) -> bool:
        if inputConsumable.Name in [i.Name for i in self.Inventory[Consumables]]:
            consumableStats = inputConsumable.consume()
            self.Happiness += consumableStats["Happiness Effect"]
            self.removeFromInventory(inputConsumable,None)
            return True
        else:
            return False
    def feedPet(self,inputConsumable:Consumables) -> bool:
        if inputConsumable.Name in [i.Name for i in self.Inventory[Consumables]] and self.EquippedPet != None:
            self.Balance += self.EquippedPet.feed(inputConsumable)
            self.removeFromInventory(inputConsumable,None)
            return True
        else:
            return False
    def equipPet(self,inputPet:Union[Pets,None]):
        self.EquippedPet = inputPet
        if self.EquippedPet.__class__ == Pets:
            self.EquippedPet.equipUnequip(True)
    def actInteractPet(self) -> bool:
        while True:
            self.EquippedPet.display()
            petAction = StringPlus(f"what is your action? (x)\n - feed (f)\n").inputSlow()
            if StringPlus(petAction).ignoreFormat() == "x":
                return False
            elif StringPlus(petAction).ignoreFormat() in ("f",):
                if self.displayInventory(Consumables):
                    chosenConsumable = StringPlus(f"what do you want to feed {self.EquippedPet.Name}? (x)\n").inputSlow()
                    for i in self.Inventory[Consumables]:
                        if StringPlus(i.Name).ignoreFormat() == StringPlus(chosenConsumable).ignoreFormat():
                            self.feedPet(i)
                            return True
            StringPlus(f"that isn't an option\n").printSlow()
            StringPlus.barrier()
    def actInventory(self) -> bool:
        optionList = []
        if self.displayInventory(None):
            while True:
                inventoryAction = StringPlus(f"what is your action? (x)\n - EQUIP PET (E)\n - CONSUME (C)\n - INTERACT PET (I)\n").inputSlow()
                if StringPlus(inventoryAction).ignoreFormat() == "x":
                    return False
                elif StringPlus(inventoryAction).ignoreFormat() in ("e","c"):
                    actionDict = {"e":{"Name":"Equip","Filter":Pets,"Reference":"who"},"c":{"Name":"Consume","Filter":Consumables,"Reference":"what"}}[StringPlus(inventoryAction).ignoreFormat()]
                    if not self.displayInventory(actionDict["Filter"]):
                        return False
                    furtherAction = StringPlus(StringPlus(f"{actionDict['Reference']} do you want to {actionDict['Name']}?\n").inputSlow()).ignoreFormat()
                    for i in self.Inventory[actionDict["Filter"]]:
                        if StringPlus(i.Name).ignoreFormat() == furtherAction:
                            {Pets:optionList.append,Consumables:self.consume}[actionDict["Filter"]](i)
                            if i.__class__ != Pets:
                                return True
                    if len(optionList) > 1:
                        Pets.handleMultiplePets(optionList[0],optionList,self.equipPet)
                        return True
                    elif len(optionList) == 1:
                        self.equipPet(optionList[0])
                        return True
                    StringPlus(f"that isn't an option\n").printSlow()
                    StringPlus.barrier()
                elif StringPlus(inventoryAction).ignoreFormat() == "i":
                    if self.EquippedPet != None:
                        self.actInteractPet()
                        return True
                    else:
                        StringPlus(f"you don't have a pet equipped\n").printSlow()
                        StringPlus.barrier()
                        return False
                StringPlus(f"that isn't an option\n").printSlow()
                StringPlus.barrier()
class Main():
    @staticmethod
    def main():
        player = Player(StringPlus(f"what is your name?\n").inputSlow())
        StringPlus(f"welcome {player.Name}\n").printSlow()
        StringPlus.barrier()
Main.main()