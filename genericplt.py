#-----------------------Imports-------------------------------
import os
import matplotlib.pyplot as plt
import sys
import matplotlib.patheffects as path_effects
import statistics
import numpy as np
import glob
from scipy import stats
import re
from matplotlib import rcParams
from adjustText import adjust_text
# -------------------------------------------------------------


reload(sys)  	
sys.setdefaultencoding('utf8') 							# set the default encoding to utf-8 Foramt.

# --------------------------Set default font properties--------------------------------
rcParams['font.family'] = 'serif'
rcParams['font.sans-serif'] = ['Tahoma']
rcParams.update({'font.size':15})

color_arr = ['r','gold','blue','gold','c','m','crimson']		# colors array
marker_arr = ['o','*','s','^','.','p','h']				# marker type array
marker_size_arr = [12,12,8,10,10,10,10,10]				# size of the each marker type in marker array
# --------------------------------------------------------------------------------------


# function to perform sorting of file names in numerical order.
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


# function to label the bars of the rectangle in bar graph.
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.005*height,
                '%.2f' %(height),
                ha='center', va='bottom', fontsize=5)
                
# function to label the bars of the rectangle in bar graph.
def autolabelMean(rects):
	height = rects[-1].get_height()
	if (height >= 0):
		return ax.text(rects[-1].get_x() + rects[-1].get_width()/2., 1.005*height,
			'%.2f' %(height),
			ha='center', va='bottom', fontsize=5)

	else:
		return ax.text(rects[-1].get_x() + rects[-1].get_width()/2., 1.15*height,
			'%.2f' %(height),
			ha='center', va='bottom', fontsize=5)


# function to convert a m*n matrix to n*m matrix
def convertMat(mat):
	outMat = []
	rows = len(mat[0])
	cols = len(mat)
	for i in range(rows):
		temp = []
		for j in range(cols):
			temp.append(mat[j][i])
		outMat.append(temp)
	return outMat



#-----------------------------------Read config file and generate the graphs attributes--------------------------
config_file = open("genericplt.config")
graph_attrs = []
for line in config_file:
	arr = line.split()
	if (len(arr)>3):
		temp_str = ""
		for i in range(2,len(arr)):
			temp_str += arr[i] + " "
		arr = arr[:2]
		temp_str = temp_str[:-1]
		arr.append(temp_str)	

	list_a = []
	if (arr[2][0]  == '['):
		list_a = arr[2][1:-1].split(",")
	if (len(list_a) != 0):
		graph_attrs.append(list_a)
	else :
		graph_attrs.append(arr[2][1:-1])

# 									Graph Attributes 

benchmarks_arr				= []					# Array to store the names of the x-ticks-labels.
legend_arr					= []					# Array to store the legends array names.
TITLE_FONT_SIZE				= 20					# Font size of Title of the graph.
AXIS_LABEL_SIZE 			= 15					# Font size of axis (x,y) labels.
MINOR_AXIS_LABEL_SIZE 		= 10					# Font size of the minor axis labels.
TILT_X_AXIS 				= False					# bool to tilt the x-ticks-labels at 45 deg.
LINE_WIDTH					= 3						# Line width of the lines in line plot.
LINE_SHADOW					= False					# bool to draw shadow of lines in line plot.


if (graph_attrs[7][0] == ''):
	legend_arr = []
else:
	legend_arr = graph_attrs[7]

if (graph_attrs[8][0] == ''):
	benchmarks_arr = []
else:
	benchmarks_arr = graph_attrs[8]

if (graph_attrs[9] != ''):
	TITLE_FONT_SIZE = int(graph_attrs[9])

if (graph_attrs[10] != ''):
	AXIS_LABEL_SIZE = int (graph_attrs[10])

if (graph_attrs[11] != ''):
	MINOR_AXIS_LABEL_SIZE = int(graph_attrs[11])

if (graph_attrs[12].lower() == 'yes'):
	TILT_X_AXIS = True

if (graph_attrs[13] != ''):
	LINE_WIDTH = int(graph_attrs[13])

if (graph_attrs[14].lower() == 'yes'):
	LINE_SHADOW = True


rcParams.update({'font.size':MINOR_AXIS_LABEL_SIZE})


if (graph_attrs[4] == ""):
	print("Please mention the graphs to plot")
	exit()
# ---------------------------------------------------------------------------------------------


# ------------------------Parse the files and populate the list to plot graphs-------------------------

path_arr = sys.argv[1:]											# stores the list of the paths.
graph_carr = []													# Stores the values to be ploted in the graph.

