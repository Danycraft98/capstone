deliverable code goes here



## date algorithm

Date format detection
# {skip} jan feb mar apr may jun jul aug sept oct nov dec
Month_day_count[null,31,28,31,30,31,30,31,31,30,31,30,31]

#assume the same format for both departure, arrival and date
date_format_detection(departure_date,arrival_date, form_submit_date_YYYY_MM_DD)-> map{} :


	# first lets find all the simple cases
	# compare the form submit date and get the year.
	# find all the fields of the same year
	
	departure_date_parts[]=split_by_tokens(departure_date)
	arrival_date_parts[]=split_by_tokens(arrival_date)


    # look for four digit years
    int dateField_index=0
    
    dateFields=map()

    for (; dateField_index++; dateField_index<=2)

        # lets assume that the date field is always in the position if
        # even if the formats are different
       if (length(departure_date_parts[dateField_index])==4 or length(arrival_date_parts[dateFIeld_index])==4))
            dateFields{"departure_year"}=departure_date_parts[dateField_index]
            dateFields{"arrival_year"}=arrival_date_parts[dateFIeld_index]
        

    # precondition (assume) no more than 15 days during travel.
    # precondition (assume) date formats are inteneded to be same for arrival and departure
    # its not possible for an animal to arrive before it departs
    # therefore departure is always before arrival

    #step 2:
    # Count the number of differences.
    	int diff_counter=0
     	date_diff_map=map();
	for (dateField_index=0; dateField_index++; dateField_index<=2)
 		date_diff=arrival_date_parts[dateField_index]-departure_date_parts[dateField_index]
   		date_diff_map{dateField_index}=date_diff
     
 		if ( absolute_value(date_diff) !=0)
   			diff_counter++
 # scenario 1		
	# if there are three differences then we've crossed a year boundary. 
 	# The year always moves forward and will have a diff of 1
  	# The month will always have a -11 diff and 01 in the arrival and 12 in the departure
   	# the remaining will be date
	if (diff_counter==3)
 		for ( key: date_diff_map.keys())
 			if date_diff_map{key}==1
   				dateFields{"departure_year"}=departure_date_parts[dateField_index]
            			dateFields{"arrival_year"}=arrival_date_parts[dateFIeld_index]
	      		# remove key from possible values
	 			date_diff_map.remove_key(key)
    				break
    		for (key: date_diff_map.keys())
     			if date_diff_map{key}==-11
				if departure_date_parts[dateField_index]== 12 and arrival_date_parts[dateFIeld_index]==1
    					dateFields{"departure_month"}=departure_date_parts[dateField_index]
            				dateFields{"arrival_month"}=arrival_date_parts[dateFIeld_index]
				# remove key
    				date_diff_map.remove(key)
				break

    		# there should only be one key left and that is the date
      		for (key: date_diff_map.keys())
			dateFields{"departure_month"}=departure_date_parts[dateField_index]
            		dateFields{"arrival_month"}=arrival_date_parts[dateFIeld_index]

       # scenario 2
       # it means we are in the same year
       # we just have to find the year and elminate it.
       if (diff_counter==2)
       		for (key: date_diff_map.keys())
				if departure_date_parts[dateField_index]== 12 and arrival_date_parts[dateFIeld_index]==1
    					dateFields{"departure_year"}=departure_date_parts[dateField_index]
            				dateFields{"arrival_year"}=arrival_date_parts[dateFIeld_index]
					# remove key
    					date_diff_map.remove(key)
					break
     		dateKeys[] date_diff_map.keys()
       		# there are only two possiblities
	 	# DD MM or MM DD , just eliminate  the one that vilolates the precondition on duration

   # secnario 3
   # only one difference
   # that diff is the day. Since the current year is 2025, no month can be 25th month so find the year and the remaing is the month

   #secario 4
   # no difference, ie everything was done on the same day. 
   # raise a warning
			 		
       		
					
				      
   	
 		
     
    


    
