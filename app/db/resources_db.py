from app.models.resource import Resource
from app import db

# Get all resources for a specific organization
def get_all_resources(org_id):
    return Resource.query.filter_by(OrgID=org_id).all()

# Get a specific resource by ID and organization
def get_resource_by_id(resource_id, org_id):
    return Resource.query.filter_by(ResourceID=resource_id, OrgID=org_id).first()

# Create a new resource
def create_new_resource(data):
    new_resource = Resource(
        Name=data.get('Name'),
        Rate=data.get('Rate'),
        Skills=data.get('Skills'),
        PastJobTitles=data.get('PastJobTitles'),
        Domain=data.get('Domain'),
        AvailableDate=data.get('AvailableDate'),
        OrgID=data.get('OrgID'),
        OnBench=data.get('OnBench', True),  # Default to True if not specified
    )
    db.session.add(new_resource)
    db.session.commit()
    return new_resource

# Update an existing resource
def update_resource(resource_id, org_id, data):
    resource = Resource.query.filter_by(ResourceID=resource_id, OrgID=org_id).first()
    if not resource:
        raise ValueError("Resource not found")

    resource.Name = data.get('Name', resource.Name)
    resource.Rate = data.get('Rate', resource.Rate)
    resource.Skills = data.get('Skills', resource.Skills)
    resource.PastJobTitles = data.get('PastJobTitles', resource.PastJobTitles)
    resource.Domain = data.get('Domain', resource.Domain)
    resource.AvailableDate = data.get('AvailableDate', resource.AvailableDate)
    resource.OnBench = data.get('OnBench', resource.OnBench)

    db.session.commit()
    return resource

# Delete a resource
def delete_resource(resource_id, org_id):
    resource = Resource.query.filter_by(ResourceID=resource_id, OrgID=org_id).first()
    if not resource:
        raise ValueError("Resource not found")

    db.session.delete(resource)
    db.session.commit()
    return {"message": "Resource deleted successfully"}
