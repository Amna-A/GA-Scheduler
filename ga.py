
# -*- coding: utf-8 -*-import datetime
import json
import calendar
import pprint
import random
import numpy as np
import datetime
import prettytable as prettytable
import random as rnd

NUMB_OF_ELITE_SCHEDULES=3
TOURNAMENT_SELECTION_SIZE=9
MUTATION_RATE=0.3
POPULATION_SIZE=30


######################################################################################
############################# the GA class contains function for crossover and mutation
class GeneticAlgorithm:
  def evolve(self,population): return self._mutate_population(self._crossover_population(population))
  
  def _crossover_population(self,pop):
    crossoverpopulation=Population(0)
    for i in range (0,NUMB_OF_ELITE_SCHEDULES):
      crossoverpopulation.get_schedules().append(pop.get_schedules()[i])
    i=NUMB_OF_ELITE_SCHEDULES
    j=i
    while j<POPULATION_SIZE:
      sche1=self._select_population(pop).get_schedules()[0]
      sche2=self._select_population(pop).get_schedules()[0]

      crossoverpopulation.get_schedules().append(self._crossover_schedule(sche1,sche2))
      j+=1
    return crossoverpopulation

  def _mutate_population(self,population): 
    for i in range(NUMB_OF_ELITE_SCHEDULES,POPULATION_SIZE):
      self._mutate_schedule(population.get_schedules()[i])
    return population
  
  def _crossover_schedule(self,sche1,sche2):
    crossover_schedule=Schedule().initialize()
    for i in range(0,len(crossover_schedule.get_classes())):
      if(rnd.random()>0.5): 
        crossover_schedule.get_classes()[i]=sche1.get_classes()[i]
      else: 
        crossover_schedule.get_classes()[i]=sche2.get_classes()[i]
    return crossover_schedule

  def _mutate_schedule(self,msche):
    schedule=Schedule().initialize()
    for i in range(0,len(msche.get_classes())):
      if(MUTATION_RATE>rnd.random()): 
          msche.get_classes()[i]=schedule.get_classes()[i]
    return msche

  def _select_population(self,pop):
    pop1=pop
    t_pop=Population(0)
    i=0
    while i<TOURNAMENT_SELECTION_SIZE:
      t_pop.get_schedules().append(pop1.get_schedules()[rnd.randrange(0,POPULATION_SIZE)])
      i+=1
    t_pop.get_schedules().sort(key=lambda x: x.get_fitness(),reverse=True)
    return t_pop


###############################################################################
# a single schedule will contains number of classes and the schedule will be added to population also calculate fitness for the schedule

class Schedule:
    '''  '''
    def __init__(self):
        self._data=data
        self._classes=[]
        self._numberOfConflicts=0
        self._fitness=-1
        self._classNumb=0
        self._isFitnessChanged=True
    def get_classes(self):
        self._isFitnessChanged=True
        return self._classes

    def get_numberOfConflicts(self): return self._numberOfConflicts
    def get_fitness(self):
        if(self._isFitnessChanged==True):
            self._fitness=self.calculate_fitness()
            self._isFitnessChanged=False
        return self._fitness
    def initialize(self):
        depts=self._data.get_depts()
        self._groups=['a','b','c']
        tclasses=[]
        s=0
        for i in range(0,len(depts)):
            courses=depts[i].get_courses()
            for j in range(0,len(courses)):
                for k in range(0,len(self._groups)):

                  newClass=Class(self._classNumb,depts[i],courses[j],self._groups[k])
                  self._classNumb+=1
                  newClass.set_meetingTime(data.get_meetingTimes()[rnd.randrange(0,len(data.get_meetingTimes()))])
                  newClass.set_room(data.get_rooms()[rnd.randrange(0,len(data.get_rooms()))])
                  newClass.set_instructor(courses[j].get_instructors())
                  tclasses.append(newClass)
        while s in range(0,len(tclasses)):
            s=rnd.randrange(0,len(tclasses))
            ######## we can increase the number of classes in a week by changing the below condition (here I'm chosing 75 )
            if len(self._classes)<75:
                self._classes.append(tclasses[s])
            else: break
        return self
    ##################### the method that claculate fitness evaluating the constraints
    def calculate_fitness(self):
        self._numberOfConflicts=0
        classes=self.get_classes()
        for i in range(0,len(classes)):
            for j in range(0,len(classes)):
                if(j>=i):
                    if(classes[i].get_meetingTime()==classes[j].get_meetingTime() and classes[i].get_id()!=classes[j].get_id()):
                        if(classes[i].get_room()== classes[j].get_room()):self._numberOfConflicts+=1
                        if(classes[i].get_instructor()== classes[j].get_instructor()):self._numberOfConflicts+=1
                    if(classes[i].get_meetingTime()==classes[j].get_meetingTime() and classes[i].get_room()== classes[j].get_room()):
                        if(classes[i].get_group()!= classes[j].get_group() and classes[i].get_dept()==classes[j].get_dept()):self._numberOfConflicts+=1
                    if(classes[i].get_meetingTime()==classes[j].get_meetingTime() and classes[i].get_room()!= classes[j].get_room()):
                        if(classes[i].get_group()== classes[j].get_group() and classes[i].get_dept()==classes[j].get_dept()):self._numberOfConflicts+=1
        return 1/((1.0*self._numberOfConflicts+1))

    def __str__(self):
        returnValue=""
        for i in range(0,len(self._classes)-1):
            returnValue+=str(self._classes[i])+", "
        returnValue+=str(self._classes[len(self._classes)-1])
        return returnValue
