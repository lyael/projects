import math

# my first project in python, this was the easiest language to set up and run in vs code console with nothing else set up on my computer

class Laws:
    def __init__(self, metal = 0, wood = 0, water = 0, fire = 0, earth = 0):
        self.metalMult = (metal / 100) + 1
        self.woodMult = (wood / 100) + 1
        self.waterMult = (water / 100) + 1
        self.fireMult = (fire / 100) + 1
        self.earthMult = (earth / 100) + 1
        
        self.points = 0

        # programming in the 0-50 leveling is a pain
        self.metalLvl = 50
        self.woodLvl = 50
        self.waterLvl = 50
        self.fireLvl = 50
        self.earthLvl = 50

    # sets law levels
    def setLvl(self, metal, wood, water, fire, earth):
        self.metalLvl = metal
        self.woodLvl = wood
        self.waterLvl = water
        self.fireLvl = fire
        self.earthLvl = earth

    # gains law points in hour increments, default time is 1 hour
    def gain(self, time = 1):
        # self.points += time * (self.lawGain('metal', self.metalLvl) + self.lawGain('wood', self.woodLvl) + self.lawGain('water', self.waterLvl) + self.lawGain('fire', self.fireLvl) + self.lawGain('earth', self.earthLvl))
        # self.points = math.floor(self.points)
        self.points += time * self.overallLawGain()
    
    # main leveling algorithm, runs until 10,000 law levels, gains in 1 hour increments
    def level(self, hours = 144):
        day = 1
        hour = 0
        target = ''

        # wanted do while loops, python gave me while true instead
        while True:
            # stop at 10k laws
            if(self.totalLawLevel() >= 10000):
                break
            
            # increment hour / day
            hour += 1
            if(hour > hours):
                hour = 1
                day += 1
            
            # gain 1 hour
            self.gain()

            # gets a new target law to level
            if(target == ''):
                target = self.chooseLaw()
            
            currentTargetLevel = self.getLevel(target)
            # hasLeveled = False

            # do the leveling
            while(self.points > self.lawCost(currentTargetLevel)):
                # stop leveling if its reached a new milestone
                # if((currentTargetLevel + 50) % 100 == 0):
                #     if(hasLeveled):
                #         break
                # hasLeveled = True

                # remove points and level
                self.points -= self.lawCost(currentTargetLevel)
                self.addLevel(target)
                currentTargetLevel += 1
                
                # stop leveling on milestones and print
                if((currentTargetLevel + 50) % 100 == 0 or currentTargetLevel == 2000):
                    print('Day ' + str(day) + ' - Hour ' + str(hour) + ' - leveled ' + target + ' to ' + str(currentTargetLevel))
                    target = ''
                    break
                
    # returns total law level
    def totalLawLevel(self):
        return self.metalLvl + self.woodLvl + self.waterLvl + self.fireLvl + self.earthLvl

    # chooses most efficient law to level
    def chooseLaw(self):
        names = ['metal', 'wood', 'water', 'fire', 'earth']
        best = 0
        bestName = ''
        for n in names:
            level = self.getLevel(n)

            # dont level past 2000
            if(level >= 2000):
                continue
            # check if everything else is 1950 before going past 1950
            if(level >= 1950):
                if(self.check1950()):
                    continue

            # calculate efficiency ratio
            cost = self.toNextMilestone(level)
            projectedGain = self.projectedLawGain(n, level) * 1000000
            projectedRatio = projectedGain / cost
            
            # set current best
            if(best < projectedRatio):
                best = projectedRatio
                bestName = n
        
        return bestName

    # returns cost to next milestone
    def toNextMilestone(self, level):
        num = level
        sum = 0
        while True:
            sum += self.lawCost(num)
            num += 1
            if((num + 50) % 100 == 0):
                return sum
            elif(num == 2000):
                return sum
            else:
                continue

    # returns cost of one law level in full
    def lawCost(self, level):
        if((level + 50) % 100 == 49):
            end = self.baseLawCost(level + 1) * 3.33
        else:
            end = self.baseLawCost(level) * 3.33
        
        return math.floor((self.baseLawCost(level) * 5) + end)

    # returns base cost of leveling a law, i.e. the cost of the five mini levels before the cost to increase the level itself
    # calculates cost using a multiplier of the base law gain, which was calculated by curve fitting to gathered data points    
    def baseLawCost(self, level):
        if(level >= 1000):
            mult = 0.0060301 * level - 0.0364739
            #mult = 0.006 * level
        else:
            mult = 0.0040325 * level - 0.0143307
            #mult = 0.004 * level
        cost = self.lawGain('base', level) * mult
        return cost

    # returns how much a law would gain if it was at its next milestone, for use in chooseLaw()
    def projectedLawGain(self, type, level):
        names = ['metal', 'wood', 'water', 'fire', 'earth']
        sum = 0
        for n in names:
            if(type == n):
                newLevel = level + (100 - ((level + 50) % 100))
            else:
                newLevel = level
            sum += self.lawGain(n, newLevel)
        return sum

    # returns combined law gain for all 5 laws    
    def overallLawGain(self):
        names = ['metal', 'wood', 'water', 'fire', 'earth']
        sum = 0
        for n in names:
            level = self.getLevel(n)
            sum += self.lawGain(n, level)
        return math.floor(sum)

    # returns hourly gain for one law, if type base is selected no law mult is added to the calculation
    def lawGain(self, type, level):
        mult = math.pow(2, math.floor((level + 50) / 100))
        if(type == 'base'):
            return mult * level * 480.5
        else:
            return mult * self.getMult(type) * level * 480.5

    def getMult(self, type):
        if(type == 'metal'):
            return self.metalMult
        if(type == 'wood'):
            return self.woodMult
        if(type == 'water'):
            return self.waterMult
        if(type == 'fire'):
            return self.fireMult
        if(type == 'earth'):
            return self.earthMult
        
    def getLevel(self, type):
        if(type == 'metal'):
            return self.metalLvl
        if(type == 'wood'):
            return self.woodLvl
        if(type == 'water'):
            return self.waterLvl
        if(type == 'fire'):
            return self.fireLvl
        if(type == 'earth'):
            return self.earthLvl
        
    def addLevel(self, type):
        if(type == 'metal'):
            self.metalLvl += 1
        if(type == 'wood'):
            self.woodLvl += 1
        if(type == 'water'):
            self.waterLvl += 1
        if(type == 'fire'):
            self.fireLvl += 1
        if(type == 'earth'):
            self.earthLvl += 1

    def check1950(self):
        if(self.metalLvl >= 1950 and self.woodLvl >= 1950 and self.waterLvl >= 1950 and self.fireLvl >= 1950 and self.earthLvl >= 1950):
            return False
        else:
            return True
        
