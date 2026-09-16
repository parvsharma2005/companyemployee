from enum import Enum


class LeaveRequestStatusEnum(Enum):

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

    @classmethod
    def choices(cls):
        return [
            (
                key.value,
                key.name.replace("_", " ").title()
            )
            for key in cls
        ]

    @classmethod
    def values(cls):
        return {
            key.value
            for key in cls
        }


class LeaveTypeEnum(Enum):

    CASUAL = "casual"
    SICK = "sick"
    EARNED = "earned"
    SHORT = "short"
    ANNUAL = "annual"
    EMERGENCY = "emergency"
    PREVIOUS = "previous"

    @classmethod
    def choices(cls):
        return [
            (
                key.value,
                key.name.replace("_", " ").title()
            )
            for key in cls
        ]

    @classmethod
    def values(cls):
        return {
            key.value
            for key in cls
        }