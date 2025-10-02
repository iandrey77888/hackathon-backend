from typing import Any, Optional
import datetime
import decimal

from geoalchemy2.types import Geometry
from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKeyConstraint, Identity, Index, Integer, Numeric, PrimaryKeyConstraint, SmallInteger, Table, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


t_bu = Table(
    'bu', Base.metadata,
    schema='hack'
)


class Buildsite(Base):
    __tablename__ = 'buildsite'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='buildsite_pk'),
        {'schema': 'hack'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    state: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'), comment='-1 - stopped\n0 - planning\n1 - started')
    coordinates: Mapped[Optional[Any]] = mapped_column(Geometry('MULTIPOLYGON', 4326, 2, False, from_text='ST_GeomFromEWKT', name='geometry'))
    start_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='If not started - planned date\nIf started - real date')
    state_changed: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    manager: Mapped[Optional[int]] = mapped_column(BigInteger)
    acceptor: Mapped[Optional[int]] = mapped_column(BigInteger)
    sitename: Mapped[Optional[str]] = mapped_column(Text)

    users: Mapped[list['Users']] = relationship('Users', secondary='hack.user2site', back_populates='buildsite')
    checklist_ans: Mapped[list['ChecklistAns']] = relationship('ChecklistAns', back_populates='buildsite')
    sitestage: Mapped[list['Sitestage']] = relationship('Sitestage', back_populates='buildsite')
    buildsite2doc: Mapped[list['Buildsite2doc']] = relationship('Buildsite2doc', back_populates='buildsite_')
    comments: Mapped[list['Comments']] = relationship('Comments', back_populates='buildsite')


