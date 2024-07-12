from typing import no_type_check

from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime


@no_type_check
class utcnow(expression.FunctionElement):
    type = DateTime(timezone=False)
    inherit_cache = True


@no_type_check
@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
