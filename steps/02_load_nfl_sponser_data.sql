USE ROLE TEAM2_ROLE;
USE WAREHOUSE TEAM2_DW;
-- ----------------------------------------------------------------------------
-- Step #1: Connect to NFL Sponser data in Marketplace
-- ----------------------------------------------------------------------------

/*---

Enter the Snowflake Data Cloud...
Connect to the "Relo Metrics: 2022-2023 NFL Post-Season Sponsorship Exposure Data" feed from Snowflake Data Marketplace by following these steps:
    -> Snowsight Home Button
         -> Marketplace
             -> Search: "2022-2023 NFL Post-Season Sponsorship Exposure Data" (and click on tile in results)
                 -> Click the blue "Get" button
                     -> Under "Options", adjust the Database name to read "NFL_SPONSOR" (all capital letters)
                        -> Grant to "TEAM2_ROLE"
 
---*/

-- Let's look at the data
SELECT * FROM NFL_SPONSOR.SPORTS.VW_SAMPLE_SPONSOR_EXPOSURES_BY_DAY LIMIT 100;