# parse to each folder given in the argument(s)
for path in path_arr:
	if (len(path_arr) > 1):
		if (path[-1] == '/'):
			path = path[:-1]
		
		folder_name = path.split('/')[-1]
		if (graph_attrs[8][0] == ''):
			benchmarks_arr.append(folder_name)
		
	graph_arr = []
	# parse each files in the folder(s)
	for filename in sorted(glob.glob(os.path.join(path, '*.txt')),key = numericalSort ):
		
		file_read = open(filename, 'r')
		string = file_read.read()

		filename = filename.split('/')
		filename = filename[len(filename) - 1].split('.')[0]
		if (len(path_arr) == 1):
			if (graph_attrs[8][0] == ''):
				benchmarks_arr.append(filename)
		else:
			if (graph_attrs[7][0] == ''):
				legend_arr.append(filename)

		if (graph_attrs[4][0].lower() == 'ipc'):
			TotalIPC = re.search(r'Total IPC[\s\t]*=(.*)\s*in terms of micro-ops\n', string).group(1).strip()
			graph_arr.append(TotalIPC)

		elif (graph_attrs[4][0].lower() == 'i1hitrate'):
			I1_hit_Rate = re.search(r'I1 Hit-Rate[\s\t]*=(.*)\n', string).group(1).strip()
			graph_arr.append(I1_hit_Rate)

		elif (graph_attrs[4][0].lower() == 'l1hitrate'):
			L1_hit_Rate = re.search(r'L1 Hit-Rate[\s\t]*=(.*)\n', string).group(1).strip()
			graph_arr.append(L1_hit_Rate)

		elif (graph_attrs[4][0].lower() == 'l2hitrate'):
			L2_hit_Rate = re.search(r'L2 Hit-Rate[\s\t]*=(.*)\n', string).group(1).strip()
			graph_arr.append(L2_hit_Rate)

		elif (graph_attrs[4][0].lower() == 'totaltime'):
			TotalTime = str(max(list(map(float,re.findall(r'time taken[\s\t]*=(.*)\s*microseconds\n', string)))))
			graph_arr.append(TotalTime)

		elif (graph_attrs[4][0].lower() == 'totalcycles'):
			Total_cycles = re.search(r'Total Cycles taken[\s\t]*=(.*)\n', string).group(1).strip()
			graph_arr.append(Total_cycles)

		else:
			temp_arr = []
			for i in range(len(graph_attrs[4])):
				out_str = ""
				index = string.find(graph_attrs[4][i])
				if (index != -1):
					index_start1,index_start2 =string.find(" ", index + len(graph_attrs[4][i])),string.find("\t", index+ len(graph_attrs[4][i]))
					if (index_start1 != -1 and index_start2 != -1):
						index_start = min(index_start1,index_start2)
					elif (index_start1 != -1):
						index_start = index_start1
					else:
						index_start =index_start2
					index_end = string.find("\n" , index_start)
					out_str = string[index_start:index_end]
					out_str_arr = out_str.split()
					if (len(out_str_arr) == 1):
						temp_arr.append(out_str_arr[0])
					else :
						graph_arr.append(out_str_arr)
				else :
					print("Given string not found! Exiting.")
					exit()
			if (len(temp_arr) != 0):
				if(len(temp_arr) == 1):
					graph_arr.append(temp_arr[0])
				else:
					graph_arr.append(temp_arr)

	if(len(path_arr) == 1):
		graph_carr = graph_arr
	else:
		graph_carr.append(graph_arr)
		
print (graph_carr)
# -----------------------------------------------------------------------------------------------------------


# ------------------------------------Use graph_attrs and plot the graph------------------------------------
is_convert = True
if(type(graph_carr[0]).__name__ == 'str'):
	is_convert = False
	graph_carr = [graph_carr]

for i in range(len(graph_carr)):
	graph_carr[i] = list(map(float,graph_carr[i]))
	# graph_carr[i] = [(1-x)*1000 for x in graph_carr[i]]

if (is_convert):
	if (graph_attrs[5] != ''):
		if graph_attrs[5] in legend_arr:
			for j in range(len(legend_arr)):
				if(legend_arr[j] == graph_attrs[5]):
					break

			for i in range(len(graph_carr)):
				if (graph_carr[i][j] == 0):
					print ("\n---------------------------------------------------------------------------------")
					print('The field used as a base has value 0, so it can not be used as base. Exiting!')
					print ("---------------------------------------------------------------------------------\n")
					exit()
				graph_carr[i] = [(x-graph_carr[i][j])*100.0/graph_carr[i][j] + 100 for x in graph_carr[i]]
				#graph_carr[i] = [(x)/graph_carr[i][j] for x in graph_carr[i]]

		else:
			print ("\n---------------------------------------------------------------------------------")
			print('The base in a normalised graph should either be one of \nthe legends in the config file or one of the text filenames, \nwhich are by default the legend names. Exiting!')
			print ("---------------------------------------------------------------------------------\n")
			exit()
	graph_carr = convertMat(graph_carr)



fig, ax = plt.subplots()
ax.minorticks_on()
ax.yaxis.grid(True)
ax.set_axisbelow(True)
ax.tick_params(axis='x',which='minor',bottom='off')


width = 1.0/(len(graph_carr) + 1)

