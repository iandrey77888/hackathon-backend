-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler version: 1.0.4
-- PostgreSQL version: 15.0
-- Project Site: pgmodeler.io
-- Model Author: ---
-- object: mh_admin | type: ROLE --
-- DROP ROLE IF EXISTS mh_admin;
CREATE ROLE mh_admin WITH 
	CREATEDB
	LOGIN
	 PASSWORD 'mh_admin';
-- ddl-end --

-- object: mh_admin_cp | type: ROLE --
-- DROP ROLE IF EXISTS mh_admin_cp;
CREATE ROLE mh_admin_cp WITH 
	CREATEDB
	LOGIN
	 PASSWORD 'mh_admin';
-- ddl-end --

-- Tablespaces creation must be performed outside a multi lined SQL file. 
-- These commands were put in this file only as a convenience.
-- 
-- object: hacktbsp | type: TABLESPACE --
-- DROP TABLESPACE IF EXISTS hacktbsp CASCADE;
CREATE TABLESPACE hacktbsp
	OWNER mh_admin
	LOCATION '/hacktbsp/';

-- ddl-end --



-- Database creation must be performed outside a multi lined SQL file. 
-- These commands were put in this file only as a convenience.
-- 
-- object: mh_db | type: DATABASE --
-- DROP DATABASE IF EXISTS mh_db;
CREATE DATABASE mh_db
	TABLESPACE = pg_default
	OWNER = mh_admin;
-- ddl-end --


-- object: hack | type: SCHEMA --
-- DROP SCHEMA IF EXISTS hack CASCADE;
CREATE SCHEMA hack;
-- ddl-end --
ALTER SCHEMA hack OWNER TO mh_admin;
-- ddl-end --

SET search_path TO pg_catalog,public,hack;
-- ddl-end --

-- object: hack.buildsite | type: TABLE --
-- DROP TABLE IF EXISTS hack.buildsite;
CREATE TABLE hack.buildsite (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	coordinates  geometry(MultiPolygon, 4326),
	state integer NOT NULL DEFAULT 0,
	start_date timestamp,
	state_changed timestamp,
	manager bigint,
	acceptor bigint,
	sitename text,
	CONSTRAINT buildsite_pk PRIMARY KEY (id)
)
TABLESPACE pg_default;
-- ddl-end --
COMMENT ON COLUMN hack.buildsite.state IS E'-1 - stopped\n0 - planning\n1 - started';
-- ddl-end --
COMMENT ON COLUMN hack.buildsite.start_date IS E'If not started - planned date\nIf started - real date';
-- ddl-end --
ALTER TABLE hack.buildsite OWNER TO mh_admin;
-- ddl-end --

-- object: hack.bu | type: TABLE --
-- DROP TABLE IF EXISTS hack.bu;
CREATE TABLE hack.bu (

)
TABLESPACE pg_default;
-- ddl-end --
ALTER TABLE hack.bu OWNER TO mh_admin;
-- ddl-end --

-- object: hack.users | type: TABLE --
-- DROP TABLE IF EXISTS hack.users;
CREATE TABLE hack.users (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	name text,
	surname text,
	patronym text,
	role smallint,
	username text NOT NULL,
	pwdhash text,
	CONSTRAINT users_pk PRIMARY KEY (id)
)
TABLESPACE pg_default;
-- ddl-end --
COMMENT ON COLUMN hack.users.role IS E'0 - owner\n1 - contractor\n2 - inspector';
-- ddl-end --
ALTER TABLE hack.users OWNER TO mh_admin;
-- ddl-end --

-- object: hack.comments | type: TABLE --
-- DROP TABLE IF EXISTS hack.comments;
CREATE TABLE hack.comments (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	site bigint NOT NULL,
	author bigint,
	created_at timestamp DEFAULT now(),
	state integer,
	comment text,
	fix_time integer,
	docs text,
	geo geometry(Point, 4326),
	type integer,
	rec_type integer,
	linked_job bigint,
	witness text, 
	document_list text,
	CONSTRAINT notices_pk PRIMARY KEY (id)
)
TABLESPACE pg_default;
-- ddl-end --
COMMENT ON COLUMN hack.comments.fix_time IS E'days';
-- ddl-end --
COMMENT ON COLUMN hack.comments.rec_type IS E'0 - notice\n1 - warning';
-- ddl-end --
ALTER TABLE hack.comments OWNER TO mh_admin;
-- ddl-end --

