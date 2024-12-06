# coding: utf-8

"""
    WP Engine API

    The API described in this document is subject to change. 

    The version of the OpenAPI document: 1.6.7
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from wp_engine_api.generated.models.installation_account import InstallationAccount
from wp_engine_api.generated.models.installation_site import InstallationSite
from typing import Optional, Set
from typing_extensions import Self

class Installation(BaseModel):
    """
    Installation
    """ # noqa: E501
    id: StrictStr
    name: Annotated[str, Field(strict=True)]
    account: InstallationAccount
    php_version: Optional[StrictStr] = Field(description="The PHP version used to run WordPress (read-only)")
    status: Optional[StrictStr] = None
    site: Optional[InstallationSite] = None
    cname: Optional[StrictStr] = Field(default=None, description="Returns the CNAME of the install")
    stable_ips: Optional[List[StrictStr]] = Field(default=None, description="A list of stable IPs bound to the install. This will only apply to some premium/enterprise plans")
    environment: Optional[StrictStr] = None
    primary_domain: Optional[StrictStr] = Field(default=None, description="The primary domain for the install.")
    is_multisite: Optional[StrictBool] = None
    __properties: ClassVar[List[str]] = ["id", "name", "account", "php_version", "status", "site", "cname", "stable_ips", "environment", "primary_domain", "is_multisite"]

    @field_validator('name')
    def name_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[a-z][a-z0-9]{2,13}$", value):
            raise ValueError(r"must validate the regular expression /^[a-z][a-z0-9]{2,13}$/")
        return value

    @field_validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['active', 'pending']):
            raise ValueError("must be one of enum values ('active', 'pending')")
        return value

    @field_validator('environment')
    def environment_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['production', 'staging', 'development']):
            raise ValueError("must be one of enum values ('production', 'staging', 'development')")
        return value

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of Installation from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of account
        if self.account:
            _dict['account'] = self.account.to_dict()
        # override the default output from pydantic by calling `to_dict()` of site
        if self.site:
            _dict['site'] = self.site.to_dict()
        # set to None if php_version (nullable) is None
        # and model_fields_set contains the field
        if self.php_version is None and "php_version" in self.model_fields_set:
            _dict['php_version'] = None

        # set to None if site (nullable) is None
        # and model_fields_set contains the field
        if self.site is None and "site" in self.model_fields_set:
            _dict['site'] = None

        # set to None if stable_ips (nullable) is None
        # and model_fields_set contains the field
        if self.stable_ips is None and "stable_ips" in self.model_fields_set:
            _dict['stable_ips'] = None

        # set to None if environment (nullable) is None
        # and model_fields_set contains the field
        if self.environment is None and "environment" in self.model_fields_set:
            _dict['environment'] = None

        # set to None if primary_domain (nullable) is None
        # and model_fields_set contains the field
        if self.primary_domain is None and "primary_domain" in self.model_fields_set:
            _dict['primary_domain'] = None

        # set to None if is_multisite (nullable) is None
        # and model_fields_set contains the field
        if self.is_multisite is None and "is_multisite" in self.model_fields_set:
            _dict['is_multisite'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Installation from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "account": InstallationAccount.from_dict(obj["account"]) if obj.get("account") is not None else None,
            "php_version": obj.get("php_version"),
            "status": obj.get("status"),
            "site": InstallationSite.from_dict(obj["site"]) if obj.get("site") is not None else None,
            "cname": obj.get("cname"),
            "stable_ips": obj.get("stable_ips"),
            "environment": obj.get("environment"),
            "primary_domain": obj.get("primary_domain"),
            "is_multisite": obj.get("is_multisite")
        })
        return _obj


