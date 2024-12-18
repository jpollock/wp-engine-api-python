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

from pydantic import BaseModel, ConfigDict, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from wp_engine_api.generated.models.installation_account import InstallationAccount
from wp_engine_api.generated.models.site_installs_inner import SiteInstallsInner
from typing import Optional, Set
from typing_extensions import Self

class Site(BaseModel):
    """
    Site
    """ # noqa: E501
    id: StrictStr
    name: StrictStr
    account: InstallationAccount
    group_name: Optional[StrictStr] = None
    tags: Optional[List[StrictStr]] = None
    installs: Optional[List[SiteInstallsInner]] = None
    __properties: ClassVar[List[str]] = ["id", "name", "account", "group_name", "tags", "installs"]

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
        """Create an instance of Site from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in installs (list)
        _items = []
        if self.installs:
            for _item_installs in self.installs:
                if _item_installs:
                    _items.append(_item_installs.to_dict())
            _dict['installs'] = _items
        # set to None if group_name (nullable) is None
        # and model_fields_set contains the field
        if self.group_name is None and "group_name" in self.model_fields_set:
            _dict['group_name'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Site from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "account": InstallationAccount.from_dict(obj["account"]) if obj.get("account") is not None else None,
            "group_name": obj.get("group_name"),
            "tags": obj.get("tags"),
            "installs": [SiteInstallsInner.from_dict(_item) for _item in obj["installs"]] if obj.get("installs") is not None else None
        })
        return _obj


