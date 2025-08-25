/* PROC statements example */

/* PROC MEANS for descriptive statistics */
proc means data=sales_data n mean std min max;
    title 'Sales Data Summary Statistics';
    var revenue cost profit;
    class region product_type;
    output out=sales_summary 
           mean=avg_revenue avg_cost avg_profit
           std=std_revenue std_cost std_profit;
run;

/* PROC FREQ for frequency analysis */
proc freq data=customer_data;
    title 'Customer Demographics';
    tables region*customer_type / chisq;
    tables age_group / out=age_freq;
run;

/* PROC SORT for data sorting */
proc sort data=transaction_data out=sorted_transactions;
    by customer_id descending transaction_date;
run;

/* PROC SQL for data manipulation */
proc sql;
    title 'Top Customers by Revenue';
    create table top_customers as
    select customer_id,
           customer_name,
           region,
           sum(revenue) as total_revenue,
           count(*) as transaction_count,
           calculated total_revenue / calculated transaction_count as avg_transaction
    from transaction_data
    group by customer_id, customer_name, region
    having calculated total_revenue > 50000
    order by calculated total_revenue desc;
    
    /* Create a summary report */
    create table regional_summary as
    select region,
           count(distinct customer_id) as customer_count,
           sum(total_revenue) as region_revenue,
           avg(total_revenue) as avg_customer_revenue
    from top_customers
    group by region
    order by region_revenue desc;
quit;

/* PROC PRINT for output */
proc print data=top_customers(obs=10);
    title 'Top 10 Customers';
    var customer_name region total_revenue transaction_count avg_transaction;
    format total_revenue avg_transaction dollar12.2;
run;