# one = Laws(38, 60, 42, 50, 56)
# one.woodLvl = 1050
# one.gain(144)
# print(one.points)
# print(one.woodMult)
# print(one.lawGain('wood', one.woodLvl))

# two = Laws(0, 0, 0, 0, 0)
# two.gain(144)
# print(two.points)
# print(two.lawGain('wood', two.woodLvl))

# kosmo = Laws(60, 60, 60, 60, 64)
# kosmo.setLvl(1150, 1000, 1150, 1000, 1231)
# kosmo.gain(1)
# print('kosmo - expected 12.8b')
# print(kosmo.points)

# lyael = Laws(38, 60, 42, 50, 56)
# lyael.setLvl(950, 1050, 950, 950, 1043)
# lyael.gain(1)
# print('lyael - expected 4.47b')
# print(lyael.points)

# jankem = Laws(10, 8, 20, 10, 30)
# jankem.setLvl(936, 850, 850, 850, 950)
# jankem.gain(1)
# print('jankem - expected 1.57b')
# print(jankem.points)

# fatalis = Laws(60, 60, 62, 60, 64)
# fatalis.setLvl(1750, 1750, 1750, 1717, 1750)
# fatalis.gain(1)
# print('fatalis - expected 1596.79b')
# print(fatalis.points)

# alu = Laws(50, 60, 54, 60, 56)
# alu.setLvl(1450, 1550, 1450, 1456, 1450)
# alu.gain(1)
# print('alu (main) - expected 219.81b')
# print(alu.points)

# print('base cost 1249 ' + str(alu.baseLawCost(1249)))
# print('base cost 1250 ' + str(alu.baseLawCost(1250)))
# print('cost 950 ' + str(alu.lawCost(950)))
# print('cost 1050 ' + str(alu.lawCost(1050)))
# print('cost    0 ->   50: ' + f'{alu.toNextMilestone(0):,}')
# print('cost   50 ->  150: ' + f'{alu.toNextMilestone(50):,}')
# print('cost  150 ->  250: ' + f'{alu.toNextMilestone(150):,}')
# print('cost  250 ->  350: ' + f'{alu.toNextMilestone(250):,}')
# print('cost  350 ->  450: ' + f'{alu.toNextMilestone(350):,}')
# print('cost  450 ->  550: ' + f'{alu.toNextMilestone(450):,}')
# print('cost  550 ->  650: ' + f'{alu.toNextMilestone(550):,}')
# print('cost  650 ->  750: ' + f'{alu.toNextMilestone(650):,}')
# print('cost  750 ->  850: ' + f'{alu.toNextMilestone(750):,}')
# print('cost  850 ->  950: ' + f'{alu.toNextMilestone(850):,}')
# print('cost  950 -> 1050: ' + f'{alu.toNextMilestone(950):,}')
# print('cost 1050 -> 1150: ' + f'{alu.toNextMilestone(1050):,}')
# print('cost 1150 -> 1250: ' + f'{alu.toNextMilestone(1150):,}')
# print('cost 1250 -> 1350: ' + f'{alu.toNextMilestone(1250):,}')
# print('cost 1350 -> 1450: ' + f'{alu.toNextMilestone(1350):,}')
# print('cost 1450 -> 1550: ' + f'{alu.toNextMilestone(1450):,}')
# print('cost 1550 -> 1650: ' + f'{alu.toNextMilestone(1550):,}')
# print('cost 1650 -> 1750: ' + f'{alu.toNextMilestone(1650):,}')
# print('cost 1750 -> 1850: ' + f'{alu.toNextMilestone(1750):,}')
# print('cost 1850 -> 1950: ' + f'{alu.toNextMilestone(1850):,}')
# print('cost 1950 -> 2000: ' + f'{alu.toNextMilestone(1950):,}')

# print('cost 1000 -> 1250: ' + f'{alu.toNextMilestone(1000) + alu.toNextMilestone(1050) + alu.toNextMilestone(1150):,}')

# print(alu.chooseLaw())
            
# kosmo = Laws(60, 60, 60, 60, 64)
# kosmo.setLvl(1150, 1000, 1150, 1000, 1249)
# kosmo.level(188)

# lyael = Laws(38, 60, 42, 60, 56)
# lyael.setLvl(950, 1050, 950, 1050, 1050)
# lyael.level(144)

# base = Laws(0, 0, 0, 0, 0)
# base.setLvl(950, 950, 950, 950, 950)
# base.level(144)

invicta = Laws(30, 50, 36, 30, 40)
invicta.setLvl(1250, 1250, 1250, 1183, 1250)
invicta.level(181)

# print('cost 1950 -> 2000: ' + f'{lyael.toNextMilestone(1050):,}')

# invicta2 = Laws(0, 60, 0, 0, 0)
# invicta2.level(144)