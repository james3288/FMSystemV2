from rest_framework import serializers
from datetime import datetime

class CustomDateField(serializers.ReadOnlyField):
    def to_representation(self, value):
        # Convert datetime to date and handle timezone explicitly
        if value is not None and isinstance(value, datetime):
            return value.date()
        return None

class ItemSerializer(serializers.Serializer):
    
    item_code_id = serializers.IntegerField()
    item_code = serializers.CharField()
    cat_type_id = serializers.IntegerField()
    category = serializers.CharField()
    item_name = serializers.CharField()
    item_name_desc_id = serializers.IntegerField()
    type_maint = serializers.CharField()
    brand = serializers.CharField()
    rs_no = serializers.CharField()
    qty_unit = serializers.CharField()
    date_borrowed = CustomDateField()
    bs_id = serializers.IntegerField()
    bs_no = serializers.CharField()
    custodian_id = serializers.IntegerField()
    custodian_name = serializers.CharField()
    borrowed_to = serializers.CharField()
    borrowed_for = serializers.CharField()
    location = serializers.CharField()
    status_item = serializers.CharField()
    status_served_name = serializers.CharField()
    cat_sub_main = serializers.CharField()
    date_schedule = CustomDateField()
    sm_id = serializers.IntegerField()
    fac_maint_id = serializers.IntegerField()
    ussm_id = serializers.IntegerField()
    date_schedule_final = serializers.CharField()
    last_date_maint = CustomDateField()
    performed_by = serializers.CharField()
    verified_by = serializers.CharField()
    repair_status = serializers.CharField()
    sys_specs_id = serializers.IntegerField()
    acquisition_date = CustomDateField()
    serial_no = serializers.CharField()