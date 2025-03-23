from apps.customer.models import Customer
from apps.driver.models import Driver
from apps.user.models import ContactPointAddress, User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_null=True, allow_blank=True, required=True)
    first_name = serializers.CharField(
        allow_blank=False, allow_null=False, required=True
    )
    last_name = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    password = serializers.CharField(write_only=True, min_length=6)
    meta = serializers.DictField(write_only=True, required=False)
    user_role = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = [
            "mobile_number",
            "email",
            "first_name",
            "last_name",
            "meta",
            "profile_picture",
            "password",
            "user_role",
            "blood_group",
        ]

    def validate_mobile_number(self, mobile_number):
        existing_user = User.objects.filter(mobile_number=mobile_number).first()
        if existing_user:
            raise serializers.ValidationError(
                f"This mobile number is already in use for {existing_user.role_label()}. "
            )
        return mobile_number.strip()

    def validate_email(self, email):
        if not email:
            return email
        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            raise serializers.ValidationError(
                f"This email is already in used for {existing_user.role_label()}. "
            )
        return email.strip()

    def validate_first_name(self, first_name):
        MINIMUM_FIRST_NAME_LENGTH = 3
        if len(first_name) < MINIMUM_FIRST_NAME_LENGTH:
            raise serializers.ValidationError(
                f"First Name must have minimum of {MINIMUM_FIRST_NAME_LENGTH} characters."
            )
        return first_name.strip()

    def validate_user_role(self, user_role):
        valid_roles = [User.DRIVER, User.CUSTOMER]
        if user_role not in valid_roles:
            raise serializers.ValidationError(
                f"Invalid user role. Allowed values: {valid_roles}"
            )
        return user_role

    def create(self, validated_data):
        mobile_number = validated_data.get("mobile_number")
        validated_data["username"] = mobile_number
        validated_data["password"] = make_password(validated_data["password"])
        user = User.objects.create(**validated_data)

        if user.user_role == User.DRIVER:
            Driver.objects.create(user=user)
        elif user.user_role == User.CUSTOMER:
            Customer.objects.create(user=user)

        return user

    def update(self, instance, validated_data):
        raise NotImplementedError()


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        user = authenticate(self.context["request"], **data)
        if not user:
            raise serializers.ValidationError("Incorrect username or password.")
        data["user"] = user
        return data


class UserProfileResponseSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)
    driver = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "mobile_number",
            "email",
            "profile_picture",
            "blood_group",
            "last_login",
            "role",
            "driver",
            "customer",
        ]

    def get_driver(self, instance):
        from apps.driver.models import Driver

        driver = Driver.objects.filter(user=instance).first()
        if not driver:
            return None
        return {
            "id": instance.driver.id,
        }

    def get_customer(self, instance):
        if not hasattr(instance, "customer"):
            return None
        customer = instance.customer
        return {
            "id": customer.id,
        }

    def validate_blood_group(self, value):
        if value not in dict(User.BLOOD_GROUP_CHOICES).keys():
            raise ValidationError("Invalid blood group value.")
        return value


class ContactAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPointAddress
        fields = [
            "contact_number",
            "contact_number_secondary",
            "contact_email",
            "label",
            "contact_person",
            "address",
            "street",
            "city",
            "state",
            "zipcode",
            "building_number",
            "zone",
            "landmark",
            "location",
        ]
