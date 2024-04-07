from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Dict

class Image(BaseModel):
    uuid: str
    id: str
    orgUrl: str
    segUrl: str
    xaiUrl: str
    orgDim1Url: str
    orgDim2Url: str
    orgDim3Url: str
    segDim1Url: str
    segDim2Url: str
    segDim3Url: str
    xaiDim1Url: str
    xaiDim2Url: str
    xaiDim3Url: str
    imageName: str
    reportUrl: str
    imageExtention: str
    imageAnnotations: object
    comments: str

    @classmethod
    def from_mongo(cls, data: dict):
        if '_id' in data:
            data['id'] = objectid_to_string(data.pop('_id'))
        return cls(**data)


# Custom validator that converts ObjectId to string
def objectid_to_string(v):
    if isinstance(v, ObjectId):
        return str(v)
    return v

class AnnotationUpdateModel(BaseModel):
    uuid: str
    orgurl: str
    imageAnnotations: Dict[str, str]
