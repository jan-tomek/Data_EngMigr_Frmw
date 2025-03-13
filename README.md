# Data Engineering/Migration Framework

This framework automates the generation and execution of SQL code by leveraging
metadata and mapping specifications. This approach is particularly beneficial 
for developing transformations targeting wide tables, as it guarantees that
the generated code consistently aligns with the target table's structure.

## Exec Tool

Tools to execute generated code.

### Code Runner

Windows batch files to parametrize and execute generated code. Dependencies implemented as waves, 
scripts in each wave executed without order (alphabetically by name) and waves in defined order 1,2,3... 

### Excel Loader

Loads Excel files into database. Two modes:
* Lookup - for each Excel file is created one table based on file name a loaded one sheet into
* Manual - for each sheet in Excel file is created table and loaded, file name is ignored  

## Meta Tools

Tool to work with metadata repository and generate code.

### Code Generator

Generate SQL based on table structure from **Metadata store** and mapping from **Mapping Excel**.

Mapping Excel contains sheet for each table (SELECT ...) and one sheet for all "table mappings", 
parts that generated SQL use to create query FROM. 

| Name            | Description                         | Sample                                                                                    |
|-----------------|-------------------------------------|-------------------------------------------------------------------------------------------|
| Meta_Order      | Ordering column                     | 1                                                                                         |
| Facet_Name      | Facet name                          | Customer Base                                                                             |
| Table_Name      | Table name                          | Customer                                                                                  |
| Column_Name     | Table column name                   | Customer Address ZIP                                                                      |
| Column_Desc     | Table column description            | Customer Address ZIP Code referencing to table Address for records with Country = 'LOCAL' |
| Column_Uniq_Id  | Unique column identifier            | [Customer Base].[Customer].[Customer Address ZIP]                                         |
| Mandatory       | Flag if column value is mandatory   | Y                                                                                         |
| Is_PK           | Column is part of table primary key | N                                                                                         |
| Data_Type       | Column data type                    | VARCHAR(5)                                                                                |
| Sample          | Column value sample                 | 15000                                                                                     |
| Src_Table       | Source table                        | ACCOUNT                                                                                   |
| Src_Column_Form | Source column or mapping formula    | CASE WHEN AC.ACTIVE = 1 THEN 'A' ELSE 'N' END                                             |
| Map_Note        | Note                                | Convert activity id to flag                                                               |

### MetaExtractor

Extract or import metadata from metadata source or source database.

**Metadata store** is simple Excel sheet metadata_store.xlsx (created by pandas) with structure:

| Name                 | Description                                                                               | Sample                                                                                                                                                                                                                                                                                      |
|----------------------|-------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Meta_Order           | Ordering column                                                                           | 1                                                                                                                                                                                                                                                                                           |
| Facet_Name           | Facet name                                                                                | Customer Base                                                                                                                                                                                                                                                                               |
| Facet_Desc           | Facet description                                                                         | Customer Base information area                                                                                                                                                                                                                                                              |
| Table_Name           | Table name                                                                                | Customer                                                                                                                                                                                                                                                                                    |
| Table_Desc           | Table description                                                                         | Customer Table with main customer info                                                                                                                                                                                                                                                      |
| Column_Name          | Table column name                                                                         | Customer Address ZIP                                                                                                                                                                                                                                                                        |
| Column_Desc          | Table column description                                                                  | Customer Address ZIP Code referencing to table Address for records with Country = 'LOCAL'                                                                                                                                                                                                   |
| Column_Uniq_Id       | Unique column identifier - can be concatenation of facet_name, table_name and column_name | [Customer Base].[Customer].[Customer Address ZIP]                                                                                                                                                                                                                                           |
| Mandatory            | Flag if column value is mandatory                                                         | Y                                                                                                                                                                                                                                                                                           |
| Is_PK                | Column is part of table primary key                                                       | N                                                                                                                                                                                                                                                                                           |
| Data_Type            | Column data type                                                                          | VARCHAR(5)                                                                                                                                                                                                                                                                                  |
| Empty_Value          | Value when column empty                                                                   | 0                                                                                                                                                                                                                                                                                           |
| Relation_Filter      | Relation is valid for subset of rows                                                      | Country = 'LOCAL'                                                                                                                                                                                                                                                                           |
| Relationed_Table     | Table to realtion with                                                                    | Address                                                                                                                                                                                                                                                                                     |
| Relationed_Column    | Columns in relationed table to create relation                                            | Address ZIP                                                                                                                                                                                                                                                                                 |
| Relationed_Filter    | Relation is valied only for subset in target table                                        | [Address Type] = 'CUSTOMER'                                                                                                                                                                                                                                                                 |
| Detailed_Description | Column description                                                                        | A ZIP Code (an acronym for Zone Improvement Plan[1]) is a system of postal codes used by the United States Postal Service (USPS). The term ZIP was chosen to suggest that the mail travels more efficiently and quickly[2] (zipping along) when senders use the code in the postal address. |
| Sample               | Column value sample                                                                       | 15000                                                                                                                                                                                                                                                                                       |

#### MSSQLMetaExtractor.py

Extract metadata from MS SQL server database

#### other db extractors e.g. PosgreSQL - TODO 
