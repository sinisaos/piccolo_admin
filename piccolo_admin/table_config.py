import typing as t
from dataclasses import dataclass

from piccolo.columns.base import Column
from piccolo.columns.column_types import (
    ForeignKey,
    Time,
    Timestamp,
    Timestamptz,
)
from piccolo.table import Table
from piccolo_api.crud.endpoints import OrderBy
from piccolo_api.crud.hooks import Hook
from piccolo_api.crud.validators import Validators
from piccolo_api.media.base import MediaStorage


@dataclass
class TableConfig:
    """
    Gives the user more control over how a ``Table`` appears in the UI.

    :param table_class:
        The :class:`Table <piccolo.table.Table>` class to configure.
    :param visible_columns:
        If specified, only these columns will be shown in the list view of the
        UI. This is useful when you have a lot of columns.
    :param exclude_visible_columns:
        You can specify this instead of ``visible_columns``, in which case all
        of the ``Table`` columns except the ones specified will be shown in the
        list view.
    :param visible_filters:
        If specified, only these columns will be shown in the filter sidebar
        of the UI. This is useful when you have a lot of columns.
    :param exclude_visible_filters:
        You can specify this instead of ``visible_filters``, in which case all
        of the ``Table`` columns except the ones specified will be shown in the
        filter sidebar.
    :param rich_text_columns:
        You can specify ``rich_text_columns`` if you want a WYSIWYG editor
        on certain Piccolo :class:`Text <piccolo.columns.column_types.Text>`
        columns. Any columns not specified will use a standard HTML textarea
        tag in the UI.
    :param hooks:
        These are passed directly to
        :class:`PiccoloCRUD <piccolo_api.crud.endpoints.PiccoloCRUD>`, which
        powers Piccolo Admin under the hood. It allows you to run custom logic
        when a row is modified.
    :param media_storage:
        These columns will be used to store media. We don't directly store the
        media in the database, but instead store a string, which is a unique
        identifier, and can be used to retrieve a URL for accessing the file.
        Piccolo Admin automatically renders a file upload widget for each media
        column in the UI.
    :param validators:
        The :class:`Validators <piccolo_api.crud.endpoints.Validators>` are
        passed directly to
        :class:`PiccoloCRUD <piccolo_api.crud.endpoints.PiccoloCRUD>`, which
        powers Piccolo Admin under the hood. It allows fine grained access
        control over each API endpoint. For example, limiting which users can
        ``POST`` data::

            from piccolo_api.crud.endpoints import PiccoloCRUD
            from starlette.exceptions import HTTPException
            from starlette.requests import Request


            async def manager_only(
                piccolo_crud: PiccoloCRUD,
                request: Request
            ):
                # The Piccolo `BaseUser` can be accessed from the request.
                user = request.user.user

                # Assuming we have another database table where we record
                # users with certain permissions.
                manager = await Manager.exists().where(manager.user == user)

                if not manager:
                    # Raise a Starlette exception if we want to reject the
                    # request.
                    raise HTTPException(
                        status_code=403,
                        detail="Only managers are allowed to do this"
                    )

            admin = create_admin(
                tables=TableConfig(
                    Movie,
                    validators=Validators(post_single=[manager_only])
                )
            )
    :param menu_group:
        If specified, tables can be divided into groups in the table
        menu. This is useful when you have many tables that you
        can organize into groups for better visibility.
    :param link_column:
        In the list view of Piccolo Admin, we use the primary key to link to
        the edit page. However, if the primary key column is hidden, due to
        ``visible_columns`` or ``exclude_visible_columns``, then we need to
        specify an alternative column to use as the link.
    :param order_by:
        If specified, the rows are sorted by ``order_by``, otherwise
        the default ``primary_key`` column is used to sort the rows.
    :param time_resolution:
        Controls the resolution of ``Time`` columns, and the time component
        of ``Timestamp`` / ``Timestamptz`` columns. The units are given in
        seconds. Some examples:

        * 0.001 - the max resolution is 1 millisecond (this is the minimum
          currently allowed by HTML input fields)
        * 1 - the max resolution is 1 second (the default)
        * 60 - the max resolution is 1 minute

    """

    table_class: t.Type[Table]
    visible_columns: t.Optional[t.List[Column]] = None
    exclude_visible_columns: t.Optional[t.List[Column]] = None
    visible_filters: t.Optional[t.List[Column]] = None
    exclude_visible_filters: t.Optional[t.List[Column]] = None
    rich_text_columns: t.Optional[t.List[Column]] = None
    hooks: t.Optional[t.List[Hook]] = None
    media_storage: t.Optional[t.Sequence[MediaStorage]] = None
    validators: t.Optional[Validators] = None
    menu_group: t.Optional[str] = None
    link_column: t.Optional[Column] = None
    order_by: t.Optional[t.List[OrderBy]] = None
    time_resolution: t.Optional[
        t.Dict[t.Union[Timestamp, Timestamptz, Time], t.Union[float, int]]
    ] = None

    def __post_init__(self):
        if self.visible_columns and self.exclude_visible_columns:
            raise ValueError(
                "Only specify `visible_columns` or "
                "`exclude_visible_columns`."
            )

        if self.visible_filters and self.exclude_visible_filters:
            raise ValueError(
                "Only specify `visible_filters` or `exclude_visible_filters`."
            )

        if isinstance(self.link_column, ForeignKey):
            raise ValueError(
                "Don't use a foreign key column for `link_column`, as they "
                "are already displayed as a link in the UI."
            )

        # Create a mapping for faster lookups
        self.media_columns = (
            {i.column: i for i in self.media_storage}
            if self.media_storage
            else None
        )

    def _get_columns(
        self,
        include_columns: t.Optional[t.List[Column]],
        exclude_columns: t.Optional[t.List[Column]],
        all_columns: t.List[Column],
    ) -> t.List[Column]:
        if include_columns and not exclude_columns:
            return include_columns

        if exclude_columns and not include_columns:
            column_names = [i._meta.name for i in exclude_columns]
            return [i for i in all_columns if i._meta.name not in column_names]

        return all_columns

    def get_visible_columns(self) -> t.List[Column]:
        return self._get_columns(
            include_columns=self.visible_columns,
            exclude_columns=self.exclude_visible_columns,
            all_columns=self.table_class._meta.columns,
        )

    def get_visible_column_names(self) -> t.Tuple[str, ...]:
        return tuple(i._meta.name for i in self.get_visible_columns())

    def get_visible_filters(self) -> t.List[Column]:
        return self._get_columns(
            include_columns=self.visible_filters,
            exclude_columns=self.exclude_visible_filters,
            all_columns=self.table_class._meta.columns,
        )

    def get_visible_filter_names(self) -> t.Tuple[str, ...]:
        return tuple(i._meta.name for i in self.get_visible_filters())

    def get_rich_text_columns_names(self) -> t.Tuple[str, ...]:
        return (
            tuple(i._meta.name for i in self.rich_text_columns)
            if self.rich_text_columns
            else ()
        )

    def get_media_columns_names(self) -> t.Tuple[str, ...]:
        return (
            tuple(i._meta.name for i in self.media_columns)
            if self.media_columns
            else ()
        )

    def get_link_column(self) -> Column:
        return self.link_column or self.table_class._meta.primary_key

    def get_order_by(self) -> t.List[OrderBy]:
        return self.order_by or [
            OrderBy(column=self.table_class._meta.primary_key, ascending=True)
        ]

    def get_time_resolution(self) -> t.Dict[str, t.Union[int, float]]:
        return (
            {
                column._meta.name: resolution
                for column, resolution in self.time_resolution.items()
            }
            if self.time_resolution
            else {}
        )
