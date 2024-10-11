# db/resources_db.py

from app.models import db, Resource

def get_all_resources():
    return Resource.query.all()

def get_resource_by_id(resource_id):
    resource = Resource.query.get(resource_id)
    if not resource:
        raise ValueError("Resource not found")
    return resource

def create_new_resource(data):
    resource = Resource(
        Name=data['Name'],
        Rate=data['Rate'],
        Skills=data['Skills'],
        PastJobTitles=data['PastJobTitles'],
        Domain=data['Domain'],
        AvailableDate=data.get('AvailableDate'),
        OrgID=data['OrgID'],
        TeamID=data.get('TeamID')  # TeamID is optional
    )
    db.session.add(resource)
    db.session.commit()
    return resource

def update_resource(resource_id, data):
    resource = get_resource_by_id(resource_id)
    resource.Name = data['Name']
    resource.Rate = data['Rate']
    resource.Skills = data['Skills']
    resource.PastJobTitles = data['PastJobTitles']
    resource.Domain = data['Domain']
    resource.AvailableDate = data.get('AvailableDate')
    resource.OrgID = data['OrgID']
    resource.TeamID = data.get('TeamID')  # TeamID is optional
    
    db.session.commit()
    return resource

def delete_resource(resource_id):
    resource = get_resource_by_id(resource_id)
    db.session.delete(resource)
    db.session.commit()
    return {"message": "Resource deleted successfully"}