-- object: hack.files | type: TABLE --
-- DROP TABLE IF EXISTS hack.files;
CREATE TABLE hack.files (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	file_key text,
	bucket text,
	filename text,
	mime_type text,
	size text,
	checksum256 text,
	uploader bigint,
	created_at timestamp NOT NULL DEFAULT now(),
	CONSTRAINT files_pk PRIMARY KEY (id)
)
TABLESPACE pg_default;
-- ddl-end --
ALTER TABLE hack.files OWNER TO mh_admin;
-- ddl-end --

-- object: hack.user2site | type: TABLE --
-- DROP TABLE IF EXISTS hack.user2site;
CREATE TABLE hack.user2site (
	userid bigint NOT NULL,
	siteid bigint NOT NULL,
	CONSTRAINT user2site_pk PRIMARY KEY (userid,siteid)
)
TABLESPACE pg_default;
-- ddl-end --
ALTER TABLE hack.user2site OWNER TO mh_admin;
-- ddl-end --

-- object: hack.sitejob | type: TABLE --
-- DROP TABLE IF EXISTS hack.sitejob;
CREATE TABLE hack.sitejob (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	name text,
	description text,
	scheduled bigint NOT NULL,
	volume numeric,
	measurement text,
	status integer,
	CONSTRAINT sitejob_pk PRIMARY KEY (id)
)
TABLESPACE pg_default;
-- ddl-end --
COMMENT ON COLUMN hack.sitejob.status IS E'0 - not started\n1 - started\n2 - finished, unverified\n3 - finished, rejected\n4 - finished, verified';
-- ddl-end --
ALTER TABLE hack.sitejob OWNER TO mh_admin;
-- ddl-end --

-- object: hack.sitestage | type: TABLE --
-- DROP TABLE IF EXISTS hack.sitestage;
CREATE TABLE hack.sitestage (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	site bigint,
	seq integer,
	name text,
	done boolean,
	CONSTRAINT sitestage_pk PRIMARY KEY (id),
	CONSTRAINT stageuq_constr UNIQUE (site,seq)
)
TABLESPACE pg_default;
-- ddl-end --
ALTER TABLE hack.sitestage OWNER TO mh_admin;
-- ddl-end --

-- object: hack.job2stage | type: TABLE --
-- DROP TABLE IF EXISTS hack.job2stage;
CREATE TABLE hack.job2stage (
	stageid bigint NOT NULL,
	jobid bigint NOT NULL,
	seq integer NOT NULL,
	CONSTRAINT job2stage_pk PRIMARY KEY (stageid,jobid)
)
TABLESPACE pg_default;
-- ddl-end --
ALTER TABLE hack.job2stage OWNER TO mh_admin;
-- ddl-end --

-- object: hack.jobshift | type: TABLE --
-- DROP TABLE IF EXISTS hack.jobshift;
CREATE TABLE hack.jobshift (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	affected_jobsch bigint,
	creator bigint,
	state integer DEFAULT 0,
	description text,
	created_at timestamp DEFAULT now(),
	state_change timestamp,
	checker bigint,
	newstart timestamp,
	newend timestamp,
	checker_comment text,
	CONSTRAINT jobshift_pk PRIMARY KEY (id)
)
TABLESPACE pg_default;
-- ddl-end --
COMMENT ON COLUMN hack.jobshift.state IS E'0 - proposed\n1 - accepted\n2 - rejected';
-- ddl-end --
ALTER TABLE hack.jobshift OWNER TO mh_admin;
-- ddl-end --

-- object: hack.jobschedule | type: TABLE --
-- DROP TABLE IF EXISTS hack.jobschedule;
CREATE TABLE hack.jobschedule (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	version integer DEFAULT 0,
	prev bigint,
	planned_start timestamp NOT NULL,
	planned_end timestamp NOT NULL,
	CONSTRAINT jobschedule_pk PRIMARY KEY (id)
)
TABLESPACE pg_default;
-- ddl-end --
ALTER TABLE hack.jobschedule OWNER TO mh_admin;
-- ddl-end --

