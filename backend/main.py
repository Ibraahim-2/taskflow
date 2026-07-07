from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],   # izinkan frontend kita
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def baca_akar():
    return {"Pesan": "Tasflow API hidup!"}

# Buat semua tabel di database saat server start (kalau belumm ada)
models.Base.metadata.create_all(bind=engine)

# Penyesia session database unutk setiap request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Cetakan data (Pydantic Model) - Validasi data
class TugasMasuk(BaseModel):
    judul: str
    selesai: bool = False

# READ - ambil semua tugas dari DB
@app.get("/tasks")
def ambil_semua_tugas(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

# CREATE - simpan tugas baru ke DB
@app.post("/tasks", status_code=201)
def buat_tugas(tugas: TugasMasuk, db: Session = Depends(get_db)):
    tugas_baru = models.Task(judul=tugas.judul, selesai=tugas.selesai)
    db.add(tugas_baru)
    db.commit()
    db.refresh(tugas_baru)
    return tugas_baru

# DELETE - hapus tugas
@app.delete("/tasks/{task_id}")
def hapus_tugas(task_id: int, db: Session = Depends(get_db)):
    tugas = db.query(models.Task).filter(models.Task.id == task_id).first()
    if tugas is None:
        raise HTTPException(status_code=404, detail="Tugas tidak ditemukan")
    db.delete(tugas)
    db.commit()
    return {"detail": f"Tugsa dengan id {task_id} berhasil dihapus"}