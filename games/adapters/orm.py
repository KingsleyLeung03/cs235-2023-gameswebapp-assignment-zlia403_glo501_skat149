from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym

from games.domainmodel.model import * 

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

# create table 



# map model