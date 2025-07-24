# Datei: backend/app/crud/__init__.py

# Importiere die einzelnen CRUD-Controller-Instanzen aus ihren jeweiligen Dateien.
# Dadurch können wir in der API einfach 'crud.asset.create' usw. aufrufen.

from .asset import asset
from .asset_log import asset_log
from .asset_type import asset_type
from .location import location
from .manufacturer import manufacturer
from .status import status
from .supplier import supplier
from .user import user