class ChecklistTemplate(Base):
    __tablename__ = 'checklist_template'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='checllist_template_pk'),
        {'schema': 'hack'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    schedule: Mapped[Optional[int]] = mapped_column(Integer)
    questions: Mapped[Optional[dict]] = mapped_column(JSONB)

    checklist_ans: Mapped[list['ChecklistAns']] = relationship('ChecklistAns', back_populates='checklist_template')


class Jobschedule(Base):
    __tablename__ = 'jobschedule'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='jobschedule_pk'),
        {'schema': 'hack'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    planned_start: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    planned_end: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    version: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    prev: Mapped[Optional[int]] = mapped_column(BigInteger)

    jobshift: Mapped[list['Jobshift']] = relationship('Jobshift', back_populates='jobschedule')
    sitejob: Mapped[list['Sitejob']] = relationship('Sitejob', back_populates='jobschedule')


class Material(Base):
    __tablename__ = 'material'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='material_pk'),
        {'schema': 'hack'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(Text)
    properties: Mapped[Optional[str]] = mapped_column(Text)
    measurement: Mapped[Optional[str]] = mapped_column(Text)

    required_mats: Mapped[list['RequiredMats']] = relationship('RequiredMats', back_populates='material')
    shipped_mats: Mapped[list['ShippedMats']] = relationship('ShippedMats', back_populates='material')


class Supplier(Base):
    __tablename__ = 'supplier'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='supplier_pk'),
        {'schema': 'hack'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(Text)

    shipment: Mapped[list['Shipment']] = relationship('Shipment', back_populates='supplier_')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pk'),
        {'schema': 'hack'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    username: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(Text)
    surname: Mapped[Optional[str]] = mapped_column(Text)
    patronym: Mapped[Optional[str]] = mapped_column(Text)
    role: Mapped[Optional[int]] = mapped_column(SmallInteger, comment='0 - owner\n1 - contractor\n2 - inspector')
    pwdhash: Mapped[Optional[str]] = mapped_column(Text)

    buildsite: Mapped[list['Buildsite']] = relationship('Buildsite', secondary='hack.user2site', back_populates='users')
    checklist_ans: Mapped[list['ChecklistAns']] = relationship('ChecklistAns', back_populates='users')
    files: Mapped[list['Files']] = relationship('Files', back_populates='users')
    jobshift: Mapped[list['Jobshift']] = relationship('Jobshift', foreign_keys='[Jobshift.checker]', back_populates='users')
    jobshift_: Mapped[list['Jobshift']] = relationship('Jobshift', foreign_keys='[Jobshift.creator]', back_populates='users_')
    shipment: Mapped[list['Shipment']] = relationship('Shipment', back_populates='users')
    comments: Mapped[list['Comments']] = relationship('Comments', back_populates='users')
    jobverification: Mapped[list['Jobverification']] = relationship('Jobverification', back_populates='users')
    comment_fix: Mapped[list['CommentFix']] = relationship('CommentFix', foreign_keys='[CommentFix.acceptor]', back_populates='users')
    comment_fix_: Mapped[list['CommentFix']] = relationship('CommentFix', foreign_keys='[CommentFix.creator]', back_populates='users_')

    def __str__(self):
        return f'#{self.id} {self.username}'
    
    def full_name(self):
        return f'{self.surname} {self.name}'


class ChecklistAns(Base):
    __tablename__ = 'checklist_ans'
    __table_args__ = (
        ForeignKeyConstraint(['author'], ['hack.users.id'], name='ans2author'),
        ForeignKeyConstraint(['checklist'], ['hack.checklist_template.id'], name='ans2check'),
        ForeignKeyConstraint(['linkedsite'], ['hack.buildsite.id'], name='ans2site'),
        PrimaryKeyConstraint('id', name='checklist_ans_pk'),
        {'schema': 'hack'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    checklist: Mapped[Optional[int]] = mapped_column(BigInteger)
    author: Mapped[Optional[int]] = mapped_column(BigInteger)
    linkedsite: Mapped[Optional[int]] = mapped_column(BigInteger)
    answers: Mapped[Optional[dict]] = mapped_column(JSONB)
    regtime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    geo: Mapped[Optional[Any]] = mapped_column(Geometry('POINT', 4326, 2, False, from_text='ST_GeomFromEWKT', name='geometry'))

    users: Mapped[Optional['Users']] = relationship('Users', back_populates='checklist_ans')
    checklist_template: Mapped[Optional['ChecklistTemplate']] = relationship('ChecklistTemplate', back_populates='checklist_ans')
    buildsite: Mapped[Optional['Buildsite']] = relationship('Buildsite', back_populates='checklist_ans')


class Files(Base):
    __tablename__ = 'files'
    __table_args__ = (
        ForeignKeyConstraint(['uploader'], ['hack.users.id'], name='fileuploader2user'),
        PrimaryKeyConstraint('id', name='files_pk'),
        {'schema': 'hack'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    file_key: Mapped[Optional[str]] = mapped_column(Text)
    bucket: Mapped[Optional[str]] = mapped_column(Text)
    filename: Mapped[Optional[str]] = mapped_column(Text)
    mime_type: Mapped[Optional[str]] = mapped_column(Text)
    size: Mapped[Optional[str]] = mapped_column(Text)
    checksum256: Mapped[Optional[str]] = mapped_column(Text)
    uploader: Mapped[Optional[int]] = mapped_column(BigInteger)

    users: Mapped[Optional['Users']] = relationship('Users', back_populates='files')
    jobprogres: Mapped[list['Jobprogres']] = relationship('Jobprogres', secondary='hack.prog2files', back_populates='files')
    shipped_mats: Mapped[list['ShippedMats']] = relationship('ShippedMats', secondary='hack.shipmat2file', back_populates='files')
    comment_fix: Mapped[list['CommentFix']] = relationship('CommentFix', secondary='hack.commentfix2file', back_populates='files')
    lab_res: Mapped[list['LabRes']] = relationship('LabRes', secondary='hack.lab2file', back_populates='files')
    buildsite2doc: Mapped[list['Buildsite2doc']] = relationship('Buildsite2doc', back_populates='files')
    comment2file: Mapped[list['Comment2file']] = relationship('Comment2file', back_populates='files')


class Jobshift(Base):
    __tablename__ = 'jobshift'
    __table_args__ = (
        ForeignKeyConstraint(['affected_jobsch'], ['hack.jobschedule.id'], name='shift2job'),
        ForeignKeyConstraint(['checker'], ['hack.users.id'], name='shift2checker'),
        ForeignKeyConstraint(['creator'], ['hack.users.id'], name='shift2creator'),
        PrimaryKeyConstraint('id', name='jobshift_pk'),
        {'schema': 'hack'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    affected_jobsch: Mapped[Optional[int]] = mapped_column(BigInteger)
    creator: Mapped[Optional[int]] = mapped_column(BigInteger)
    state: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'), comment='0 - proposed\n1 - accepted\n2 - rejected')
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    state_change: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    checker: Mapped[Optional[int]] = mapped_column(BigInteger)
    newstart: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    newend: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    checker_comment: Mapped[Optional[str]] = mapped_column(Text)

    jobschedule: Mapped[Optional['Jobschedule']] = relationship('Jobschedule', back_populates='jobshift')
    users: Mapped[Optional['Users']] = relationship('Users', foreign_keys=[checker], back_populates='jobshift')
    users_: Mapped[Optional['Users']] = relationship('Users', foreign_keys=[creator], back_populates='jobshift_')


class Shipment(Base):
    __tablename__ = 'shipment'
    __table_args__ = (
        ForeignKeyConstraint(['acceptor'], ['hack.users.id'], name='shipment2acceptor'),
        ForeignKeyConstraint(['supplier'], ['hack.supplier.id'], name='shipment2supplier'),
        PrimaryKeyConstraint('id', name='shipment_pk'),
        {'schema': 'hack'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    scheduled_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    arrived_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    supplier: Mapped[Optional[int]] = mapped_column(BigInteger)
    state: Mapped[Optional[int]] = mapped_column(Integer, comment='0 - scheduled\n1 - accepted\n2 - rejected')
    comment: Mapped[Optional[str]] = mapped_column(Text)
    acceptor: Mapped[Optional[int]] = mapped_column(BigInteger)
    doc_serial: Mapped[Optional[str]] = mapped_column(Text)
    package_state: Mapped[Optional[str]] = mapped_column(Text)
    geo: Mapped[Optional[Any]] = mapped_column(Geometry('POINT', 4326, 2, False, from_text='ST_GeomFromEWKT', name='geometry'))

    users: Mapped[Optional['Users']] = relationship('Users', back_populates='shipment')
    supplier_: Mapped[Optional['Supplier']] = relationship('Supplier', back_populates='shipment')
    shipment_files: Mapped[list['ShipmentFiles']] = relationship('ShipmentFiles', back_populates='shipment_')
    shipped_mats: Mapped[list['ShippedMats']] = relationship('ShippedMats', back_populates='shipment')


class Sitejob(Base):
    __tablename__ = 'sitejob'
    __table_args__ = (
        ForeignKeyConstraint(['scheduled'], ['hack.jobschedule.id'], name='job2sched'),
        PrimaryKeyConstraint('id', name='sitejob_pk'),
        {'schema': 'hack'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    scheduled: Mapped[int] = mapped_column(BigInteger, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    volume: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    measurement: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[Optional[int]] = mapped_column(Integer, comment='0 - not started\n1 - started\n2 - finished, unverified\n3 - finished, rejected\n4 - finished, verified')

    jobschedule: Mapped['Jobschedule'] = relationship('Jobschedule', back_populates='sitejob')
    comments: Mapped[list['Comments']] = relationship('Comments', back_populates='sitejob')
    job2stage: Mapped[list['Job2stage']] = relationship('Job2stage', back_populates='sitejob')
    jobprogres: Mapped[list['Jobprogres']] = relationship('Jobprogres', back_populates='sitejob')
    jobverification: Mapped[list['Jobverification']] = relationship('Jobverification', back_populates='sitejob_')
    required_mats: Mapped[list['RequiredMats']] = relationship('RequiredMats', back_populates='sitejob')


class Sitestage(Base):
    __tablename__ = 'sitestage'
    __table_args__ = (
        ForeignKeyConstraint(['site'], ['hack.buildsite.id'], name='site2sitestage'),
        PrimaryKeyConstraint('id', name='sitestage_pk'),
        UniqueConstraint('site', 'seq', name='stageuq_constr'),
        {'schema': 'hack'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    site: Mapped[Optional[int]] = mapped_column(BigInteger)
    seq: Mapped[Optional[int]] = mapped_column(Integer)
    name: Mapped[Optional[str]] = mapped_column(Text)
    done: Mapped[Optional[bool]] = mapped_column(Boolean)

    buildsite: Mapped[Optional['Buildsite']] = relationship('Buildsite', back_populates='sitestage')
    job2stage: Mapped[list['Job2stage']] = relationship('Job2stage', back_populates='sitestage')


t_user2site = Table(
    'user2site', Base.metadata,
    Column('userid', BigInteger, primary_key=True),
    Column('siteid', BigInteger, primary_key=True),
    ForeignKeyConstraint(['siteid'], ['hack.buildsite.id'], name='user2site_site'),
    ForeignKeyConstraint(['userid'], ['hack.users.id'], name='user2site_user'),
    PrimaryKeyConstraint('userid', 'siteid', name='user2site_pk'),
    schema='hack'
)


class Buildsite2doc(Base):
    __tablename__ = 'buildsite2doc'
    __table_args__ = (
        ForeignKeyConstraint(['buildsite'], ['hack.buildsite.id'], name='sitedoc2site'),
        ForeignKeyConstraint(['file'], ['hack.files.id'], name='sitedoc2doc'),
        PrimaryKeyConstraint('buildsite', 'file', name='buildsite2doc_pk'),
        {'schema': 'hack'}
    )

    buildsite: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    file: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    type: Mapped[Optional[int]] = mapped_column(Integer)

    buildsite_: Mapped['Buildsite'] = relationship('Buildsite', back_populates='buildsite2doc')
    files: Mapped['Files'] = relationship('Files', back_populates='buildsite2doc')


class Comments(Base):
    __tablename__ = 'comments'
    __table_args__ = (
        ForeignKeyConstraint(['author'], ['hack.users.id'], name='notice2author'),
        ForeignKeyConstraint(['linked_job'], ['hack.sitejob.id'], name='comment2job'),
        ForeignKeyConstraint(['site'], ['hack.buildsite.id'], name='notice2site'),
        PrimaryKeyConstraint('id', name='notices_pk'),
        Index('comment_type_notice_idx', 'id'),
        Index('comment_type_warning_idx', 'id'),
        {'schema': 'hack'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    site: Mapped[int] = mapped_column(BigInteger, nullable=False)
    author: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    state: Mapped[Optional[int]] = mapped_column(Integer)
    comment: Mapped[Optional[str]] = mapped_column(Text)
    fix_time: Mapped[Optional[int]] = mapped_column(Integer, comment='days')
    docs: Mapped[Optional[str]] = mapped_column(Text)
    geo: Mapped[Optional[Any]] = mapped_column(Geometry('POINT', 4326, 2, False, from_text='ST_GeomFromEWKT', name='geometry'))
    type: Mapped[Optional[int]] = mapped_column(Integer)
    rec_type: Mapped[Optional[int]] = mapped_column(Integer, comment='0 - notice\n1 - warning')
    linked_job: Mapped[Optional[int]] = mapped_column(BigInteger)
    witness: Mapped[Optional[str]] = mapped_column(Text)
    document_list: Mapped[Optional[str]] = mapped_column(Text)

    users: Mapped[Optional['Users']] = relationship('Users', back_populates='comments')
    sitejob: Mapped[Optional['Sitejob']] = relationship('Sitejob', back_populates='comments')
    buildsite: Mapped['Buildsite'] = relationship('Buildsite', back_populates='comments')
    comment2file: Mapped[list['Comment2file']] = relationship('Comment2file', back_populates='comments')
    comment_fix: Mapped[list['CommentFix']] = relationship('CommentFix', back_populates='comments')


class Job2stage(Base):
    __tablename__ = 'job2stage'
    __table_args__ = (
        ForeignKeyConstraint(['jobid'], ['hack.sitejob.id'], name='j2s_job'),
        ForeignKeyConstraint(['stageid'], ['hack.sitestage.id'], name='j2s_stage'),
        PrimaryKeyConstraint('stageid', 'jobid', name='job2stage_pk'),
        {'schema': 'hack'}
    )

    stageid: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    jobid: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    seq: Mapped[int] = mapped_column(Integer, nullable=False)

    sitejob: Mapped['Sitejob'] = relationship('Sitejob', back_populates='job2stage')
    sitestage: Mapped['Sitestage'] = relationship('Sitestage', back_populates='job2stage')


class Jobprogres(Base):
    __tablename__ = 'jobprogres'
    __table_args__ = (
        ForeignKeyConstraint(['linkedjob'], ['hack.sitejob.id'], name='linkedjob2job'),
        PrimaryKeyConstraint('id', name='jobprogres_pk'),
        {'schema': 'hack'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    regtime: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    linkedjob: Mapped[Optional[int]] = mapped_column(BigInteger)
    comment: Mapped[Optional[str]] = mapped_column(Text)
    geo: Mapped[Optional[Any]] = mapped_column(Geometry('POINT', 4326, 2, False, from_text='ST_GeomFromEWKT', name='geometry'))

    files: Mapped[list['Files']] = relationship('Files', secondary='hack.prog2files', back_populates='jobprogres')
    sitejob: Mapped[Optional['Sitejob']] = relationship('Sitejob', back_populates='jobprogres')


class Jobverification(Base):
    __tablename__ = 'jobverification'
    __table_args__ = (
        ForeignKeyConstraint(['sitejob'], ['hack.sitejob.id'], name='ver2job'),
        ForeignKeyConstraint(['verifier'], ['hack.users.id'], name='ver2verifier'),
        PrimaryKeyConstraint('id', name='jobverification_pk'),
        {'schema': 'hack'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    regtime: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    verifier: Mapped[int] = mapped_column(BigInteger, nullable=False)
    sitejob: Mapped[Optional[int]] = mapped_column(BigInteger)
    result: Mapped[Optional[int]] = mapped_column(Integer)
    comment: Mapped[Optional[str]] = mapped_column(Text)
    geo: Mapped[Optional[Any]] = mapped_column(Geometry('POINT', 4326, 2, False, from_text='ST_GeomFromEWKT', name='geometry'))

    sitejob_: Mapped[Optional['Sitejob']] = relationship('Sitejob', back_populates='jobverification')
    users: Mapped['Users'] = relationship('Users', back_populates='jobverification')


class RequiredMats(Base):
    __tablename__ = 'required_mats'
    __table_args__ = (
        ForeignKeyConstraint(['jobid'], ['hack.sitejob.id'], name='reqmat2job'),
        ForeignKeyConstraint(['materialid'], ['hack.material.id'], name='reqmat2mat'),
        PrimaryKeyConstraint('jobid', 'materialid', name='required_mats_pk'),
        {'schema': 'hack'}
    )

    jobid: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    materialid: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    volume: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)

    sitejob: Mapped['Sitejob'] = relationship('Sitejob', back_populates='required_mats')
    material: Mapped['Material'] = relationship('Material', back_populates='required_mats')
    mat_usage: Mapped[list['MatUsage']] = relationship('MatUsage', back_populates='required_mats')


class ShipmentFiles(Files):
    __tablename__ = 'shipment_files'
    __table_args__ = (
        ForeignKeyConstraint(['id'], ['hack.files.id'], name='shipmentfile2file'),
        ForeignKeyConstraint(['shipment'], ['hack.shipment.id'], name='shipmentfile2shipment'),
        PrimaryKeyConstraint('id', name='shipment_files_pk'),
        {'schema': 'hack'}
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    shipment: Mapped[Optional[int]] = mapped_column(BigInteger)
    category: Mapped[Optional[int]] = mapped_column(Integer, comment='File category\n0 - shipment docs\n1 - certificates\n2 - misc')
    description: Mapped[Optional[str]] = mapped_column(Text)
    shipment_: Mapped[Optional['Shipment']] = relationship('Shipment', back_populates='shipment_files')


class ShippedMats(Base):
    __tablename__ = 'shipped_mats'
    __table_args__ = (
        ForeignKeyConstraint(['materialid'], ['hack.material.id'], name='shmat2mat'),
        ForeignKeyConstraint(['shipmentid'], ['hack.shipment.id'], name='shmat2shipment'),
        PrimaryKeyConstraint('shipmentid', 'materialid', name='bu_cp_pk'),
        {'schema': 'hack'}
    )

    shipmentid: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    materialid: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    volume: Mapped[decimal.Decimal] = mapped_column(Numeric, nullable=False)
    serial: Mapped[Optional[str]] = mapped_column(Text)
    accepted: Mapped[Optional[bool]] = mapped_column(Boolean)
    spent: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    lab_required: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    files: Mapped[list['Files']] = relationship('Files', secondary='hack.shipmat2file', back_populates='shipped_mats')
    material: Mapped['Material'] = relationship('Material', back_populates='shipped_mats')
    shipment: Mapped['Shipment'] = relationship('Shipment', back_populates='shipped_mats')
    lab_res: Mapped[list['LabRes']] = relationship('LabRes', back_populates='shipped_mats')
    mat_usage: Mapped[list['MatUsage']] = relationship('MatUsage', back_populates='shipped_mats')


class Comment2file(Base):
    __tablename__ = 'comment2file'
    __table_args__ = (
        ForeignKeyConstraint(['file'], ['hack.files.id'], name='nf2file'),
        ForeignKeyConstraint(['notice'], ['hack.comments.id'], name='nf2notice'),
        PrimaryKeyConstraint('notice', 'file', name='notice2file_pk'),
        {'schema': 'hack'}
    )

    notice: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    file: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    description: Mapped[Optional[int]] = mapped_column(SmallInteger)

    files: Mapped['Files'] = relationship('Files', back_populates='comment2file')
    comments: Mapped['Comments'] = relationship('Comments', back_populates='comment2file')


class CommentFix(Base):
    __tablename__ = 'comment_fix'
    __table_args__ = (
        ForeignKeyConstraint(['acceptor'], ['hack.users.id'], name='fix2acceptor'),
        ForeignKeyConstraint(['creator'], ['hack.users.id'], name='fix2author'),
        ForeignKeyConstraint(['notice'], ['hack.comments.id'], name='fix2notice'),
        PrimaryKeyConstraint('id', name='notice_fix_pk'),
        {'schema': 'hack'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    notice: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_at: Mapped[Optional[int]] = mapped_column(BigInteger)
    comment: Mapped[Optional[int]] = mapped_column(SmallInteger)
    creator: Mapped[Optional[int]] = mapped_column(BigInteger)
    state: Mapped[Optional[int]] = mapped_column(SmallInteger, comment='0 - pending\n1 - accepted\n2 - rejected')
    acceptor: Mapped[Optional[int]] = mapped_column(BigInteger)
    acceptor_comment: Mapped[Optional[int]] = mapped_column(SmallInteger)
    state_changed: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    geo: Mapped[Optional[Any]] = mapped_column(Geometry('POINT', 4326, 2, False, from_text='ST_GeomFromEWKT', name='geometry'))

    files: Mapped[list['Files']] = relationship('Files', secondary='hack.commentfix2file', back_populates='comment_fix')
    users: Mapped[Optional['Users']] = relationship('Users', foreign_keys=[acceptor], back_populates='comment_fix')
    users_: Mapped[Optional['Users']] = relationship('Users', foreign_keys=[creator], back_populates='comment_fix_')
    comments: Mapped[Optional['Comments']] = relationship('Comments', back_populates='comment_fix')


class LabRes(Base):
    __tablename__ = 'lab_res'
    __table_args__ = (
        ForeignKeyConstraint(['shipmentid', 'materialid'], ['hack.shipped_mats.shipmentid', 'hack.shipped_mats.materialid'], name='lab2ship'),
        PrimaryKeyConstraint('id', name='labship_pk'),
        {'schema': 'hack'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    shipmentid: Mapped[Optional[int]] = mapped_column(BigInteger)
    materialid: Mapped[Optional[int]] = mapped_column(BigInteger)
    result: Mapped[Optional[int]] = mapped_column(BigInteger)

    files: Mapped[list['Files']] = relationship('Files', secondary='hack.lab2file', back_populates='lab_res')
    shipped_mats: Mapped[Optional['ShippedMats']] = relationship('ShippedMats', back_populates='lab_res')


class MatUsage(Base):
    __tablename__ = 'mat_usage'
    __table_args__ = (
        ForeignKeyConstraint(['materialid', 'shipmentid'], ['hack.shipped_mats.materialid', 'hack.shipped_mats.shipmentid'], name='matspent2ship'),
        ForeignKeyConstraint(['sitejob', 'materialid'], ['hack.required_mats.jobid', 'hack.required_mats.materialid'], name='matspent2req'),
        PrimaryKeyConstraint('id', name='mat_usage_pk'),
        {'schema': 'hack'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    regtime: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    sitejob: Mapped[Optional[int]] = mapped_column(BigInteger)
    materialid: Mapped[Optional[int]] = mapped_column(BigInteger)
    shipmentid: Mapped[Optional[int]] = mapped_column(BigInteger)
    spent: Mapped[Optional[int]] = mapped_column(BigInteger)

    shipped_mats: Mapped[Optional['ShippedMats']] = relationship('ShippedMats', back_populates='mat_usage')
    required_mats: Mapped[Optional['RequiredMats']] = relationship('RequiredMats', back_populates='mat_usage')


t_prog2files = Table(
    'prog2files', Base.metadata,
    Column('progresrep', BigInteger, primary_key=True),
    Column('file', BigInteger, primary_key=True),
    ForeignKeyConstraint(['file'], ['hack.files.id'], name='progfile2file'),
    ForeignKeyConstraint(['progresrep'], ['hack.jobprogres.id'], name='progfile2prog'),
    PrimaryKeyConstraint('progresrep', 'file', name='prog2files_pk'),
    schema='hack'
)


t_shipmat2file = Table(
    'shipmat2file', Base.metadata,
    Column('shippedmat', BigInteger, primary_key=True),
    Column('file', BigInteger, primary_key=True),
    Column('materialid', BigInteger, primary_key=True),
    ForeignKeyConstraint(['file'], ['hack.files.id'], name='shipmatfile2file'),
    ForeignKeyConstraint(['shippedmat', 'materialid'], ['hack.shipped_mats.shipmentid', 'hack.shipped_mats.materialid'], name='shipmatfile2mat'),
    PrimaryKeyConstraint('shippedmat', 'file', 'materialid', name='shipmat2file_pk'),
    schema='hack'
)


t_commentfix2file = Table(
    'commentfix2file', Base.metadata,
    Column('noticefix', BigInteger, primary_key=True),
    Column('file', BigInteger, primary_key=True),
    ForeignKeyConstraint(['file'], ['hack.files.id'], name='ntfixfile2file'),
    ForeignKeyConstraint(['noticefix'], ['hack.comment_fix.id'], name='nfixfile2fix'),
    PrimaryKeyConstraint('noticefix', 'file', name='noticefix2file_pk'),
    schema='hack'
)


t_lab2file = Table(
    'lab2file', Base.metadata,
    Column('labrec', BigInteger, primary_key=True),
    Column('file', BigInteger, primary_key=True),
    ForeignKeyConstraint(['file'], ['hack.files.id'], name='labfile2file'),
    ForeignKeyConstraint(['labrec'], ['hack.lab_res.id'], name='labfile2labrec'),
    PrimaryKeyConstraint('labrec', 'file', name='lab2file_pk'),
    schema='hack'
)
