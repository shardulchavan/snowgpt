USE ROLE TEAM2_ROLE;
USE WAREHOUSE TEAM2_DW;
USE DATABASE CONSUMER_INFO;
 
-- ----------------------------------------------------------------------------
-- Step #1: Connect to Consumer info data in Marketplace
-- ----------------------------------------------------------------------------
 
/*---
Enter the Snowflake Data Cloud...
Connect to the "Alesco Consumer Database" feed from Snowflake Data Marketplace by following these steps:
    -> Snowsight Home Button
         -> Marketplace
             -> Search: "Alesco Consumer Database (sample)" (and click on tile in results)
                 -> Click the blue "Get" button
                     -> Under "Options", adjust the Database name to read "CONSUMER_INFO" (all capital letters)
                        -> Grant to "TEAM2_ROLE"
 
---*/
 
-- Let's look at the data
SELECT * FROM CONSUMER_INFO.PUBLIC.CONSUMER_TEST_DATA_VIEW LIMIT 100;
 