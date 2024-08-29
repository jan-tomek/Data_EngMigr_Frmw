import argparse
import pandas as pd
from sqlalchemy import create_engine

parser = argparse.ArgumentParser(description='Extract metadata information from MS SQL database.')
parser.add_argument("--server",   required=True, help="Database server ip address.")
parser.add_argument("--username", required=True, help="Database user name.")
parser.add_argument("--password", required=True, help="Database user name password.")
parser.add_argument("--database", required=True, help="Database name to extract.")
parser.add_argument("--schema",   required=True, help="Schema name to extract.")

args = parser.parse_args()

print("#################################")
print("# MSSQLMetaExtractor.py started #")
print("#################################")

print("Connecting to "+'mssql+pyodbc://'+args.username+':'+'***********'+'@'+args.server+'/'+args.database+'?driver=ODBC+Driver+17+for+SQL+Server')
engine = create_engine('mssql+pyodbc://'+args.username+':'+args.password+'@'+args.server+'/'+args.database+'?driver=ODBC+Driver+17+for+SQL+Server')

meta_df = pd.read_sql("""
SELECT 
	 ROW_NUMBER() OVER(ORDER BY CO.TABLE_CATALOG,CO.TABLE_NAME,CO.ORDINAL_POSITION) AS Meta_Order
        ,'['+CO.TABLE_CATALOG+']' AS Facet_Name
	,'' AS Facet_Desc
	,'['+CO.TABLE_NAME+']' AS Table_Name
	,'' AS Table_Desc
	,'['+CO.COLUMN_NAME+']' AS Column_Name
	,'' AS Column_Desc
	,'['+CO.TABLE_CATALOG+'].['+CO.TABLE_NAME+'].['+CO.COLUMN_NAME+']' AS Column_Uniq_Id
	,CASE WHEN IS_NULLABLE = 'NO' THEN 'Y' ELSE 'N' END AS Mandatory
	,CASE WHEN COCOUS.CONSTRAINT_NAME IS NOT NULL THEN 'Y' ELSE 'N' END AS Is_PK
	,UPPER(DATA_TYPE)+CASE WHEN DATA_TYPE LIKE '%char%' THEN '('+CAST(CHARACTER_MAXIMUM_LENGTH AS VARCHAR(10))+')' ELSE '' END AS Data_Type
	,'NULL' AS Empty_Value
	,'' AS Relation_Filter
	,'['+COCOUS_FK_PK.TABLE_NAME_PK+']' AS Relationed_Table
	,'['+COCOUS_FK_PK.COLUMN_NAME_PK+']' AS Relationed_Column
	,'' AS Relationed_Filter
	,'' AS Detailed_Description
	,'' AS Sample
FROM INFORMATION_SCHEMA.COLUMNS AS CO
LEFT OUTER JOIN (SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE CONSTRAINT_TYPE = 'PRIMARY KEY') AS TACO 
ON CO.TABLE_CATALOG = TACO.TABLE_CATALOG AND CO.TABLE_SCHEMA = TACO.TABLE_SCHEMA AND CO.TABLE_NAME = TACO.TABLE_NAME
LEFT OUTER JOIN (SELECT * FROM INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE) AS COCOUS 
ON TACO.CONSTRAINT_CATALOG = COCOUS.CONSTRAINT_CATALOG AND TACO.CONSTRAINT_SCHEMA = COCOUS.CONSTRAINT_SCHEMA AND TACO.CONSTRAINT_NAME = COCOUS.CONSTRAINT_NAME AND CO.COLUMN_NAME = COCOUS.COLUMN_NAME
LEFT OUTER JOIN (
SELECT COCOUS_FK.TABLE_CATALOG AS TABLE_CATALOG_FK,COCOUS_FK.TABLE_SCHEMA AS TABLE_SCHEMA_FK,COCOUS_FK.TABLE_NAME AS TABLE_NAME_FK,COCOUS_FK.COLUMN_NAME AS COLUMN_NAME_FK
,COCOUS_PK.TABLE_CATALOG AS TABLE_CATALOG_PK,COCOUS_PK.TABLE_SCHEMA AS TABLE_SCHEMA_PK,COCOUS_PK.TABLE_NAME AS TABLE_NAME_PK,COCOUS_PK.COLUMN_NAME AS COLUMN_NAME_PK
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS TACO
INNER JOIN (SELECT * FROM INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE) AS COCOUS_FK 
ON TACO.CONSTRAINT_CATALOG = COCOUS_FK.CONSTRAINT_CATALOG AND TACO.CONSTRAINT_SCHEMA = COCOUS_FK.CONSTRAINT_SCHEMA AND TACO.CONSTRAINT_NAME = COCOUS_FK.CONSTRAINT_NAME
INNER JOIN INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS AS RECO
ON COCOUS_FK.CONSTRAINT_CATALOG = RECO.CONSTRAINT_CATALOG AND COCOUS_FK.CONSTRAINT_SCHEMA = RECO.CONSTRAINT_SCHEMA AND COCOUS_FK.CONSTRAINT_NAME = RECO.CONSTRAINT_NAME
INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE AS COCOUS_PK 
ON RECO.CONSTRAINT_CATALOG = COCOUS_PK.CONSTRAINT_CATALOG AND RECO.CONSTRAINT_SCHEMA = COCOUS_PK.CONSTRAINT_SCHEMA AND RECO.UNIQUE_CONSTRAINT_NAME = COCOUS_PK.CONSTRAINT_NAME
WHERE TACO.CONSTRAINT_TYPE = 'FOREIGN KEY') AS COCOUS_FK_PK
ON CO.TABLE_CATALOG = COCOUS_FK_PK.TABLE_CATALOG_FK AND CO.TABLE_SCHEMA = COCOUS_FK_PK.TABLE_SCHEMA_FK AND CO.TABLE_NAME = COCOUS_FK_PK.TABLE_NAME_FK AND CO.COLUMN_NAME = COCOUS_FK_PK.COLUMN_NAME_FK

"""+"WHERE CO.TABLE_SCHEMA = '"+args.schema+"' ORDER BY 1;" ,engine)

print("Extracted metadata overview:")
print(meta_df.info(show_counts=True))

print("Saving output:")
meta_df.to_excel("metadata_store.xlsx")  

print("Done.")

