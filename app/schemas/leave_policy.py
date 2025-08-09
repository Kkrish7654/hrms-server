from pydantic import BaseModel, Field


class LeavePolicyBase(BaseModel):
    policy_name: str = Field(..., max_length=150)
    details: dict


class LeavePolicyCreate(LeavePolicyBase):
    pass


class LeavePolicy(LeavePolicyBase):
    id: int

    class Config:
        orm_mode = True