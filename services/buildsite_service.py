
from fastapi import Depends, HTTPException, status
from sqlalchemy import  text
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
import core.database as database
import models.domain.hack as m
from core.database import engine
import core.config as config
from repositories import buildsite_repository as bsrepo 
from repositories import user_repository as urepo
from repositories import comments_repository as crepo
from repositories import sitejob_repository as sjrepo
from sqlalchemy.orm import Query
from typing import Tuple, List, Optional
from models.domain.hack import Buildsite, Comments
from models.schemas.hack import (
    ActiveJobResponce, BuildsitePaginationRequest, BuildsiteResponse, 
    BuildsiteListResponse, CommentCreationRequest, CommentCreationResponce, GeoData, CoordinatePoint, 
    BuildsiteExtendedResponse, ChecklistAnsResponse,
    CommentResponse, JobShiftResponse, SiteJobResponse, SiteStageResponse
)
from services.auth_service import ERole
from datetime import datetime
from core.logger import logger
from shapely.geometry import Point
from geoalchemy2.shape import from_shape

class BuildsiteService():
    def __init__(self, buildsite_repository: bsrepo.BuildsiteRepository, user_repository: urepo.UserRepository, comment_repository: crepo.CommentsRepository, sitejob_repository: sjrepo.SitejobRepository):
        self.buildsite_repository = buildsite_repository
        self.user_repository = user_repository
        self.comment_repository = comment_repository
        self.sitejob_repository = sitejob_repository

    def _apply_filters(self, query: Query[Buildsite], filters: BuildsitePaginationRequest) -> Query[Buildsite]:
        if filters.state_filter is not None:
            query = query.filter(Buildsite.state == filters.state_filter)
        
        if filters.search_text:
            query = query.filter(Buildsite.sitename.ilike(f"%{filters.search_text}%"))
        
        return query

    def _point_to_geo_data(self, point) -> Optional[dict]:
        if (point is None):
            return None
        from geoalchemy2.shape import to_shape
        point_sp =to_shape(point)

        return {
            'accuracy': None,
            'latitude': point_sp.y,
            'longitude': point_sp.x
        }

    def _extract_polygons_from_geometry(self, geometry) -> Optional[List[List[List[Tuple[float, float]]]]]:
        """
        Извлекает полигоны из MULTIPOLYGON геометрии.
        Возвращает список полигонов, где каждый полигон - список точек (lat, lon)
        """
        if geometry is None:
            return None
            
        try:
            from geoalchemy2.shape import to_shape
            shape = to_shape(geometry)
            
            polygons =[]
            
            if hasattr(shape, 'geoms'):
                for polygon in shape.geoms:
                    int_poly = []
                    if hasattr(polygon, 'exterior'):
                        exterior_coords = []
                        for coord in polygon.exterior.coords:
                            exterior_coords.append((coord[0], coord[1]))
                        int_poly.append(exterior_coords)
                    if len(polygon.interiors) > 0:
                        for interior in polygon.interiors:
                            interior_coords = []
                            for coords in interior.coords:
                                interior_coords.append((coord[0], coord[1]))
                            int_poly.append(interior_coords)
                    polygons.append(int_poly)
            elif hasattr(shape, 'exterior'):
                int_poly = []
                exterior_coords = []
                for coord in shape.exterior.coords:
                    exterior_coords.append((coord[0], coord[1]))
                int_poly.append(exterior_coords)
                if hasattr(polygon, 'interior'):
                    interior_coords = []
                    for coord in polygon.interior.coords:
                        interior_coords.append((coord[0], coord[1]))
                    int_poly.append(interior_coords)
                polygons.append(int_poly)
                
            return polygons if polygons else None
            
        except Exception as e:
            print(f"Error extracting polygons: {e}")
            return None

    def _calculate_centroid(self, polygons: List[List[List[Tuple[float, float]]]]) -> Optional[Tuple[float, float]]:
        """Вычисляет центроид для набора полигонов"""
        if not polygons:
            return None
            
        total_points = 0
        sum_lat = 0.0
        sum_lon = 0.0
        
        for polygon in polygons:
            exterior = polygon[0]
            for lat, lon in exterior:
                sum_lat += lat
                sum_lon += lon
                total_points += 1
                
        if total_points > 0:
            return (sum_lat / total_points, sum_lon / total_points)
        return None

    def _create_coordinates_response(self, polygons: List[List[List[Tuple[float, float]]]]) -> Optional[List[List[List[CoordinatePoint]]]]:
        if not polygons:
            return None
            
        result = []
        for polygon in polygons:
            full_poly = []
            for int_poly in polygon:
                polygon_points = []
                for lat, lon in int_poly:
                    polygon_points.append(CoordinatePoint(latitude=lat, longitude=lon))
                full_poly.append(polygon_points)
            result.append(full_poly)
        return result

    def _create_geo_data(self, polygons: List[List[List[Tuple[float, float]]]]) -> Optional[GeoData]:
        """Создает объект GeoData из центроида полигонов"""
        centroid = self._calculate_centroid(polygons)
        if centroid is None:
            return None
            
        latitude, longitude = centroid
        return GeoData(
            latitude=latitude,
            longitude=longitude,
            accuracy=None
        )

    def _checklist_ans_to_model(self, item: m.ChecklistAns) -> ChecklistAnsResponse:
        data = {
            "id": item.id,
            "author": None if item.author is None else self.user_repository.get_by_id(item.author),
            "answers": item.answers,
            "regtime": item.regtime,
            "geo": self._point_to_geo_data(item.geo),
        }

        return ChecklistAnsResponse.model_validate(data)

    def _comment_to_model(self, item: m.Comments) -> CommentResponse:
        data = {
            "id": item.id,
            "author": None if item.author is None else self.user_repository.get_by_id(item.author),
            "created_at": item.created_at,
            "state": item.state,
            "comment": item.comment,
            "fix_time": item.fix_time,
            "docs": item.docs,
            "type": item.type,
            "rec_type": item.rec_type,
            "linked_job": item.linked_job,
            "comment2file": [i.files for i in item.comment2file],
            "geo": self._point_to_geo_data(item.geo),
        }

        return CommentResponse.model_validate(data)

    def _jobs_to_model(self, item: m.Job2stage) -> SiteJobResponse:
        jobItem = item.sitejob
        data = {
            "seq": item.seq,
            "id": jobItem.id,
            "name": jobItem.name,
            "description": jobItem.description,
            "start_date": jobItem.jobschedule.planned_start,
            "end_date": jobItem.jobschedule.planned_end,
            "volume": jobItem.volume,
            "measurement": jobItem.measurement,
            "status": jobItem.status
        }
        return SiteJobResponse.model_validate(data)

    def _activejob_to_model(self, item: m.Job2stage) -> ActiveJobResponce:
        jobItem = item.sitejob
        data = {
            "seq": item.seq,
            "id": jobItem.id,
            "name": jobItem.name,
            "description": jobItem.description,
            "start_date": jobItem.jobschedule.planned_start,
            "end_date": jobItem.jobschedule.planned_end,
            "volume": jobItem.volume,
            "measurement": jobItem.measurement,
            "status": jobItem.status,
            "stage_seq": item.sitestage.seq,
            "stage_id": item.stageid
        }
        return ActiveJobResponce.model_validate(data)

    def _stage_to_model(self, item: m.Sitestage) -> SiteStageResponse:
        data = {
            "id": item.id,
            "site": item.site,
            "seq": item.seq,
            "name": item.name,
            "done": item.done,
            "job2stage": [self._jobs_to_model(i) for i in item.job2stage]
        }
        return SiteStageResponse.model_validate(data)
    
    def _find_job_shifts(self, item: m.Sitestage) -> List[JobShiftResponse]:
        res = []
        for i in item.job2stage:
            sched = i.sitejob.jobschedule
            if sched.jobshift is not None and len(sched.jobshift) > 0:
                for shift in sched.jobshift:
                    if shift.state == 0:
                        data = {
                            "id": shift.id,
                            "creator_name": self.user_repository.get_by_id(shift.creator).full_name(),
                            "comment": shift.description,
                            "created_at": shift.created_at,
                            "old_start_date": sched.planned_start,
                            "new_start_date": shift.newstart,
                            "old_end_date": sched.planned_end,
                            "new_end_date": shift.newend
                        }
                        res.append(JobShiftResponse.model_validate(data))
        return res

    def _buildsite_to_model(self, item: m.Buildsite, need_details: bool = False) -> BuildsiteResponse | BuildsiteExtendedResponse:
        polygons = self._extract_polygons_from_geometry(item.coordinates)
        coordinates_response = self._create_coordinates_response(polygons) if polygons else None
        geo_data_response = self._create_geo_data(polygons) if polygons else None

        change_present = False
        active_jobs_stage = []

        with engine.connect() as connection:
            result = connection.execute(text(f'select count(1) >= 1 flag from buildsite b left join sitestage s on s.site = b.id left join job2stage js on js.stageid = s.id left join sitejob sj on sj.id = js.jobid left join jobschedule jsh on sj.scheduled = jsh.id left join jobshift jf on jsh.id = jf.affected_jobsch  where jf.state = 0 and b.id = {item.id}'))
            for row in result:
                change_present = row.flag
            result = connection.execute(text(f'select js2.stageid stageid, js2.jobid jobid, js2.seq from job2stage js2 left join sitestage s2 on js2.stageid = s2.id left join sitejob s3 on js2.jobid = s3.id where (js2.stageid, js2.seq) in (select js.stageid, min(js.seq) from buildsite b left join sitestage s on s.site = b.id left join job2stage js on js.stageid = s.id left join sitejob sj on sj.id = js.jobid left join jobschedule jsh on sj.scheduled = jsh.id where b.id = {item.id} and sj.status = 0 and now() between jsh.planned_start and jsh.planned_end group by (js.stageid));'))
            for row in result:
                active_jobs_stage.append(self.sitejob_repository.get_job2stage_by_id(row.jobid, row.stageid))

        foreman = None
        for usr in item.users:
            if usr.role == 1:
                foreman = usr
                break
        data = {
            "id": item.id,
            "state": item.state,
            "sitename": item.sitename,
            "start_date": item.start_date,
            "state_changed": item.state_changed,
            "manager": item.manager,
            "manager_name": self.user_repository.get_by_id(item.manager).full_name(),
            "foreman": foreman.id,
            "foreman_name": None if foreman is None else foreman.full_name(),
            "acceptor": item.acceptor,
            "jobshift_present": change_present,
            "notes_count": self.comment_repository.get_active_notes_cnt(item),
            "warns_count": self.comment_repository.get_active_warns_cnt(item),
            "active_jobs": [self._activejob_to_model(i) for i in active_jobs_stage],
            "coordinates": coordinates_response,
            "geo_data": geo_data_response
        }

        if need_details is True:
            details = {
                "users": item.users,
                "jobshifts": [s for obj in item.sitestage for s in self._find_job_shifts(obj)],
                "checklist_ans": [self._checklist_ans_to_model(i) for i in item.checklist_ans],
                "sitestage": [self._stage_to_model(i) for i in item.sitestage],
                "buildsite2doc": item.buildsite2doc,
                "comments": [self._comment_to_model(i) for i in item.comments],
            }
            data.update(details)
            return BuildsiteExtendedResponse.model_validate(data)

        return BuildsiteResponse.model_validate(data)

    def get_available_objects(
        self, 
        user: m.Users, 
        request: BuildsitePaginationRequest
    ) -> BuildsiteListResponse:
        query: Query[Buildsite] = self.buildsite_repository.get_by_role(user)
        
        query = self._apply_filters(query, request)
        
        total = query.count()
        
        items = query.offset(
            (request.page - 1) * request.per_page
        ).limit(request.per_page).all()
        
        buildsite_responses = []
        for item in items:
            response_data = self._buildsite_to_model(item)
            buildsite_responses.append(response_data)
        
        total_pages = (total + request.per_page - 1) // request.per_page
        
        return BuildsiteListResponse(
            items=buildsite_responses,
            total=total,
            page=request.page,
            per_page=request.per_page,
            total_pages=total_pages
        )
    
    def check_buildsite_user_access(self, buildsite: Buildsite, user: m.Users) -> bool:
        match user.role:
            case ERole.CONTRACTOR:
                if buildsite.manager != user.id and buildsite.start_date <= datetime.now():
                    return False
            case _:
                if user not in buildsite.users:
                    return False
        return True

    def get_buildsite_by_id(
        self, 
        buildsite_id: int,
        user: m.Users,
        need_details: bool
    ) -> BuildsiteResponse:
        try:
            buildsite = self.buildsite_repository.get_by_id(buildsite_id)
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Buildsite not found",
            )
        
        if self.check_buildsite_user_access(buildsite, user) is not True:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden",
            )

        response_data = self._buildsite_to_model(buildsite, need_details)
        return response_data
    
    def process_comment_creation(
        self, 
        user: m.Users, 
        request: CommentCreationRequest
    ) -> CommentCreationResponce:
        have_rights = self.buildsite_repository.user_has_perms(user, request.site_id)
        if have_rights:
            buildiste = self.buildsite_repository.get_by_id(request.site_id)
            point_real = self.buildsite_repository.point_on_site(request.site_id, request.geo.longitude, request.geo.latitude,  request.geo.accuracy)
            if point_real:
                today = datetime.now().date()
                delta = None if request.fix_time is None else request.fix_time.date() - today
                delta_days = None if delta is None else delta.days
                comment = Comments(site = request.site_id,
                                    author = user.id,
                                    state = 0,
                                    comment = request.comment,
                                    fix_time= delta_days,
                                    docs= request.docs,
                                    geo= from_shape(Point(request.geo.longitude, request.geo.latitude), srid=4326),
                                    type= request.stop_type,
                                    rec_type= request.comm_type,
                                    linked_job= request.job_id,
                                    witness= request.witness)
                self.comment_repository.add_new(comment)
                if request.file_ids is not None:
                    for file_id in request.file_ids:
                        self.comment_repository.link_file(comment, file_id)
                data = {               
                    "is_done": True,
                    "error_text": ""
                }
            else:
                data = {               
                    "is_done": False,
                    "error_text": "Не на объекте"
                }
        else:
            data = {               
                "is_done": False,
                "error_text": "Недостаточно прав"
            }
            
        return CommentCreationResponce.model_validate(data)
    


    