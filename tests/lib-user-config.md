# User config

    >>> from gage._internal.user_config import *
    >>> from gage._internal.types import *

User config is non-project configuration provide by the user.

User config can be defined in one of two locations:

- With a project
- System wide (user directory)

User config defined for a project extends system wide user config.

    >>> from gage._internal.user_config import *

Create sample project config.

    >>> project_dir = make_temp_dir()
    >>> cd(project_dir)

    >>> write("gageconfig.toml", """
    ... [repos.git]
    ... type = "git"
    ... url = "git@github.com:gar1t/gage-runs.git"
    ...
    ... [repos.backup]
    ... path = "~/Backups/gage-runs"
    ... """)

Load the config.

    >>> config = user_config_for_dir(".")

    >>> config.as_json()  # +json +diff
    {
      "repos": {
        "backup": {
          "path": "~/Backups/gage-runs"
        },
        "git": {
          "type": "git",
          "url": "git@github.com:gar1t/gage-runs.git"
        }
      }
    }

    >>> validate_user_config_data(config.as_json())

`get_repositories()` returns a dict of repositories keyed by name.

    >>> repos = config.get_repositories()

    >>> sorted(repos)
    ['backup', 'git']

    >>> git_repo = repos["git"]
    >>> git_repo.as_json()  # +json +diff
    {
      "type": "git",
      "url": "git@github.com:gar1t/gage-runs.git"
    }

    >>> backup_repo = repos["backup"]
    >>> backup_repo.as_json()  # +json +diff
    {
      "path": "~/Backups/gage-runs"
    }


Each repository has a type.

    >>> git_repo.get_type()
    'git'

The default type is 'local'.

    >>> backup_repo.get_type()
    'local'

`attrs()` returns repository attributes.

    >>> git_repo.attrs()
    {'url': 'git@github.com:gar1t/gage-runs.git'}

    >>> backup_repo.attrs()
    {'path': '~/Backups/gage-runs'}

## Validation

    >>> from gage._internal.schema_util import validation_errors

    >>> def validate(data):
    ...     try:
    ...         validate_user_config_data(data)
    ...     except UserConfigValidationError as e:
    ...         json_pprint(validation_errors(e))

Empty config.

    >>> validate({})

    >>> validate({"repos": {}})

Unknown top-level attributes.

    >>> validate({"unknown": {}})
    [
      [
        "unknown"
      ]
    ]

Invalid repository type.

    >>> validate({"repos": 123})
    [
      "Properties ['repos'] are invalid",
      "The instance must be of type \"object\""
    ]

Invalid repo type.

    >>> validate({"repos": {"test": 123}})  # +wildcard
    [
      "Properties ['repos'] are invalid",
      "Properties ['test'] are invalid",
      "The instance must be of type \"object\"",
      ...
    ]

Missing required type or path.

    >>> validate({"repos": {"test": {}}})  # +wildcard
    [
      "Properties ['repos'] are invalid",
      "Properties ['test'] are invalid",
      ...
      "The object is missing required properties ['type']",
      "The object is missing required properties ['path']"
    ]

    >>> validate({"repos": {"test": {"foo": 123}}})  # +wildcard
    [
      "Properties ['repos'] are invalid",
      "Properties ['test'] are invalid",
      ...
      "The object is missing required properties ['type']",
      "The object is missing required properties ['path']"
    ]

Invalid type attribute.

    >>> validate({"repos": {"test": {"type": 123}}})
    [
      "Properties ['repos'] are invalid",
      "Properties ['test'] are invalid",
      "Properties ['type'] are invalid",
      "The instance must be of type \"string\""
    ]

Invalid path attribute.

    >>> validate({"repos": {"test": {"path": 123}}})
    [
      "Properties ['repos'] are invalid",
      "Properties ['test'] are invalid",
      "Properties ['path'] are invalid",
      "The instance must be of type \"string\""
    ]
    