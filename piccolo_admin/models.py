import io
import typing as t
from dataclasses import dataclass

from pydantic import BaseModel, Field
from typing_extensions import TypeAlias


class UserResponseModel(BaseModel):
    username: str
    user_id: str


class MetaResponseModel(BaseModel):
    piccolo_admin_version: str
    site_name: str


class StoreFileResponseModel(BaseModel):
    file_key: str = Field(description="For example `my_file-some-uuid.jpeg`.")


class GenerateFileURLRequestModel(BaseModel):
    column_name: str
    table_name: str
    file_key: str = Field(description="For example `my_file-some-uuid.jpeg`.")


class GenerateFileURLResponseModel(BaseModel):
    file_url: str = Field(description="A URL which the file is accessible on.")


class GroupItem(BaseModel):
    name: str
    slug: str


class GroupedTableNamesResponseModel(BaseModel):
    grouped: t.Dict[str, t.List[str]] = Field(default_factory=dict)
    ungrouped: t.List[str] = Field(default_factory=list)


class FormConfigResponseModel(BaseModel):
    name: str
    slug: str
    description: t.Optional[str] = None


class GroupedFormsResponseModel(BaseModel):
    grouped: t.Dict[str, t.List[FormConfigResponseModel]] = Field(
        default_factory=dict
    )
    ungrouped: t.List[FormConfigResponseModel] = Field(default_factory=list)


@dataclass
class FileResponse:
    contents: t.Union[io.StringIO, io.BytesIO]
    file_name: str
    media_type: str


PydanticModel = t.TypeVar("PydanticModel", bound=BaseModel)
FormResponse: TypeAlias = t.Union[str, FileResponse, None]
