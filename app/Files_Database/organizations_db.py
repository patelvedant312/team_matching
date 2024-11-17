# app/db/organizations_db.py

from app.models import Organization
from app import db

def get_all_organizations():
    return Organization.query.all()

def get_organization_by_id(org_id):
    organization = Organization.query.get(org_id)
    if not organization:
        raise ValueError("Organization not found")
    return organization

def create_new_organization(data):
    org = Organization(
        OrgName=data['OrgName']
    )
    db.session.add(org)
    db.session.commit()
    return org

def update_organization(org_id, data):
    organization = Organization.query.get(org_id)
    if not organization:
        raise ValueError("Organization not found")
    
    organization.OrgName = data.get('OrgName', organization.OrgName)
    # Update other fields as necessary
    
    db.session.commit()
    return organization

def delete_organization(org_id):
    organization = Organization.query.get(org_id)
    if not organization:
        raise ValueError("Organization not found")
    
    db.session.delete(organization)
    db.session.commit()
    return {"message": "Organization deleted successfully"}
