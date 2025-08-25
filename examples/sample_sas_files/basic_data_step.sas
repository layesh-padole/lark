/* Basic DATA step example */

data customers_clean;
    set raw_customers;
    
    /* Filter active customers only */
    where status = 'Active';
    
    /* Calculate customer metrics */
    customer_value = revenue - cost;
    profit_margin = customer_value / revenue * 100;
    
    /* Categorize customers */
    if customer_value >= 10000 then tier = 'Premium';
    else if customer_value >= 5000 then tier = 'Gold';
    else if customer_value >= 1000 then tier = 'Silver';
    else tier = 'Bronze';
    
    /* Format dates */
    join_year = year(join_date);
    
    /* Keep relevant variables */
    keep customer_id name region customer_value profit_margin tier join_year;
run;