##################################################################################
##############################################################################
# this class will be member of a schdule.
class Class:
    def __init__(self,id,dept,course,group):
        self._id=id
        self._dept=dept
        self._course=course
        self._group=group
        self._intructor=None
        self._meetingTime=None
        self._room=None
    def get_id(self): return self._id
    def get_dept(self): return self._dept
    def get_course(self): return self._course
    def get_instructor(self): return self._instructor
    def get_group(self): return self._group
    def get_meetingTime(self): return self._meetingTime
    def get_room(self): return self._room
    def set_instructor(self,instructor): self._instructor=instructor
    def set_meetingTime(self,meetingTime): self._meetingTime=meetingTime
    def set_room(self,room): self._room=room
    def __str__(self):
        return str(self._dept.get_name())+"," +str(self._course.get_name())+"," + str(self._room.get_number())+ ","+ str(self._instructor.get_name())+ "," + str(self._meetingTime.get_time())+", "+str(self.get_group())

################################################################
# deaprtment which contains refrences to the courses in department
class Department:
    '''  '''
    def __init__(self,name,courses):
        self._name=name
        self._courses=courses
    def get_name(self): return self._name
    def get_courses(self): return self._courses


########################################################
#room data of a class
class Room:
    '''  '''
    def __init__(self,number):
        self._number=number
    def get_number(self): return self._number
    


##################################################
# to hold meeting time for a class
class MeetingTime:
    '''  '''
    def __init__(self,id,time):
        self._id=id
        self._time=time
    def get_id(self): return self._id
    def get_time(self): return self._time


####################################################################
#to hold the instuctor data
class Instructor:
    '''  '''
    def __init__(self,id,name):
        self._id=id
        self._name=name

    def get_id(self): return self._id
    def get_name(self): return self._name
    def __str__(self): return self._name
    
    
##########################################################################
#####to hold the course data and refrence to the instructor
class Course:
    '''  '''
    def __init__(self,number,name):
        self._number=number
        self._name=name
        self._instructors=None
    def get_number(self): return self._number
    def get_name(self): return self._name
    def get_instructors(self): return self._instructors
    def set_instructors(self,instructors): self._instructors=instructors
    def __str__(self): return self._name



################################################################
#create size number of schedules for initial population and then this population is optimized using GA 
class Population:
    def __init__(self,size):
        self._size=size
        self._data=data
        self._schedules=[]
        #self._sche=Schedule()
        for i in range(0,size): self._schedules.append(Schedule().initialize())
    def get_schedules(self): return self._schedules
    
