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
        

    # assume no more than 21 days during travel. This means day fields
    # cannot overlap 
    # its not possible for an animal to arrive before it departs
    # therefore departure is always before arrival

    #step 2:
    # calculate the difference between all the date components

    dateDiff_by_token_index=list()

    dateDiff_by_token_index[0]= arrival_date_parts[0]-departure_date_parts[0]
    dateDiff_by_token_index[1]=arrival_date_parts[1]-departure_date_parts[1]
    dateDiff_by_token_index[2]=arrival_date_parts[2]-departure_date_parts[2]

    # look for non zero differences
    


    
