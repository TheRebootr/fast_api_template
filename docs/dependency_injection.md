# FastAPI Dependency Injection - Quick Reference

## Import Dependencies

```python
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import (
    get_db,
    get_settings,
    CommonQueryParams,
    SearchQueryParams,
)
from app.config import Settings
```

## Common Patterns

### 1. Database Session

```python
@router.get("/endpoint")
async def my_endpoint(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(Model))
    return result.scalars().all()
```

### 2. Pagination

```python
@router.get("/endpoint")
async def my_endpoint(
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination: Annotated[CommonQueryParams, Depends()],
):
    query = select(Model).offset(pagination.skip).limit(pagination.limit)
    result = await db.execute(query)
    return result.scalars().all()
```

**Query params:** `?skip=0&limit=20` (max limit: 100)

### 3. Search & Sort

```python
@router.get("/endpoint")
async def my_endpoint(
    db: Annotated[AsyncSession, Depends(get_db)],
    search: Annotated[SearchQueryParams, Depends()],
):
    query = select(Model)
    if search.q:
        query = query.where(Model.name.ilike(f"%{search.q}%"))
    if search.sort_by:
        sort_col = getattr(Model, search.sort_by)
        query = query.order_by(
            sort_col.desc() if search.order == "desc" else sort_col
        )
    result = await db.execute(query)
    return result.scalars().all()
```

**Query params:** `?q=search&sort_by=name&order=desc`

### 4. Settings

```python
@router.get("/endpoint")
async def my_endpoint(
    settings: Annotated[Settings, Depends(get_settings)],
):
    return {
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT.value,
    }
```

### 5. Multiple Dependencies

```python
@router.get("/endpoint")
async def my_endpoint(
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination: Annotated[CommonQueryParams, Depends()],
    search: Annotated[SearchQueryParams, Depends()],
    settings: Annotated[Settings, Depends(get_settings)],
):
    # All dependencies injected automatically
    ...
```

## Testing Dependencies

```python
from app.main import app
from app.api.dependencies import get_db

# Override dependency
async def mock_get_db():
    # Return mock session
    yield MockSession()

app.dependency_overrides[get_db] = mock_get_db

# Clear after test
app.dependency_overrides.clear()
```

## Router-Level Dependencies

Apply dependency to all endpoints:

```python
router = APIRouter(
    dependencies=[Depends(require_admin)],  # All routes require admin
)
```

## Custom Dependencies

```python
async def get_item_by_id(
    item_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Item:
    result = await db.get(Item, item_id)
    if not result:
        raise HTTPException(404, "Item not found")
    return result

@router.get("/items/{item_id}")
async def endpoint(
    item: Annotated[Item, Depends(get_item_by_id)],  # Pre-fetched
):
    return item
```

## Tips

✅ Always use `Annotated` for type hints
✅ Name parameters descriptively (`pagination`, not `params`)
✅ Document query parameters in docstring
✅ Keep dependencies focused (single responsibility)
✅ Test with dependency overrides

## Resources

- [FastAPI Dependencies Documentation](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [Dependency Injection in FastAPI](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)
- [Advanced Dependencies](https://fastapi.tiangolo.com/advanced/advanced-dependencies/)
