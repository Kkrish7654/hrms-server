from pydantic import BaseModel, Field, ConfigDict


class LeavePolicyBase(BaseModel):
    policy_name: str = Field(..., max_length=150)
    details: dict


class LeavePolicyCreate(LeavePolicyBase):
    pass


class LeavePolicyUpdate(BaseModel):
    policy_name: str | None = Field(None, max_length=150)
    details: dict | None = None


class LeavePolicy(LeavePolicyBase):
    id: int

    model_config = ConfigDict(from_attributes=True)