###########################################################################
# this class load the data from json file into the repective object i.e intructor,course,department
class Data:
  def generate_time_slots():
    start_time = '9:00' #earliest class starts at 9:00
    end_time = '18:00' #last class ends at 18:00
    slot_time = 60 #no lecture more than 1 hour

    # Start date from today to next 5 day
    start_date = datetime.datetime.now().date()
    end_date = datetime.datetime.now().date() + datetime.timedelta(days=5)

    days = []
    date = start_date
    while date <= end_date:
      hours = []
      time = datetime.datetime.strptime(start_time, '%H:%M')
      end = datetime.datetime.strptime(end_time, '%H:%M')
      while time <= end:
        hours.append(str(date)+" "+time.strftime("%H:%M"))
        time += datetime.timedelta(minutes=slot_time)
      date += datetime.timedelta(days=1)
      days.append(hours)

    return days
  def dataset():
    
            info = open('fall_2020_dataset.json')
            data = json.load(info)
    
            if data is not None:
                data = data
        
            return data  


  ROOMS=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  MEETING_TIMES=generate_time_slots()
    
  data1 = dataset()
  list_of_departments = [dept for dept in data1]
  list_of_instructurs=[]
  list_of_courses=[]
  for i in range(0,4):
    list_of_instructurs .append( [key["instructor_name"] for key in data1[list_of_departments[i]]])
    list_of_courses .append( [key["course name"] for key in data1[list_of_departments[i]]])


  def __init__(self):
      self._rooms=[];self._meetingTimes=[]; self._instructors=[]; self._courses=[] 
      for i in range(0,len(self.ROOMS)):
          self._rooms.append(Room("r"+str(i)))

      for i in range(0,len(self.MEETING_TIMES)):
          for j in range(0,len(self.MEETING_TIMES[i])):
              self._meetingTimes.append(MeetingTime(str(i)+str(j),self.MEETING_TIMES[i][j]))

      for i in range(0,len(self.list_of_instructurs)):
          for j in range(0,len(self.list_of_instructurs[i])):
              self._instructors.append(Instructor(str(i)+str(j),self.list_of_instructurs[i][j])) 
        
      for i in range(0,len(self.list_of_courses)):
          for j in range(0,len(self.list_of_instructurs[i])):
              self._courses.append(Course(i,self.list_of_courses[i][j]))
        
      for i in range(0,len(self._courses)):
          self._courses[i].set_instructors(self._instructors[i])
      dept1=Department("CME",self._courses[0:2])
      dept2=Department("CIVE",self._courses[2:26])
      dept3=Department("ECE",self._courses[26:47])
      dept4=Department("MECE",self._courses[47:-1])
      self._depts=[dept1,dept2,dept3,dept4]
        
      self._numberOfClasses=0
      for i in range(0,len(self._depts)):
          self._numberOfClasses+=len(self._depts[i].get_courses())

  def get_rooms(self): return self._rooms
  def get_instructors(self): return self._instructors
  def get_courses(self): return self._courses
  def get_depts(self): return self._depts
  def get_meetingTimes(self): return self._meetingTimes
  def get_numberOfClasses(self): return self._numberOfClasses
  
  
###########################################################################
#this class used for display purposes
class DisplayMgr:
  def print_dept(self):
    depts=data.get_depts()
    availableDeptsTable=prettytable.PrettyTable(['depts','courses'])
    for i in range(0,len(depts)):
      courses=depts.__getitem__(i).get_courses()
      tempStr="["
      for j in range(0,len(courses)-1):
        tempStr+=courses[j].__str__()+", "
      tempStr+=courses[len(courses)-1].__str__()+" ]"
      availableDeptsTable.add_row([depts.__getitem__(i).get_name(),tempStr])
    print(availableDeptsTable)
  def print_available_data(self):
    print(">   All Available Data")
    self.print_dept()
        #self.print_course()
        #self.print_room()
        #self.print_instructor()
        #self.print_meeting_times()
  
  def print_generation(self,population):
    table1=prettytable.PrettyTable(['schedules #','fitnesss','No.of Conflicts'])
    schedules=population.get_schedules()
    for i in range(0,len(schedules)):
      table1.add_row([str(i),schedules[i].get_fitness(),schedules[i].get_numberOfConflicts()])
    print(table1)
    
    
  def print_schedule(self,schedule):
    table1=prettytable.PrettyTable(['class #','dept','class detail'])
    classes=schedule.get_classes()
    for i in range(0,len(classes)):
      table1.add_row([str(i),classes[i].get_dept().get_name(),classes[i].__str__()])
    print(table1)


############################################################3
################################################################33
# GA main 
data=Data()
displayMgr=DisplayMgr()
generationNumber=0
print("\n >Generation # "+str(generationNumber))
population=Population(POPULATION_SIZE)
pprint.pprint(population.get_schedules().sort(key=lambda x: x.get_fitness(),reverse=True))
displayMgr.print_available_data()
displayMgr.print_generation(population)

ga=GeneticAlgorithm()
while(population.get_schedules()[0].get_fitness() != 1.0):
  generationNumber+=1
  print("\n> Generation #"+str(generationNumber))
  population=ga.evolve(population)
  population.get_schedules().sort(key=lambda x: x.get_fitness(),reverse=True)
  displayMgr.print_generation(population)
  if(population.get_schedules()[0].get_fitness() == 1.0 or population.get_schedules()[0].get_numberOfConflicts()==0):
    break
  print("\n\n")

population.get_schedules().sort(key=lambda x: x.get_fitness(),reverse=True)
displayMgr.print_schedule(population.get_schedules()[0])