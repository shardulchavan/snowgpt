import time
from snowflake.snowpark import Session
import snowflake.snowpark.types as T
import snowflake.snowpark.functions as F


def table_exists(session, schema='', name=''):
    exists = session.sql("SELECT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}') AS TABLE_EXISTS".format(schema, name)).collect()[0]['TABLE_EXISTS']
    return exists

def create_sponsor_appusage_corr_table(session):
    SPONSOR_APPUSAGE_COLUMN= [T.StructField("SPONSOR", T.StringType()),
                                        T.StructField("TEAM_NAME", T.StringType()),
                                        T.StructField("PLATFORM_NAME", T.StringType()),
                                        T.StructField("TOTAL_IMPRESSIONS", T.IntegerType()),
                                        T.StructField("TOTAL_ENGAGEMENTS", T.IntegerType()),
                                        T.StructField("TOTAL_MEDIA_VALUE", T.DecimalType()),
                                        T.StructField("TOTAL_APP_USER", T.IntegerType()),
                                        T.StructField("TOTAL_TIME_SPENT", T.IntegerType())
                                    ]
    SPONSOR_APPUSAGE_COLUMN = [*SPONSOR_APPUSAGE_COLUMN, T.StructField("META_UPDATED_AT", T.TimestampType())]
    SPONSOR_APPUSAGE_SCHEMA = T.StructType(SPONSOR_APPUSAGE_COLUMN)

    dcm = session.create_dataframe([[None]*len(SPONSOR_APPUSAGE_SCHEMA.names)], schema=SPONSOR_APPUSAGE_SCHEMA) \
                        .na.drop() \
                        .write.mode('overwrite').save_as_table('ANALYTICS.SPONSORSHIP_APPUSAGES_CORR')
    dcm = session.table('ANALYTICS.SPONSORSHIP_APPUSAGES_CORR')


def merge_sponsor_appusage_metrics(session):
    _ = session.sql('ALTER WAREHOUSE TEAM2_DW SET WAREHOUSE_SIZE = XLARGE WAIT_FOR_COMPLETION = TRUE').collect()

    print("{} records in stream".format(session.table('TEAM2_DB.ANALYTICS.SPONSOR_EXPOSURE_STREAM').count()))

    sponser_agg = session.table("TEAM2_DB.ANALYTICS.SPONSOR_EXPOSURE_STREAM").group_by(F.col('TEAM_NAME'), F.col('STATE_CODE'), F.col('SPONSOR'), F.col('PLATFORM_NAME')) \
                                        .agg(F.sum(F.col("SUM_IMPRESSIONS")).as_("TOTAL_IMPRESSIONS"), \
                                             F.sum(F.col("ENGAGEMENTS")).as_("TOTAL_ENGAGEMENTS"), \
                                             F.sum(F.col("FULL_MEDIAL_VALUE")).as_("TOTAL_MEDIA_VALUE")) \
                                        .select(F.col('TEAM_NAME').alias("TEAM_NAME"), F.col("SPONSOR").alias("SPONSOR"), \
                                                F.col("PLATFORM_NAME").alias("PLATFORM_NAME"), F.col("TOTAL_IMPRESSIONS"), \
                                                F.col("TOTAL_ENGAGEMENTS"), F.col("TOTAL_MEDIA_VALUE"), F.col('STATE_CODE').alias("STATE"))
    
    sponser_agg.limit(5).show()

    usage_agg = session.table("TEAM2_DB.ANALYTICS.PANELIST_APP_USAGE_STREAM").group_by(F.col('APP_NAME'), F.col('STATE')) \
                        .agg(F.sum(F.col('DURATION_SEC')).as_('TOTAL_TIME_SPENT'),  \
                             F.count_distinct(F.col('BIRTHDAY')).as_('TOTAL_APP_USER')) \
                        .select(F.col('APP_NAME'), F.col('STATE'), F.col('TOTAL_TIME_SPENT'), F.col('TOTAL_APP_USER'))
                                
                            

    usage_agg.limit(5).show()


    sponsor_appusage_corr = sponser_agg.join(usage_agg, (F.lower(sponser_agg['PLATFORM_NAME'])==usage_agg['APP_NAME']) & (sponser_agg['STATE']==usage_agg['STATE']), \
                                             how='inner', rsuffix='_u') \
                                             .select("SPONSOR", "TEAM_NAME", "PLATFORM_NAME", "TOTAL_IMPRESSIONS", "TOTAL_ENGAGEMENTS", \
                                                     "TOTAL_MEDIA_VALUE", "TOTAL_APP_USER", "TOTAL_TIME_SPENT")

    
    sponsor_appusage_corr.limit(5).show()

    cols_to_update = {c: sponsor_appusage_corr[c] for c in sponsor_appusage_corr.schema.names}
    metadata_col_to_update = {"META_UPDATED_AT": F.current_timestamp()}
    updates = {**cols_to_update, **metadata_col_to_update}

    dcm = session.table('ANALYTICS.SPONSORSHIP_APPUSAGES_CORR')
    dcm.merge(sponsor_appusage_corr, (dcm['SPONSOR'] == sponsor_appusage_corr['SPONSOR']) & (dcm['TEAM_NAME'] == sponsor_appusage_corr['TEAM_NAME']) & (dcm['PLATFORM_NAME'] == sponsor_appusage_corr['PLATFORM_NAME']), \
                        [F.when_matched().update(updates), F.when_not_matched().insert(updates)])

    _ = session.sql('ALTER WAREHOUSE TEAM2_DW SET WAREHOUSE_SIZE = XSMALL').collect()

def main(session: Session) -> str:

    if not table_exists(session, schema='ANALYTICS', name='SPONSORSHIP_APPUSAGES_CORR'):
        create_sponsor_appusage_corr_table(session)
    
    merge_sponsor_appusage_metrics(session)

    return f"Successfully processed SPONSOR_APPUSAGE_CORREALATIONS"


if __name__ == '__main__':
    import os, sys
    current_dir = os.getcwd()
    parent_parent_dir = os.path.dirname(os.path.dirname(current_dir))
    sys.path.append(parent_parent_dir)

    from utils import snowpark_utils
    session = snowpark_utils.get_snowpark_session()

    if len(sys.argv) > 1:
        print(main(session, *sys.argv[1:]))  # type: ignore
    else:
        print(main(session))  # type: ignore

    session.close()