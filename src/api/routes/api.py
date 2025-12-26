from fastapi import APIRouter

from api.routes import users, category, scope, client, workplace, cat_scope_workplace_rel, law

router = APIRouter()

router.include_router(oauth_routes.router, tags=["Oauth2"], prefix="/oauth2")
router.include_router(users.router, tags=["users"], prefix="/users")
router.include_router(law.router, tags=["law"], prefix="/law")
router.include_router(category.router, tags=["category"], prefix="/category")
router.include_router(scope.router, tags=["scope"], prefix="/scope")
router.include_router(client.router, tags=["client"], prefix="/client")
router.include_router(workplace.router, tags=["workplace"], prefix="/workplace")
router.include_router(
    cat_scope_workplace_rel.router, tags=["cat_scope_workplace_rel"], prefix="/cat_scope_workplace_rel"
)