#!/usr/bin/env python
#_*_coding:utf-8_*_
from datetime import  *  
import time
import logger
import staticValue as static_value


#get logger
log = logger.log
log.propagate = False
#get date part of a String
#return formate yyyy-mm-dd
def getDateStr(str):
	_time_symbol = 'T'
	index = str.find(_time_symbol)
	if index == -1:
		raise Exception('String value:'+str+' is not the expected format:yyyy-mm-ddT00:00:00.000Z') 
	return str[0:index]

#transform a string to date type
#return formate date
def transformStrToDate(str):
	dateList = map(int,str.split('-'))
	return date(dateList[0],dateList[1],dateList[2])

#get passed months
#return [date1,date2....]
def getPassedMonths(s_date,reduce_months,month_range):
	if reduce_months==0:
		return month_range
	d = date(s_date.year,s_date.month,1)-timedelta(days=1)
	month_range.append(d)
	reduce_months = reduce_months-1
	return getPassedMonths(d,reduce_months,month_range)
	

##input -- [{squad iteration},{...}]
##output -- {'yyyy-mm-dd':[{squad 1 iteration 1 json data},{squad 1 iteration 2 json data}]}
def filter_data_by_Date(data):
	log.info('Filter the data by date..')
	result = {}
	passedMonths = getPassedMonths(date.today(),6,[])
	for i,value in enumerate(data):
		for mon in passedMonths:
			itEndDate = transformStrToDate(getDateStr(value.get('endDate')))
			if itEndDate.year==mon.year and itEndDate.month==mon.month:
				
				if result.get(str(mon)) != None:
					result.get(str(mon)).append(value)
				else:
					result.update({str(mon):[value]})
	return result

def getInt(obj):
	if obj == None:
		return 0
	return int(obj)
def getSpecificType(obj,func):
	if obj == None:
		return 0
	return func(obj)
def getFloat(obj,precision=1):
	if getSpecificType(obj,float) != None:
		return round(getSpecificType(obj,float),precision)
	return 0
##input {'yyyy-mm-dd':[{squad 1 iteration 1 json data},{squad 1 iteration 2 json data}]}
##output {'yyyy-mm-dd':{'Velocity':value,'Squads':value1...}}
def calculate_result(data):
	log.info('calculate the result..')
	#log.info(data)
	result = {}
	for k,its in data.iteritems():
		velocity=0
		teamId_set = set([]) #set size refer to the 'Squads'
		throughput = 0
		deployments = 0
		defects = 0
		cycleTimeInBacklog = 0
		cycleTimeWIP = 0
		teamsWithFiveToTwel=0
		teamsWithLessFive=0
		teamsWithMoreTwel=0
		teamSatisfaction = 0
		clientSatisfaction = 0
		#[{squad 1 iteration 1 json data},{squad 1 iteration 2 json data}]
		for it in its:
			teamMembers = getFloat(it.get('memberFte'))
			#make sure 1 team to be counted only 1 time
			if it.get('teamId') not in teamId_set:
				if teamMembers<5:
					teamsWithLessFive = teamsWithLessFive + 1
				elif teamMembers>12:
					teamsWithMoreTwel = teamsWithMoreTwel + 1
				else:
					teamsWithFiveToTwel = teamsWithFiveToTwel + 1
			velocity = velocity+getInt(it.get('storyPointsDelivered'))
			teamId_set.add(it.get('teamId'))
			throughput = throughput+getFloat(it.get('deliveredStories'))
			deployments = deployments+getInt(it.get('deployments'))
			defects = defects+getInt(it.get('defects'))
			cycleTimeInBacklog = cycleTimeInBacklog + getInt(it.get('cycleTimeInBacklog'))
			cycleTimeWIP= cycleTimeWIP+ getInt(it.get('cycleTimeWIP'))
			teamSatisfaction = teamSatisfaction+getFloat(it.get('teamSatisfaction'))
			clientSatisfaction = clientSatisfaction+getFloat(it.get('clientSatisfaction'))
		percentIter = 0
		if throughput!=0:
			percentIter = getFloat((teamsWithFiveToTwel/throughput)*100)
		values = [velocity,len(teamId_set),len(its),throughput,deployments,defects,cycleTimeInBacklog,cycleTimeWIP
		,percentIter,throughput,teamsWithFiveToTwel,teamsWithLessFive,teamsWithMoreTwel,teamSatisfaction,clientSatisfaction]
		temp = {}
		itersPerMonth = {k:temp}
		for i,v in enumerate(static_value._result_fields):
			temp.update({v:values[i]})
		result.update(itersPerMonth)
	return result
			
def	get_group_data(input_data):
	return calculate_result(filter_data_by_Date(input_data))

temp = {'2015-01-01':{1:1},'2014-05-08':{2:12},'2016-05-08':{3:12},'2012-05-08':{2:12}}
def sort_date(str_d1,str_d2):
	d1=transformStrToDate(str_d1)
	d2=transformStrToDate(str_d2)
	if d1>d2:
		return 1
	elif d1<d2:
		return -1
	return 0

def sort_dict(my_dict):
	result = []
	sorted_list = sorted(my_dict)
	log.info(sorted_list)
	for item in sorted_list:
		result.append({item : my_dict.get(item)})
	return result
# print temp
