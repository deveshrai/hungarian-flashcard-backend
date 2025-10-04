from fastapi import APIRouter

router = APIRouter()

@router.get("/admin")
def admin_home():
    return {"message": "Admin dashboard coming soon"}
