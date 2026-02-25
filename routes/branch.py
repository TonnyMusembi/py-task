from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

# from app.database import get_db
from src.database import get_db
# from  models import Branch, Company
# from models import Branch, Company

from  schemas import BranchCreate, BranchUpdate, BranchOut
from  core.security import get_current_user

router = APIRouter(prefix="/branches", tags=["Branches"])


# ── Create ────────────────────────────────────────────────────────────────────
@router.post("/", response_model=BranchOut, status_code=status.HTTP_201_CREATED)
def create_branch(
    payload:      BranchCreate,
    db:           Session = Depends(get_db),
    current_user  = Depends(get_current_user),
):
    # 1. Verify company exists
    company = db.query(Company).filter(Company.id == payload.company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id {payload.company_id} not found"
        )

    # 2. Check company is active
    if company.status != 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create a branch under an inactive company"
        )

    # 3. Build branch object
    branch = Branch(
        **payload.model_dump(),
        lower_name = payload.name.lower(),
        created_by = current_user.id,
    )

    # 4. Save — catch unique constraint violations
    try:
        db.add(branch)
        db.commit()
        db.refresh(branch)
    except IntegrityError as e:
        db.rollback()
        error = str(e.orig).lower()

        if "uq_branch_name" in error or "name" in error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Branch name '{payload.name}' already exists"
            )
        if "uq_branch_code" in error or "branch_code" in error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Branch code '{payload.branch_code}' already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A branch with these details already exists"
        )

    return branch


# ── Read all ──────────────────────────────────────────────────────────────────
@router.get("/", response_model=List[BranchOut])
def list_branches(
    company_id: int  = None,       # optional filter by company
    status:     int  = None,       # optional filter by status
    skip:       int  = 0,
    limit:      int  = 100,
    db:         Session = Depends(get_db),
    _           = Depends(get_current_user),
):
    query = db.query(Branch)

    if company_id is not None:
        query = query.filter(Branch.company_id == company_id)
    if status is not None:
        query = query.filter(Branch.status == status)

    return query.offset(skip).limit(limit).all()


# ── Read one ──────────────────────────────────────────────────────────────────
@router.get("/{branch_id}", response_model=BranchOut)
def get_branch(
    branch_id: int,
    db:        Session = Depends(get_db),
    _          = Depends(get_current_user),
):
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Branch {branch_id} not found"
        )
    return branch


# ── Update ────────────────────────────────────────────────────────────────────
@router.patch("/{branch_id}", response_model=BranchOut)
def update_branch(
    branch_id:    int,
    payload:      BranchUpdate,
    db:           Session = Depends(get_db),
    current_user  = Depends(get_current_user),
):
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Branch {branch_id} not found"
        )

    # Only update fields that were actually sent
    updates = payload.model_dump(exclude_unset=True)

    # Keep lower_name in sync if name changes
    if "name" in updates:
        updates["lower_name"] = updates["name"].lower()

    updates["updated_by"] = current_user.id

    for field, value in updates.items():
        setattr(branch, field, value)

    try:
        db.commit()
        db.refresh(branch)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Name or branch code already in use"
        )

    return branch


# ── Delete (soft) ─────────────────────────────────────────────────────────────
@router.delete("/{branch_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_branch(
    branch_id:   int,
    db:          Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Branch {branch_id} not found"
        )

    # Soft delete — set status to 0 instead of dropping the row
    branch.status     = 0
    branch.updated_by = current_user.id
    db.commit()
