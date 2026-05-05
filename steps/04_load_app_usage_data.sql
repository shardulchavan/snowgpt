USE ROLE TEAM2_ROLE;
USE WAREHOUSE TEAM2_DW;
 
 
-- ----------------------------------------------------------------------------
-- Step #1: Connect to app user data in Marketplace
-- ----------------------------------------------------------------------------
 
/*---
Enter the Snowflake Data Cloud...
 
Let's connect to the "App + Web Data" feed from
MFOUR Mobile research in the Snowflake Data Marketplace by following these steps:
 
    -> Snowsight Home Button
         -> Marketplace
             -> Search: "App + Web Data" (and click on tile in results)
                 -> Click the blue "Get" button
                     -> Under "Options", adjust the Database name to read "APP_USES" (all capital letters)
                        -> Grant to "TEAM2_ROLE"
   
That's it... we don't have to do anything from here to keep this data updated.
The provider will do that for us and data sharing means we are always seeing
whatever they they have published.
 
---*/
 
 
-- Let's look at the data - same 3-part naming convention as any other table
SELECT * FROM APP_USES.MFOUR_SHARE.APP_VISIT  LIMIT 100;