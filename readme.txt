Supported python-versions : 2.7,3.5


======================================================================================================================
Description:

	The python script is used to plot line and bar graphs from the tejas output files present in appropriate folder(s).

=======================================================================================================================
Usage:

	To run the python-script, type:
		python genericplt.py <(space-separated) path(s) to the folder(s) containing the tejas output files>

	Before running the python-script, the user must add appropriate values to the fields present in the genericplt.config file, which are as follows:

	a) GRAPH_TYPE			: To decide whether the graph should be a line graph or a bar graph (default- bar graph)
	b) TITLE				: The title of the graph (if the title string is empty, there will be no title in the output
								graph)
	c) X_LABEL				: The label on the x-axis
	d) Y_LABEL				: The label on the y-axis
	e) STRING_TO_SEARCH		: This attribute tells what string(s) is(are) to be searched in each of the tejas output files 
								to get the values to be plotted in a single graph. There are some standard values that can 
								be written in this field.
							  i)   ipc for Total-IPC
							  ii)  i1hitrate for Instruction Cache Hit Rate
							  iii) l1hitrate for L1-Cache Hit-Rate
							  iv)  l2hitrate for L2-Cache Hit-Rate
							  v)   totaltime for Total time taken
							  vi)  totalcycles for Total number of cycles
	f) BASE					: In case the graph is to be normalised, this attribute represents the base field, otherwise 
								it should be left empty
	g) PLOT_MEAN			: Can have values 'gmean' (to also plot GM), 'mean' (to also plot AM) or empty string in case 
								mean is not to be plotted
	h) LEGENDS				: Contains the legend names of the graph. In case they are not mentioned, then the legend 
								names are taken from the filenames present in each of the folders.
	i) X_TICKS_LABEL		: This field specifies the labels that should appear on the x-axis of the graph. In case this 
								field is empty, the labels are taken from the folder/file names by default.
	j) TITLE_FONT_SIZE		: To specify the font-size of the graph's title. The default value is 20.
	k) AXIS_LABEL_SIZE		: To specify the font-size of the labels of both axes. The default value is 15.
	l) MINOR_AXIS_LABEL_SIZE: To specify the font-size of the minor labels on both the axes as well as the legends. The 
								default value is 10.
	m) TILT_X_LABELS		: In case the minor labels on the x-axis have long names, they can be tilted by setting this 
								field 'yes' , otherwise the labels appear horizontally.
	n) LINE_WIDTH			: For line graph, this field specifies the width of the line(s). The default value is 3.
	o) LINE_SHADOW			: In line graph, this field can be set as 'yes' for shadow-effect.

==========================================================================================================================
Important points:

	1) The order of fields in the file genericplt.config should not be changed.
	2) The value in LEGENDS, STRING_TO_SEARCH, X_TICKS_LABEL fields should be comma-separated.

==========================================================================================================================

Sample run:
	
	python genericplt.py /home/$USER/<folder1> /home/$USER/<folder2>......

Sample config file:

	GRAPH_TYPE				:	"line"
	TITLE					:	"Percentage of block address misses"
	X_LABEL					:	"BENCHMARKS"
	Y_LABEL					:	"Block address misses(%)"
	STRING_TO_SEARCH		:	[For 0-10,For 10-100,For 100-1000]
	BASE					:	"10-100"
	PLOT_MEAN				:	"gmean"
	LEGENDS					:	[0-10,10-100,100-1000]
	X_TICKS_LABEL			:	[calculix,gcc,hmmer,soplex]
	TITLE_FONT_SIZE			:	"20"
	AXIS_LABEL_SIZE			:	"15"
	MINOR_AXIS_LABEL_SIZE	:	"10"
	TILT_X_LABELS			:	"yes"
	LINE_WIDTH				:	"5"
	LINE_SHADOW				:	"yes"

===========================================================================================================================
Scenario-1:
	A single folder containing multiple tejas-output files.

	In this case, the filenames are by default taken as the minor-labels on the x-axis.

Scenario-2:
	Multiple folders, each containing multiple tejas-output files.

	In this case, the folder names are by default considered as the minor-labels on the x-axis.
	The filenames are taken as the legend names (assuming the filenames are same in each of the folders).
