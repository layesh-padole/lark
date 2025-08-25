/* Macro example with %let, %macro, and %do loops */

/* Define macro variables */
%let base_year = 2023;
%let regions = North South East West;
%let input_lib = rawdata;
%let output_lib = processed;

/* Macro to process data for a specific region and year */
%macro process_region(region, year);
    data &output_lib..sales_&region._&year;
        set &input_lib..raw_sales;
        where region = "&region" and year = &year;
        
        /* Calculate metrics */
        quarterly_avg = (q1_sales + q2_sales + q3_sales + q4_sales) / 4;
        growth_rate = (q4_sales - q1_sales) / q1_sales * 100;
        
        /* Performance categories */
        if quarterly_avg > 50000 then performance = 'Excellent';
        else if quarterly_avg > 25000 then performance = 'Good';
        else performance = 'Needs Improvement';
        
        format quarterly_avg dollar12.2;
        format growth_rate percent8.2;
    run;
    
    /* Create summary statistics */
    proc means data=&output_lib..sales_&region._&year noprint;
        var quarterly_avg growth_rate;
        output out=&output_lib..summary_&region._&year
               mean=avg_quarterly_avg avg_growth_rate
               std=std_quarterly_avg std_growth_rate;
    run;
%mend process_region;

/* Process multiple years using %do loop */
%do year = &base_year %to %eval(&base_year + 2);
    %process_region(North, &year);
    %process_region(South, &year);
    %process_region(East, &year);
    %process_region(West, &year);
%end;

/* Conditional processing based on macro variable */
%let create_combined = YES;

%if &create_combined = YES %then %do;
    /* Combine all regional data */
    data &output_lib..combined_sales;
        set &output_lib..sales_North_&base_year
            &output_lib..sales_South_&base_year
            &output_lib..sales_East_&base_year
            &output_lib..sales_West_&base_year;
        
        /* Add derived fields */
        total_sales = q1_sales + q2_sales + q3_sales + q4_sales;
        region_code = substr(region, 1, 1);
    run;
%end;