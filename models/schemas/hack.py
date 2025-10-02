from pydantic import BaseModel, Field, field_serializer, model_serializer
from models.schemas.pagination import PaginationRequest, PaginationResponse
from typing import List, Optional, Any
from datetime import datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class TestRequest(BaseModel):
    test: str

class ProtectedResponse(BaseModel):
    message: str
    your_data: dict

class GeoData(BaseModel):
    accuracy: Optional[float] = Field(None, description="Погрешность в метрах")
    longitude: Optional[float] = Field(None, description="Долгота")
    latitude: Optional[float] = Field(None, description="Широта")
    

class CoordinatePoint(BaseModel):
    latitude: float = Field(None, description="Широта")
    longitude: float = Field(None, description="Долгота")

class SiteJobBase(BaseModel):
    seq: int
    id: int
    name: Optional[str] = Field(None, description="Название работы")
    description: Optional[str] = Field(None, description="Описание этапа")
    start_date: Optional[datetime] = Field(None, description="Дата начала")
    end_date: Optional[datetime] = Field(None, description="Дата конца")
    volume: Optional[float] = Field(None, description="Объем работ")
    measurement: Optional[str] = Field(None, description="Единица измерения объема")
    status: Optional[int] = Field(None, description="Состояние: 0 - не окончен, 1 - окончен не валидирован, 2 - окончен валидирован, 3 - окончен отклонен")

class SiteJobResponse(SiteJobBase):
    """Схема для ответа с информацией о работе"""
    pass

class ActiveJobBase(SiteJobBase):
    stage_seq: int
    stage_id: int

class ActiveJobResponce(ActiveJobBase):
    """Схема для ответа с информацией о текущей работе и ее фазе"""
    pass


class BuildsiteBase(BaseModel):
    id: int
    state: int = Field(..., description="-1 - stopped, 0 - planning, 1 - started")
    sitename: Optional[str] = None
    start_date: Optional[datetime] = None
    state_changed: Optional[datetime] = None
    manager: Optional[int] = None
    manager_name: Optional[str] = None
    foreman: Optional[int] = None
    foreman_name: Optional[str] = None
    acceptor: Optional[int] = None
    jobshift_present: Optional[bool] = None
    notes_count: Optional[int] = None
    warns_count: Optional[int] = None
    active_jobs: List[ActiveJobResponce] = None
    coordinates: Optional[List[List[List[CoordinatePoint]]]] = Field(None, description="Список полигонов, каждый полигон - список точек")
    geo_data: Optional[GeoData] = Field(None, description="Основная точка объекта")

    class Config:
        from_attributes = True
        json_encoders = {
            #кастомные энкодеры если нужно для координат
        }

class BuildsiteResponse(BuildsiteBase):
    pass

class BuildsiteListResponse(PaginationResponse[BuildsiteResponse]):
    pass

class BuildsitePaginationRequest(PaginationRequest):
    state_filter: Optional[int] = Field(None, description="Фильтр по состоянию: -1, 0, 1")
    search_text: Optional[str] = Field(None, description="Поиск по названию объекта")

class CommentCreationRequest(BaseModel):
    user_id: int
    site_id: int
    comment: str
    fix_time: Optional[datetime] = None
    docs: str
    file_ids: Optional[List[int]] = None
    geo: GeoData
    stop_type: int
    comm_type: int
    witness: str
    job_id: Optional[int] = None

class CommentCreationResponce(BaseModel):
    is_done: bool
    error_text: Optional[str]

class UserBase(BaseModel):
    id: int
    username: str
    name: Optional[str] = None
    surname: Optional[str] = None
    patronym: Optional[str] = None
    role: Optional[int] = Field(None, description="0 - owner/contractor, 1 - foreman, 2 - inspector")

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    pass

class FilesBase(BaseModel):
    id: int
    created_at: datetime
    file_key: Optional[str] = None
    filename: Optional[str] = None
    mime_type: Optional[str] = None
    size: Optional[str] = None
    checksum256: Optional[str] = None
    uploader: Optional[int] = None

    class Config:
        from_attributes = True

class FilesResponse(FilesBase):
    """Схема для ответа с информацией о файле"""
    pass

class Job2StageBase(BaseModel):
    stageid: int
    jobid: int
    seq: int

    class Config:
        from_attributes = True

class Job2StageResponse(Job2StageBase):
    """Схема для ответа с информацией о связи работы и этапа"""
    pass

class SiteStageBase(BaseModel):
    id: int
    site: Optional[int] = Field(None, description="ID строительной площадки (Buildsite)")
    seq: Optional[int] = Field(None, description="Порядковый номер этапа")
    name: Optional[str] = Field(None, description="Название этапа")
    done: Optional[bool] = Field(None, description="Завершен ли этап")
    job2stage: List[SiteJobResponse] = Field([], description="Список работ")

class SiteStageResponse(SiteStageBase):
    """Схема для ответа с информацией об этапе"""
    pass

class JobShiftBase(BaseModel):
    id: int
    creator_name: Optional[str] = Field(None, description="Имя создателя")
    comment: Optional[str] = Field(None, description="Комментарий")
    created_at: Optional[datetime] = Field(None, description="Дата создания")
    old_start_date: Optional[datetime] = Field(None, description="старая дата начала")
    new_start_date: Optional[datetime] = Field(None, description="новая дата начала")
    old_end_date: Optional[datetime] = Field(None, description="старая дата конца")
    new_end_date: Optional[datetime] = Field(None, description="новая дата конца")
    
class JobShiftResponse(JobShiftBase):
    """Схема для ответа с информацией о предложении изменить график"""
    pass

class CommentFileResponse(BaseModel):
    file: FilesResponse
    description: Optional[int] = None

    class Config:
        from_attributes = True


class CommentResponse(BaseModel):
    id: int
    author: Optional[UserResponse] = None
    created_at: Optional[datetime] = None
    state: Optional[int] = None
    comment: Optional[str] = None
    fix_time: Optional[int] = Field(None, description="days")
    docs: Optional[str] = None
    geo: Optional[GeoData] = None
    type: Optional[int] = None
    rec_type: Optional[int] = Field(None, description="0 - notice, 1 - warning")
    linked_job: Optional[int] = None
    comment2file: List[FilesResponse] = []

    class Config:
        from_attributes = True

class ChecklistAnsResponse(BaseModel):
    id: int
    author: Optional[UserResponse] = None
    answers: Optional[dict] = None
    regtime: Optional[datetime] = None
    geo: Optional[GeoData] = None

    class Config:
        from_attributes = True


class BuildsiteDocumentResponse(BaseModel):
    file: FilesResponse
    type: Optional[int] = None

    class Config:
        from_attributes = True


class BuildsiteExtendedResponse(BuildsiteBase):
    users: List[UserResponse] = []
    jobshifts: List[JobShiftResponse] = []
    checklist_ans: List[ChecklistAnsResponse] = []
    sitestage: List[SiteStageResponse] = []
    buildsite2doc: List[BuildsiteDocumentResponse] = []
    comments: List[CommentResponse] = []

class OcrRequest(BaseModel):
    bucket: str = Field(None, description="bucket name")
    file: str = Field(None, description="filename in bucket")

class OcrResponse(BaseModel):
    model: Optional[str] = Field()
    created_at: Optional[str] = Field()
    response: Optional[str] = Field()