if(graph_attrs[6].lower() == 'gmean'):
	for i in range(len(graph_carr)):
		graph_carr[i].append(stats.gmean(graph_carr[i]))
	
	if (graph_attrs[0].lower() == 'line'):
		ax.axvline(x=len(benchmarks_arr) -1/2.0,linestyle='--',color='darkgrey')
	else :
		ax.axvline(x=len(benchmarks_arr) - width/2,linestyle='--',color='darkgrey')
	benchmarks_arr.append('mean')

elif(graph_attrs[6].lower() == 'mean'):
	for i in range(len(graph_carr)):
		graph_carr[i].append(statistics.mean(graph_carr[i]))
	
	if (graph_attrs[0].lower() == 'line'):
		ax.axvline(x=len(benchmarks_arr) -1/2.0,linestyle='--',color='darkgrey')
	else :
		ax.axvline(x=len(benchmarks_arr) - width/2,linestyle='--',color='darkgrey')
	benchmarks_arr.append('mean')

graph_type = 'bar'
if(graph_attrs[0].lower() == 'line'):
	graph_type = 'line'
	ax.set_xticks(range(len(benchmarks_arr)))
	ax.set_xticklabels(benchmarks_arr)
	if (TILT_X_AXIS):
		for tick in ax.get_xticklabels():
		    tick.set_rotation(45)
		    tick.set_ha('right')
		    tick.set_va('top')


	for i in range(len(graph_carr)):
		if (len(legend_arr) == 0):
			if (LINE_SHADOW):
				ax.plot(graph_carr[i], color=color_arr[i], marker = marker_arr[i], linewidth = LINE_WIDTH, markersize=10 ,path_effects=[path_effects.SimpleLineShadow(alpha=0.2),path_effects.Normal()])
			else :
				ax.plot(graph_carr[i], color=color_arr[i], marker = marker_arr[i], linewidth = LINE_WIDTH, markersize=10)
		else:
			if (LINE_SHADOW):
				ax.plot(graph_carr[i], label = legend_arr[i], color=color_arr[i], marker = marker_arr[i], linewidth = LINE_WIDTH, markersize=10,path_effects=[path_effects.SimpleLineShadow(alpha=0.2),path_effects.Normal()])
			else :
				ax.plot(graph_carr[i], label = legend_arr[i], color=color_arr[i], marker = marker_arr[i], linewidth = LINE_WIDTH, markersize=10)


	handles, labels = ax.get_legend_handles_labels()
	lgd = ax.legend(handles, labels, loc='center left',bbox_to_anchor=(1, 0.5))
else:
	N = len(benchmarks_arr)
	width = 1.0/(len(graph_carr) + 1)
	# width = 1.0/(len(graph_carr) + 4)
	ind = np.arange(N)
	ax.set_xticks(ind + width*len(graph_carr)/2.0 )
	ax.set_xticklabels(benchmarks_arr)
	if (TILT_X_AXIS):
		for tick in ax.get_xticklabels():
		    tick.set_rotation(45)
		    tick.set_ha('right')
		    tick.set_va('top')
	texts = []
	for i in range(len(graph_carr)):
		if (len(legend_arr) == 0):
			rects = ax.bar(ind+ i*width, graph_carr[i], width, edgecolor = 'w', linewidth = 0.5, align = 'edge',color = color_arr[i] )
		else:
			rects = ax.bar(ind+ i*width, graph_carr[i], width, edgecolor = 'w', linewidth = 0.5, label = legend_arr[i] , align = 'edge',color = color_arr[i] )
			# autolabel(rects)									# uncomment this if you want to show value of the bars in bar graph.
			texts.append(autolabelMean(rects))								# uncomment this if you want to show value of the last bar in bar graph.)

	adjust_text(texts , autoalign=False, only_move={'points':'y', 'text':'y'},ha='center', va='bottom')
	if (len(legend_arr) != 0):
		handles, labels = ax.get_legend_handles_labels()
		lgd = ax.legend(handles, labels, loc='upper center',bbox_to_anchor=(0.5, 1.15),ncol = len(graph_carr), frameon=False)

#graph_attrs[3] = graph_attrs[3].replace("\\" , "\\\\")
ylabel = graph_attrs[3].replace('\\n', '\n')
Xlabel = graph_attrs[2].replace('\\n', '\n')
ax.set_ylabel(ylabel,fontsize=AXIS_LABEL_SIZE)
if (graph_attrs[2] != ''):
	ax.set_xlabel(Xlabel,fontsize=AXIS_LABEL_SIZE)
if (graph_attrs[1] != ''):
	ax.set_title(graph_attrs[1] + "\n", fontsize=TITLE_FONT_SIZE, fontweight = 'bold')
# else:
	# ax.set_title(graph_attrs[1] , fontsize=TITLE_FONT_SIZE, fontweight = 'bold')
plt.tight_layout()

if (len(legend_arr) != 0):
	plt.savefig(graph_attrs[1]  + '_' +  graph_type+ '.svg', bbox_extra_artists=(lgd,), bbox_inches='tight')
else :
	plt.savefig( graph_attrs[1] + '_' +  graph_type + '.svg', bbox_inches='tight')
plt.show()


# --------------------------------------------------------------------------------------------------------------
