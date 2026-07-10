from fastapi import APIRouter,Depends,HTTPException
from app.core.security import get_current_user, oauth2_scheme
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.note import Note
from app.schemas.note import NoteCreate

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)

@router.get("/")
def get_notes(   token:str=Depends(oauth2_scheme)
):
    user=get_current_user(token)

    return {
        
        "message": "Notes Route Working",
        "user":user
        
    }

@router.post("/")
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = get_current_user(token)

    new_note = Note(
        title=note.title,
        content=note.content,
        owner_id=1
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return {
        "message": "Note created successfully",
        "data": new_note
    }
@router.get("/all")
def get_all_notes(
    page: int=1,
    limit: int=5,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    current_user=get_current_user(token)
    if current_user.role !="admin":
        raise HTTPException(status_code=403,detail="Admin access only")
    skip=(page-1)*limit

    notes = db.query(Note)\
        .offset(skip)\
        .limit(limit)\
        .all()

    return {
        "page":page,
        "limit":limit,
        "data":notes
    }
@router.get("/{note_id}")
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note
@router.put("/{note_id}")
def update_note(
    note_id: int,
    note_data: NoteCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.title = note_data.title
    note.content = note_data.content

    db.commit()

    return {"message": "Note updated successfully"}
@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()

    return {"message": "Note deleted successfully"}
@router.get("/search/{keyword}")
def search_notes(
    keyword: str,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    notes = db.query(Note).filter(
        Note.title.ilike(f"%{keyword}%")
    ).all()

    return notes
@router.get("/filter")
def filter_notes(
    title: str,
    db: Session = Depends(get_db)
):

    notes = db.query(Note).filter(
        Note.title.contains(title)
    ).all()

    return notes