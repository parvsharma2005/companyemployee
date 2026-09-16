from .models import AuditLog


def create_audit_log(
    user,
    action,
    module,
    object_id=None,
    description="",
    old_data=None,
    new_data=None,
    ip_address=None,
):
    return AuditLog.objects.create(
        user=user,
        action=action,
        module=module,
        object_id=str(object_id) if object_id else None,
        description=description,
        old_data=old_data,
        new_data=new_data,
        ip_address=ip_address,
    )
    