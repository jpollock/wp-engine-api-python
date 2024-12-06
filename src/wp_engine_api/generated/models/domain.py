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

from pydantic import BaseModel, ConfigDict, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from wp_engine_api.generated.models.domain_redirects_to_inner import DomainRedirectsToInner
from typing import Optional, Set
from typing_extensions import Self

class Domain(BaseModel):
    """
    Domain
    """ # noqa: E501
    name: StrictStr
    duplicate: StrictBool
    primary: StrictBool
    id: StrictStr
    redirects_to: Optional[List[DomainRedirectsToInner]] = None
    __properties: ClassVar[List[str]] = ["name", "duplicate", "primary", "id", "redirects_to"]

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
        """Create an instance of Domain from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in redirects_to (list)
        _items = []
        if self.redirects_to:
            for _item_redirects_to in self.redirects_to:
                if _item_redirects_to:
                    _items.append(_item_redirects_to.to_dict())
            _dict['redirects_to'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Domain from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "duplicate": obj.get("duplicate"),
            "primary": obj.get("primary"),
            "id": obj.get("id"),
            "redirects_to": [DomainRedirectsToInner.from_dict(_item) for _item in obj["redirects_to"]] if obj.get("redirects_to") is not None else None
        })
        return _obj


