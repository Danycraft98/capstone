deliverable code goes here



## date algorithm

Date format detection

if (date_contains([A-Za-z])
	return split_based_on_alpha_num_date(date)

date_format_detection(departure_date,arrival_date, form_date)-> map{} :
	
	#assume the same date format across both fields

	departure_date_parts[]=split_by_tokens(departure_date)
	arrival_date_parts[]=split_by_tokens(arrival_date)

	#assumptions 
	#the departure date and arrival date are with in 1 month of each other
	#departure is always before* arrival, ie. arrival will always have "higher value"

	datePartDiffs[]= int[3]
	datePartDiff[0]= arrival_date_parts[0]-departure_date_parts[0]
	datePartsDiff[1]=arrival_date_parts[1]-departure_date_parts[1]
	datePartsDiff[2]=arrival_date_parts[2]-departure_date_parts[2]
	
	# if there are none zero values in all the fields then the field 
	# with a diff of 1 is the year, the field with with a diff of -11 is the month and the other must be days
	dateIndexMap=Map{};

	if (datePartsDiff[0]!=0 && datePartsDiff[0]!=0 && datePartsDiff[0]!=0)

		#look for the year
		if datePartsDiff[0]==1
			dateIndexMap{Year}=0
		else datePartsDiff[1]==1
			dateIndexMap{Year}=1
		else datePartsDiff[2]==1
			dateIndexMap{Year}=2
		
		# In this case the moth should be -11			
		#look for the year
		if datePartsDiff[0]==1
			dateIndexMap{Year}=0
		else datePartsDiff[1]==1
			dateIndexMap{Year}=1
		else datePartsDiff[2]==1
			dateIndexMap{Year}=2 


 
	
