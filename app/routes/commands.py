from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.session import get_db
from schemas.commands import Command as CommandBase, CommandCreate, CommandUpdate, CommandResponse as Response, getResponse
from model.commands import Command as DBCommand
from datetime import datetime, timezone

router = APIRouter()

@router.post("/commands", response_model=Response, status_code=201)
def create_command(command: CommandCreate, db: Session = Depends(get_db)):
    try:
        if not command.name or command.price is None or command.stock_quantity is None:
            return JSONResponse(status_code=400, content={"message": "Name, price, and stock quantity are required."})
        existing_command = db.query(DBCommand).filter(DBCommand.name == command.name).first()
        if existing_command:
            return JSONResponse(status_code=400, content={"message": "Command with this name already exists."})
        # Add a timestamp for creation as ISO string
        now_iso = datetime.now(timezone.utc).isoformat()
        command.created_at = now_iso
        command.updated_at = now_iso
        new_command = DBCommand(**command.model_dump())
        db.add(new_command)
        db.commit()
        db.refresh(new_command)
        return {
            "message": "Command created successfully.",
            "command": CommandBase.model_validate(new_command)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
       
@router.get("/commands/{command_id}", response_model=Response, status_code=200)
def get_command(command_id: int, db: Session = Depends(get_db)):
    command = db.query(DBCommand).filter(DBCommand.id == command_id).first()
    if not command:
        raise HTTPException(status_code=404, detail="Command not found")
    return {
        "message": "Command retrieved successfully.",
        "command": CommandBase.model_validate(command)
    }

@router.get("/commands", response_model=getResponse, status_code=200)
def get_commands(db: Session = Depends(get_db)):
    commands = db.query(DBCommand).all()
    print(f"Retrieved {len(commands)} commands from the database.")
    return {
        "message": "All commands retrieved successfully.",
        "command": [CommandBase.model_validate(command) for command in commands]
    }

    
@router.put("/commands/{command_id}", response_model=Response, status_code=200)
def update_command(command_id: int, command: CommandUpdate, db: Session = Depends(get_db)):
    command_in_db = db.query(DBCommand).filter(DBCommand.id == command_id).first()
    if not command_in_db:
        raise HTTPException(status_code=404, detail="Command not found")
    update_data = command.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(command_in_db, key, value)
    db.commit()
    db.refresh(command_in_db)
    return {
        "message": "Command updated successfully.",
        "command": CommandBase.model_validate(command_in_db)
    }

@router.delete("/commands/{command_id}", response_model=Response, status_code=200)
def delete_command(command_id: int, db: Session = Depends(get_db)):
    command = db.query(DBCommand).filter(DBCommand.id == command_id).first()
    if not command:
        raise HTTPException(status_code=404, detail="Command not found")
    db.delete(command)
    db.commit()
    return {
        "message": "Command deleted successfully.",
        "command": CommandBase.model_validate(command)
    }