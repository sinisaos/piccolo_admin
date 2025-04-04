import typing as t
from dataclasses import dataclass

from starlette.requests import Request

from .models import FormResponse, PydanticModel


@dataclass
class FormConfig:
    """
    Used to specify forms, which are passed into ``create_admin``.

    :param name:
        This will be displayed in the UI in the sidebar.
    :param pydantic_model:
        This determines which fields to display in the form, and is used to
        deserialise the responses.
    :param endpoint:
        Your custom handler, which accepts two arguments - the FastAPI /
        Starlette request object, in case you want to access the cookies /
        headers / logged in user (via `request.user`). And secondly an instance
        of the Pydantic model. If it returns a string, it will be shown to
        the user in the UI as the success message. For example ``'Successfully
        sent email'``. The endpoint can be a normal function or async function.
    :param description:
        An optional description which is shown in the UI to explain to the user
        what the form is for.
    :param form_group:
        If specified, forms can be divided into groups in the form
        menu. This is useful when you have many forms that you
        can organize into groups for better visibility.

    Here's a full example:

    .. code-block:: python

        class MyModel(pydantic.BaseModel):
            message: str = "hello world"


        def my_endpoint(request: Request, data: MyModel):
            print(f"I received {data.message}")

            # If we're not happy with the data raise a ValueError
            # The message inside the exception will be displayed in the UI.
            raise ValueError("We were unable to process the form.")

            # If we're happy with the data, just return a string, which
            # will be displayed in the UI.
            return "Successful."


        config = FormConfig(
            name="My Form",
            pydantic_model=MyModel,
            endpoint=my_endpoint,
            form_group="Text forms",
        )

    """

    def __init__(
        self,
        name: str,
        pydantic_model: t.Type[PydanticModel],
        endpoint: t.Callable[
            [Request, PydanticModel],
            t.Union[FormResponse, t.Coroutine[None, None, FormResponse]],
        ],
        description: t.Optional[str] = None,
        form_group: t.Optional[str] = None,
    ):
        self.name = name
        self.pydantic_model = pydantic_model
        self.endpoint = endpoint
        self.description = description
        self.form_group = form_group
        self.slug = self.name.replace(" ", "-").lower()
