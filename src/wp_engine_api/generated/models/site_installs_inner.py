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
from typing import Optional, Set
from typing_extensions import Self

class SiteInstallsInner(BaseModel):
    """
    SiteInstallsInner
    """ # noqa: E501
    id: Optional[StrictStr] = None
    name: Optional[StrictStr] = None
    environment: Optional[StrictStr] = None
    cname: Optional[StrictStr] = Field(default=None, description="Returns the CNAME of the install")
    php_version: Optional[StrictStr] = Field(default=None, description="The PHP version used to run WordPress")
    is_multisite: Optional[StrictBool] = None
    __properties: ClassVar[List[str]] = ["id", "name", "environment", "cname", "php_version", "is_multisite"]

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
        """Create an instance of SiteInstallsInner from a JSON string"""
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
        # set to None if environment (nullable) is None
        # and model_fields_set contains the field
        if self.environment is None and "environment" in self.model_fields_set:
            _dict['environment'] = None

        # set to None if php_version (nullable) is None
        # and model_fields_set contains the field
        if self.php_version is None and "php_version" in self.model_fields_set:
            _dict['php_version'] = None

        # set to None if is_multisite (nullable) is None
        # and model_fields_set contains the field
        if self.is_multisite is None and "is_multisite" in self.model_fields_set:
            _dict['is_multisite'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SiteInstallsInner from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "environment": obj.get("environment"),
            "cname": obj.get("cname"),
            "php_version": obj.get("php_version"),
            "is_multisite": obj.get("is_multisite")
        })
        return _obj

