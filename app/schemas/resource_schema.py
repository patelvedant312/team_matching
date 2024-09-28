# /app/schemas/resource_schema.py
from marshmallow import Schema, fields

class ResourceSchema(Schema):
    ResourceID = fields.Int(dump_only=True)
    Name = fields.Str(required=True)
    Rate = fields.Float()
    PastJobTitles = fields.List(fields.Str())
    CurrentJobTitle = fields.Str()
    PastWorkDomains = fields.List(fields.Str())
    YearsOfExperience = fields.Int()
    AvailableDate = fields.Date()
    OrgID = fields.Int()