-- object: hack.shipment | type: TABLE --
-- DROP TABLE IF EXISTS hack.shipment;
CREATE TABLE hack.shipment (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	scheduled_at timestamp,
	arrived_at timestamp,
	supplier bigint,
	state integer,
	comment text,
	acceptor bigint,
	doc_serial text,
	package_state text,
	geo geometry(Point, 4326),
	CONSTRAINT shipment_pk PRIMARY KEY (id)
)
TABLESPACE pg_default;
-- ddl-end --
COMMENT ON COLUMN hack.shipment.state IS E'0 - scheduled\n1 - accepted\n2 - rejected';
-- ddl-end --
ALTER TABLE hack.shipment OWNER TO mh_admin;
-- ddl-end --

-- object: hack.material | type: TABLE --
-- DROP TABLE IF EXISTS hack.material CASCADE;
CREATE TABLE hack.material (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	name text,
	properties text,
	measurement text,
	CONSTRAINT material_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE hack.material OWNER TO mh_admin;
-- ddl-end --

-- object: hack.shipped_mats | type: TABLE --
-- DROP TABLE IF EXISTS hack.shipped_mats;
CREATE TABLE hack.shipped_mats (
	shipmentid bigint NOT NULL,
	materialid bigint NOT NULL,
	volume numeric NOT NULL,
	serial text,
	accepted boolean,
	spent numeric,
	lab_required boolean DEFAULT false,
	CONSTRAINT bu_cp_pk PRIMARY KEY (shipmentid,materialid)
)
TABLESPACE pg_default;
-- ddl-end --
ALTER TABLE hack.shipped_mats OWNER TO mh_admin;
-- ddl-end --

-- object: hack.required_mats | type: TABLE --
-- DROP TABLE IF EXISTS hack.required_mats;
CREATE TABLE hack.required_mats (
	jobid bigint NOT NULL,
	materialid bigint NOT NULL,
	volume numeric,
	CONSTRAINT required_mats_pk PRIMARY KEY (jobid,materialid)
)
TABLESPACE pg_default;
-- ddl-end --
ALTER TABLE hack.required_mats OWNER TO mh_admin;
-- ddl-end --

-- object: hack.mat_usage | type: TABLE --
-- DROP TABLE IF EXISTS hack.mat_usage;
CREATE TABLE hack.mat_usage (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	regtime timestamp NOT NULL DEFAULT now(),
	sitejob bigint,
	materialid bigint,
	shipmentid bigint,
	spent bigint,
	CONSTRAINT mat_usage_pk PRIMARY KEY (id)
)
TABLESPACE pg_default;
-- ddl-end --
ALTER TABLE hack.mat_usage OWNER TO mh_admin;
-- ddl-end --

-- object: hack.supplier | type: TABLE --
-- DROP TABLE IF EXISTS hack.supplier;
CREATE TABLE hack.supplier (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	name text,
	CONSTRAINT supplier_pk PRIMARY KEY (id)
)
TABLESPACE pg_default;
-- ddl-end --
ALTER TABLE hack.supplier OWNER TO mh_admin;
-- ddl-end --

-- object: hack.shipment_files | type: TABLE --
-- DROP TABLE IF EXISTS hack.shipment_files;
CREATE TABLE hack.shipment_files (
	id bigint NOT NULL,
	shipment bigint,
	category integer,
	description text,
	CONSTRAINT shipment_files_pk PRIMARY KEY (id)
)
TABLESPACE pg_default;
-- ddl-end --
COMMENT ON COLUMN hack.shipment_files.category IS E'File category\n0 - shipment docs\n1 - certificates\n2 - misc';
-- ddl-end --
ALTER TABLE hack.shipment_files OWNER TO mh_admin;
-- ddl-end --

-- object: hack.lab_res | type: TABLE --
-- DROP TABLE IF EXISTS hack.lab_res;
CREATE TABLE hack.lab_res (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	shipmentid bigint,
	materialid bigint,
	result bigint,
	CONSTRAINT labship_pk PRIMARY KEY (id)
)
TABLESPACE pg_default;
-- ddl-end --
ALTER TABLE hack.lab_res OWNER TO mh_admin;
-- ddl-end --

-- object: hack.jobverification | type: TABLE --
-- DROP TABLE IF EXISTS hack.jobverification;
CREATE TABLE hack.jobverification (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	regtime timestamp NOT NULL DEFAULT now(),
	verifier bigint NOT NULL,
	sitejob bigint,
	result integer,
	comment text,
	geo geometry(Point, 4326),
	CONSTRAINT jobverification_pk PRIMARY KEY (id)
)
TABLESPACE pg_default;
-- ddl-end --
ALTER TABLE hack.jobverification OWNER TO mh_admin;
-- ddl-end --

-- object: hack.comment2file | type: TABLE --
-- DROP TABLE IF EXISTS hack.comment2file;
CREATE TABLE hack.comment2file (
	notice bigint NOT NULL,
	file bigint NOT NULL,
	description smallint,
	CONSTRAINT notice2file_pk PRIMARY KEY (notice,file)
)
TABLESPACE pg_default;
-- ddl-end --
ALTER TABLE hack.comment2file OWNER TO mh_admin;
-- ddl-end --

-- object: hack.comment_fix | type: TABLE --
-- DROP TABLE IF EXISTS hack.comment_fix;
CREATE TABLE hack.comment_fix (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	notice bigint,
	created_at bigint,
	comment smallint,
	creator bigint,
	state smallint,
	acceptor bigint,
	acceptor_comment smallint,
	state_changed timestamp,
	geo geometry(Point, 4326),
	CONSTRAINT notice_fix_pk PRIMARY KEY (id)
)
TABLESPACE pg_default;
-- ddl-end --
COMMENT ON COLUMN hack.comment_fix.state IS E'0 - pending\n1 - accepted\n2 - rejected';
-- ddl-end --
ALTER TABLE hack.comment_fix OWNER TO mh_admin;
-- ddl-end --

-- object: hack.commentfix2file | type: TABLE --
-- DROP TABLE IF EXISTS hack.commentfix2file;
CREATE TABLE hack.commentfix2file (
	noticefix bigint NOT NULL,
	file bigint NOT NULL,
	CONSTRAINT noticefix2file_pk PRIMARY KEY (noticefix,file)
)
TABLESPACE pg_default;
-- ddl-end --
ALTER TABLE hack.commentfix2file OWNER TO mh_admin;
-- ddl-end --

-- object: comment_type_notice_idx | type: INDEX --
-- DROP INDEX IF EXISTS hack.comment_type_notice_idx CASCADE;
CREATE INDEX comment_type_notice_idx ON hack.comments
(
	id
)
WHERE (rec_type = 0);

-- object: comment_type_warning_idx | type: INDEX --
-- DROP INDEX IF EXISTS hack.comment_type_warning_idx CASCADE;
CREATE INDEX comment_type_warning_idx ON hack.comments
(id)
WHERE (rec_type = 1);
-- ddl-end --

-- object: hack.checklist_template | type: TABLE --
-- DROP TABLE IF EXISTS hack.checklist_template;
CREATE TABLE hack.checklist_template (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	name text,
	description text,
	schedule integer,
	questions jsonb,
	CONSTRAINT checllist_template_pk PRIMARY KEY (id)
)
TABLESPACE pg_default;
-- ddl-end --
ALTER TABLE hack.checklist_template OWNER TO mh_admin;
-- ddl-end --

-- object: hack.buildsite2doc | type: TABLE --
-- DROP TABLE IF EXISTS hack.buildsite2doc;
CREATE TABLE hack.buildsite2doc (
	buildsite bigint NOT NULL,
	file bigint NOT NULL,
	type integer,
	CONSTRAINT buildsite2doc_pk PRIMARY KEY (buildsite,file)
)
TABLESPACE pg_default;
-- ddl-end --
ALTER TABLE hack.buildsite2doc OWNER TO mh_admin;
-- ddl-end --

-- object: hack.jobprogres | type: TABLE --
-- DROP TABLE IF EXISTS hack.jobprogres;
CREATE TABLE hack.jobprogres (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	linkedjob bigint,
	comment text,
	regtime timestamp NOT NULL DEFAULT now(),
	geo geometry(Point, 4326),
	volume numeric,
	CONSTRAINT jobprogres_pk PRIMARY KEY (id)
)
TABLESPACE pg_default;
-- ddl-end --
ALTER TABLE hack.jobprogres OWNER TO mh_admin;
-- ddl-end --

-- object: hack.prog2files | type: TABLE --
-- DROP TABLE IF EXISTS hack.prog2files;
CREATE TABLE hack.prog2files (
	progresrep bigint NOT NULL,
	file bigint NOT NULL,
	CONSTRAINT prog2files_pk PRIMARY KEY (progresrep,file)
)
TABLESPACE pg_default;
-- ddl-end --
ALTER TABLE hack.prog2files OWNER TO mh_admin;
-- ddl-end --

-- object: hack.lab2file | type: TABLE --
-- DROP TABLE IF EXISTS hack.lab2file;
CREATE TABLE hack.lab2file (
	labrec bigint NOT NULL,
	file bigint NOT NULL,
	CONSTRAINT lab2file_pk PRIMARY KEY (labrec,file)
)
TABLESPACE pg_default;
-- ddl-end --
ALTER TABLE hack.lab2file OWNER TO mh_admin;
-- ddl-end --

-- object: hack.shipmat2file | type: TABLE --
-- DROP TABLE IF EXISTS hack.shipmat2file;
CREATE TABLE hack.shipmat2file (
	shippedmat bigint NOT NULL,
	file bigint NOT NULL,
	materialid bigint NOT NULL,
	CONSTRAINT shipmat2file_pk PRIMARY KEY (shippedmat,file,materialid)
)
TABLESPACE pg_default;
-- ddl-end --
ALTER TABLE hack.shipmat2file OWNER TO mh_admin;
-- ddl-end --

-- object: hack.checklist_ans | type: TABLE --
-- DROP TABLE IF EXISTS hack.checklist_ans;
CREATE TABLE hack.checklist_ans (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	checklist bigint,
	author bigint,
	linkedsite bigint,
	answers jsonb,
	regtime timestamp DEFAULT now(),
	geo geometry(Point, 4326),
	CONSTRAINT checklist_ans_pk PRIMARY KEY (id)
)
TABLESPACE pg_default;
-- ddl-end --
ALTER TABLE hack.checklist_ans OWNER TO mh_admin;
-- ddl-end --

-- object: notice2author | type: CONSTRAINT --
-- ALTER TABLE hack.comments DROP CONSTRAINT IF EXISTS notice2author CASCADE;
ALTER TABLE hack.comments ADD CONSTRAINT notice2author FOREIGN KEY (author)
REFERENCES hack.users (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: notice2site | type: CONSTRAINT --
-- ALTER TABLE hack.comments DROP CONSTRAINT IF EXISTS notice2site CASCADE;
ALTER TABLE hack.comments ADD CONSTRAINT notice2site FOREIGN KEY (site)
REFERENCES hack.buildsite (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: comment2job | type: CONSTRAINT --
-- ALTER TABLE hack.comments DROP CONSTRAINT IF EXISTS comment2job CASCADE;
ALTER TABLE hack.comments ADD CONSTRAINT comment2job FOREIGN KEY (linked_job)
REFERENCES hack.sitejob (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fileuploader2user | type: CONSTRAINT --
-- ALTER TABLE hack.files DROP CONSTRAINT IF EXISTS fileuploader2user CASCADE;
ALTER TABLE hack.files ADD CONSTRAINT fileuploader2user FOREIGN KEY (uploader)
REFERENCES hack.users (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: user2site_site | type: CONSTRAINT --
-- ALTER TABLE hack.user2site DROP CONSTRAINT IF EXISTS user2site_site CASCADE;
ALTER TABLE hack.user2site ADD CONSTRAINT user2site_site FOREIGN KEY (siteid)
REFERENCES hack.buildsite (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: user2site_user | type: CONSTRAINT --
-- ALTER TABLE hack.user2site DROP CONSTRAINT IF EXISTS user2site_user CASCADE;
ALTER TABLE hack.user2site ADD CONSTRAINT user2site_user FOREIGN KEY (userid)
REFERENCES hack.users (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: job2sched | type: CONSTRAINT --
-- ALTER TABLE hack.sitejob DROP CONSTRAINT IF EXISTS job2sched CASCADE;
ALTER TABLE hack.sitejob ADD CONSTRAINT job2sched FOREIGN KEY (scheduled)
REFERENCES hack.jobschedule (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: site2sitestage | type: CONSTRAINT --
-- ALTER TABLE hack.sitestage DROP CONSTRAINT IF EXISTS site2sitestage CASCADE;
ALTER TABLE hack.sitestage ADD CONSTRAINT site2sitestage FOREIGN KEY (site)
REFERENCES hack.buildsite (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: j2s_stage | type: CONSTRAINT --
-- ALTER TABLE hack.job2stage DROP CONSTRAINT IF EXISTS j2s_stage CASCADE;
ALTER TABLE hack.job2stage ADD CONSTRAINT j2s_stage FOREIGN KEY (stageid)
REFERENCES hack.sitestage (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: j2s_job | type: CONSTRAINT --
-- ALTER TABLE hack.job2stage DROP CONSTRAINT IF EXISTS j2s_job CASCADE;
ALTER TABLE hack.job2stage ADD CONSTRAINT j2s_job FOREIGN KEY (jobid)
REFERENCES hack.sitejob (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: shift2job | type: CONSTRAINT --
-- ALTER TABLE hack.jobshift DROP CONSTRAINT IF EXISTS shift2job CASCADE;
ALTER TABLE hack.jobshift ADD CONSTRAINT shift2job FOREIGN KEY (affected_jobsch)
REFERENCES hack.jobschedule (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: shift2creator | type: CONSTRAINT --
-- ALTER TABLE hack.jobshift DROP CONSTRAINT IF EXISTS shift2creator CASCADE;
ALTER TABLE hack.jobshift ADD CONSTRAINT shift2creator FOREIGN KEY (creator)
REFERENCES hack.users (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: shift2checker | type: CONSTRAINT --
-- ALTER TABLE hack.jobshift DROP CONSTRAINT IF EXISTS shift2checker CASCADE;
ALTER TABLE hack.jobshift ADD CONSTRAINT shift2checker FOREIGN KEY (checker)
REFERENCES hack.users (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: shipment2supplier | type: CONSTRAINT --
-- ALTER TABLE hack.shipment DROP CONSTRAINT IF EXISTS shipment2supplier CASCADE;
ALTER TABLE hack.shipment ADD CONSTRAINT shipment2supplier FOREIGN KEY (supplier)
REFERENCES hack.supplier (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: shipment2acceptor | type: CONSTRAINT --
-- ALTER TABLE hack.shipment DROP CONSTRAINT IF EXISTS shipment2acceptor CASCADE;
ALTER TABLE hack.shipment ADD CONSTRAINT shipment2acceptor FOREIGN KEY (acceptor)
REFERENCES hack.users (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: shmat2shipment | type: CONSTRAINT --
-- ALTER TABLE hack.shipped_mats DROP CONSTRAINT IF EXISTS shmat2shipment CASCADE;
ALTER TABLE hack.shipped_mats ADD CONSTRAINT shmat2shipment FOREIGN KEY (shipmentid)
REFERENCES hack.shipment (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: shmat2mat | type: CONSTRAINT --
-- ALTER TABLE hack.shipped_mats DROP CONSTRAINT IF EXISTS shmat2mat CASCADE;
ALTER TABLE hack.shipped_mats ADD CONSTRAINT shmat2mat FOREIGN KEY (materialid)
REFERENCES hack.material (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: reqmat2job | type: CONSTRAINT --
-- ALTER TABLE hack.required_mats DROP CONSTRAINT IF EXISTS reqmat2job CASCADE;
ALTER TABLE hack.required_mats ADD CONSTRAINT reqmat2job FOREIGN KEY (jobid)
REFERENCES hack.sitejob (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: reqmat2mat | type: CONSTRAINT --
-- ALTER TABLE hack.required_mats DROP CONSTRAINT IF EXISTS reqmat2mat CASCADE;
ALTER TABLE hack.required_mats ADD CONSTRAINT reqmat2mat FOREIGN KEY (materialid)
REFERENCES hack.material (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: matspent2req | type: CONSTRAINT --
-- ALTER TABLE hack.mat_usage DROP CONSTRAINT IF EXISTS matspent2req CASCADE;
ALTER TABLE hack.mat_usage ADD CONSTRAINT matspent2req FOREIGN KEY (sitejob,materialid)
REFERENCES hack.required_mats (jobid,materialid) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: matspent2ship | type: CONSTRAINT --
-- ALTER TABLE hack.mat_usage DROP CONSTRAINT IF EXISTS matspent2ship CASCADE;
ALTER TABLE hack.mat_usage ADD CONSTRAINT matspent2ship FOREIGN KEY (materialid,shipmentid)
REFERENCES hack.shipped_mats (materialid,shipmentid) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: shipmentfile2file | type: CONSTRAINT --
-- ALTER TABLE hack.shipment_files DROP CONSTRAINT IF EXISTS shipmentfile2file CASCADE;
ALTER TABLE hack.shipment_files ADD CONSTRAINT shipmentfile2file FOREIGN KEY (id)
REFERENCES hack.files (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: shipmentfile2shipment | type: CONSTRAINT --
-- ALTER TABLE hack.shipment_files DROP CONSTRAINT IF EXISTS shipmentfile2shipment CASCADE;
ALTER TABLE hack.shipment_files ADD CONSTRAINT shipmentfile2shipment FOREIGN KEY (shipment)
REFERENCES hack.shipment (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: lab2ship | type: CONSTRAINT --
-- ALTER TABLE hack.lab_res DROP CONSTRAINT IF EXISTS lab2ship CASCADE;
ALTER TABLE hack.lab_res ADD CONSTRAINT lab2ship FOREIGN KEY (shipmentid,materialid)
REFERENCES hack.shipped_mats (shipmentid,materialid) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: ver2job | type: CONSTRAINT --
-- ALTER TABLE hack.jobverification DROP CONSTRAINT IF EXISTS ver2job CASCADE;
ALTER TABLE hack.jobverification ADD CONSTRAINT ver2job FOREIGN KEY (sitejob)
REFERENCES hack.sitejob (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: ver2verifier | type: CONSTRAINT --
-- ALTER TABLE hack.jobverification DROP CONSTRAINT IF EXISTS ver2verifier CASCADE;
ALTER TABLE hack.jobverification ADD CONSTRAINT ver2verifier FOREIGN KEY (verifier)
REFERENCES hack.users (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: nf2notice | type: CONSTRAINT --
-- ALTER TABLE hack.comment2file DROP CONSTRAINT IF EXISTS nf2notice CASCADE;
ALTER TABLE hack.comment2file ADD CONSTRAINT nf2notice FOREIGN KEY (notice)
REFERENCES hack.comments (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: nf2file | type: CONSTRAINT --
-- ALTER TABLE hack.comment2file DROP CONSTRAINT IF EXISTS nf2file CASCADE;
ALTER TABLE hack.comment2file ADD CONSTRAINT nf2file FOREIGN KEY (file)
REFERENCES hack.files (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fix2notice | type: CONSTRAINT --
-- ALTER TABLE hack.comment_fix DROP CONSTRAINT IF EXISTS fix2notice CASCADE;
ALTER TABLE hack.comment_fix ADD CONSTRAINT fix2notice FOREIGN KEY (notice)
REFERENCES hack.comments (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fix2author | type: CONSTRAINT --
-- ALTER TABLE hack.comment_fix DROP CONSTRAINT IF EXISTS fix2author CASCADE;
ALTER TABLE hack.comment_fix ADD CONSTRAINT fix2author FOREIGN KEY (creator)
REFERENCES hack.users (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fix2acceptor | type: CONSTRAINT --
-- ALTER TABLE hack.comment_fix DROP CONSTRAINT IF EXISTS fix2acceptor CASCADE;
ALTER TABLE hack.comment_fix ADD CONSTRAINT fix2acceptor FOREIGN KEY (acceptor)
REFERENCES hack.users (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: nfixfile2fix | type: CONSTRAINT --
-- ALTER TABLE hack.commentfix2file DROP CONSTRAINT IF EXISTS nfixfile2fix CASCADE;
ALTER TABLE hack.commentfix2file ADD CONSTRAINT nfixfile2fix FOREIGN KEY (noticefix)
REFERENCES hack.comment_fix (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: ntfixfile2file | type: CONSTRAINT --
-- ALTER TABLE hack.commentfix2file DROP CONSTRAINT IF EXISTS ntfixfile2file CASCADE;
ALTER TABLE hack.commentfix2file ADD CONSTRAINT ntfixfile2file FOREIGN KEY (file)
REFERENCES hack.files (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: sitedoc2site | type: CONSTRAINT --
-- ALTER TABLE hack.buildsite2doc DROP CONSTRAINT IF EXISTS sitedoc2site CASCADE;
ALTER TABLE hack.buildsite2doc ADD CONSTRAINT sitedoc2site FOREIGN KEY (buildsite)
REFERENCES hack.buildsite (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: sitedoc2doc | type: CONSTRAINT --
-- ALTER TABLE hack.buildsite2doc DROP CONSTRAINT IF EXISTS sitedoc2doc CASCADE;
ALTER TABLE hack.buildsite2doc ADD CONSTRAINT sitedoc2doc FOREIGN KEY (file)
REFERENCES hack.files (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: linkedjob2job | type: CONSTRAINT --
-- ALTER TABLE hack.jobprogres DROP CONSTRAINT IF EXISTS linkedjob2job CASCADE;
ALTER TABLE hack.jobprogres ADD CONSTRAINT linkedjob2job FOREIGN KEY (linkedjob)
REFERENCES hack.sitejob (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: progfile2prog | type: CONSTRAINT --
-- ALTER TABLE hack.prog2files DROP CONSTRAINT IF EXISTS progfile2prog CASCADE;
ALTER TABLE hack.prog2files ADD CONSTRAINT progfile2prog FOREIGN KEY (progresrep)
REFERENCES hack.jobprogres (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: progfile2file | type: CONSTRAINT --
-- ALTER TABLE hack.prog2files DROP CONSTRAINT IF EXISTS progfile2file CASCADE;
ALTER TABLE hack.prog2files ADD CONSTRAINT progfile2file FOREIGN KEY (file)
REFERENCES hack.files (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: labfile2labrec | type: CONSTRAINT --
-- ALTER TABLE hack.lab2file DROP CONSTRAINT IF EXISTS labfile2labrec CASCADE;
ALTER TABLE hack.lab2file ADD CONSTRAINT labfile2labrec FOREIGN KEY (labrec)
REFERENCES hack.lab_res (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: labfile2file | type: CONSTRAINT --
-- ALTER TABLE hack.lab2file DROP CONSTRAINT IF EXISTS labfile2file CASCADE;
ALTER TABLE hack.lab2file ADD CONSTRAINT labfile2file FOREIGN KEY (file)
REFERENCES hack.files (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: shipmatfile2mat | type: CONSTRAINT --
-- ALTER TABLE hack.shipmat2file DROP CONSTRAINT IF EXISTS shipmatfile2mat CASCADE;
ALTER TABLE hack.shipmat2file ADD CONSTRAINT shipmatfile2mat FOREIGN KEY (shippedmat,materialid)
REFERENCES hack.shipped_mats (shipmentid,materialid) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: shipmatfile2file | type: CONSTRAINT --
-- ALTER TABLE hack.shipmat2file DROP CONSTRAINT IF EXISTS shipmatfile2file CASCADE;
ALTER TABLE hack.shipmat2file ADD CONSTRAINT shipmatfile2file FOREIGN KEY (file)
REFERENCES hack.files (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: ans2check | type: CONSTRAINT --
-- ALTER TABLE hack.checklist_ans DROP CONSTRAINT IF EXISTS ans2check CASCADE;
ALTER TABLE hack.checklist_ans ADD CONSTRAINT ans2check FOREIGN KEY (checklist)
REFERENCES hack.checklist_template (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: ans2site | type: CONSTRAINT --
-- ALTER TABLE hack.checklist_ans DROP CONSTRAINT IF EXISTS ans2site CASCADE;
ALTER TABLE hack.checklist_ans ADD CONSTRAINT ans2site FOREIGN KEY (linkedsite)
REFERENCES hack.buildsite (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: ans2author | type: CONSTRAINT --
-- ALTER TABLE hack.checklist_ans DROP CONSTRAINT IF EXISTS ans2author CASCADE;
ALTER TABLE hack.checklist_ans ADD CONSTRAINT ans2author FOREIGN KEY (author)
REFERENCES hack.users (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --


