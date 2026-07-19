from pydantic import BaseModel


class PersonalityCreate(BaseModel):
    name: str
    description: str
    system_prompt: str
    voice: str


class PersonalityUpdate(BaseModel):
    name: str
    description: str
    system_prompt: str
    voice: str


class PersonalityResponse(BaseModel):
    id: int
    name: str
    description: str
    system_prompt: str
    voice: str

    class Config:
        from_attributes = True