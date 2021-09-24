-- Generated by Ora2Pg, the Oracle database Schema converter, version 17.4
-- Copyright 2000-2016 Gilles DAROLD. All rights reserved.
-- DATASOURCE: dbi:Oracle:host=sgd-nex2-db.stanford.edu;sid=SGD

SET client_encoding TO 'UTF8';

\set ON_ERROR_STOP ON

-- Curation tables

DROP TABLE IF EXISTS nex.curation_locus CASCADE;
CREATE TABLE nex.curation_locus (
	curation_id bigint NOT NULL DEFAULT nextval('curation_seq'),
	locus_id bigint NOT NULL,
	source_id bigint NOT NULL,
	curation_tag varchar(40) NOT NULL,
	date_created timestamp NOT NULL DEFAULT LOCALTIMESTAMP,
	created_by varchar(12) NOT NULL,
    curator_comment varchar(2000),
    json text,
	CONSTRAINT curationlocus_pk PRIMARY KEY (curation_id)
) ;
COMMENT ON TABLE nex.curation_locus IS 'Tags and notes associated with locus curation.';
COMMENT ON COLUMN nex.curation_locus.curator_comment IS 'Comment or note.';
COMMENT ON COLUMN nex.curation_locus.locus_id IS 'FK to LOCUSDBENTITY.DBENTITY_ID.';
COMMENT ON COLUMN nex.curation_locus.curation_id IS 'Unique identifier (serial number).';
COMMENT ON COLUMN nex.curation_locus.source_id IS 'FK to SOURCE.SOURCE_ID.';
COMMENT ON COLUMN nex.curation_locus.created_by IS 'Username of the person who entered the record into the database.';
COMMENT ON COLUMN nex.curation_locus.date_created IS 'Date the record was entered into the database.';
COMMENT ON COLUMN nex.curation_locus.curation_tag IS 'Type of curation tag (GO needs review, Headline reviewed, Paragraph not needed, Phenotype uncuratable).';
COMMENT ON COLUMN nex.curation_locus.json IS 'JSON object of locus curation data.'; 
CREATE UNIQUE INDEX curationlocus_uk_index on nex.curation_locus (locus_id,curation_tag);
ALTER TABLE nex.curation_locus ADD CONSTRAINT curationlocus_tag_ck CHECK (CURATION_TAG IN ('GO needs review','Headline reviewed','Paragraph not needed','Phenotype uncuratable'));
CREATE INDEX curationlocus_source_fk_index ON nex.curation_locus (source_id);

DROP TABLE IF EXISTS nex.curation_reference CASCADE;
CREATE TABLE nex.curation_reference (
    curation_id bigint NOT NULL DEFAULT nextval('curation_seq'),
    reference_id bigint NOT NULL,
    source_id bigint NOT NULL,
    dbentity_id bigint,
    curation_tag varchar(40) NOT NULL,
    date_created timestamp NOT NULL DEFAULT LOCALTIMESTAMP,
    created_by varchar(12) NOT NULL,
    curator_comment varchar(2000),
    json text,
    CONSTRAINT curationreference_pk PRIMARY KEY (curation_id)
) ;
COMMENT ON TABLE nex.curation_reference IS 'Tags and notes associated with reference curation.';
COMMENT ON COLUMN nex.curation_reference.curator_comment IS 'Comment or note.';
COMMENT ON COLUMN nex.curation_reference.reference_id IS 'FK to REFERENCEDBENTITY.DBENTITY_ID.';
COMMENT ON COLUMN nex.curation_reference.dbentity_id IS 'FK to DBENTITY.DBENTITY_ID.';
COMMENT ON COLUMN nex.curation_reference.curation_id IS 'Unique identifier (serial number).';
COMMENT ON COLUMN nex.curation_reference.source_id IS 'FK to SOURCE.SOURCE_ID.';
COMMENT ON COLUMN nex.curation_reference.created_by IS 'Username of the person who entered the record into the database.';
COMMENT ON COLUMN nex.curation_reference.date_created IS 'Date the record was entered into the database.';
COMMENT ON COLUMN nex.curation_reference.curation_tag IS 'Type of curation tag (Classical phenotype information,Delay,Fast Track,GO information,Gene model,Headline needs review,Headline information,High Priority,Homology/Disease,HTP phenotype,Non-phenotype HTP,Not yet curated,Paragraph needs review,Pathways,Phenotype needs review,Post-translational modifications,Regulation information).';
COMMENT ON COLUMN nex.curation_reference.json IS 'JSON object of reference curation data.';
CREATE UNIQUE INDEX curationreference_uk_index on nex.curation_reference (reference_id,curation_tag,coalesce(dbentity_id,0));
ALTER TABLE nex.curation_reference ADD CONSTRAINT curationreference_tag_ck CHECK (CURATION_TAG IN ('Classical phenotype information','Delay','Fast Track','GO information','Gene model','Headline needs review','Headline information','High Priority','Homology/Disease','HTP phenotype','Non-phenotype HTP','Not yet curated','Paragraph needs review','Pathways','Phenotype needs review','Post-translational modifications','Regulation information'));
CREATE INDEX curationreference_dbentity_fk_index ON nex.curation_reference (dbentity_id);
CREATE INDEX curationreference_source_fk_index ON nex.curation_reference (source_id);

DROP TABLE IF EXISTS nex.authorresponse CASCADE;
CREATE TABLE nex.authorresponse (
	curation_id bigint NOT NULL DEFAULT nextval('curation_seq'),
	reference_id bigint NOT NULL,
	source_id bigint NOT NULL,
	colleague_id bigint,
	author_email varchar(100) NOT NULL,
	has_novel_research boolean NOT NULL,
	has_large_scale_data boolean NOT NULL,
	has_fast_track_tag boolean NOT NULL,
	curator_checked_datasets boolean NOT NULL,
	curator_checked_genelist boolean NOT NULL,
	no_action_required boolean NOT NULL,
	research_results text,
	gene_list varchar(4000),
	dataset_description varchar(4000),
	other_description varchar(4000),
	date_created timestamp NOT NULL DEFAULT LOCALTIMESTAMP,
	created_by varchar(12) NOT NULL,
	CONSTRAINT authorresponse_pk PRIMARY KEY (curation_id)
) ;
COMMENT ON TABLE nex.authorresponse IS 'Replies from the Author Reponse System.';
COMMENT ON COLUMN nex.authorresponse.has_large_scale_data IS 'Whether there is large scale data in the paper.';
COMMENT ON COLUMN nex.authorresponse.created_by IS 'Username of the person who entered the record into the database.';
COMMENT ON COLUMN nex.authorresponse.no_action_required IS 'Whether any further action is needed.';
COMMENT ON COLUMN nex.authorresponse.gene_list IS 'List of gene names contained in the paper submitted by the author.';
COMMENT ON COLUMN nex.authorresponse.date_created IS 'Date the record was entered into the database.';
COMMENT ON COLUMN nex.authorresponse.has_novel_research IS 'Whether there is novel research in the paper.';
COMMENT ON COLUMN nex.authorresponse.has_fast_track_tag IS 'Whether a fast track tag has been attached to this paper.';
COMMENT ON COLUMN nex.authorresponse.curation_id IS 'Unique identifier (serial number).';
COMMENT ON COLUMN nex.authorresponse.author_email IS 'Email address of the author.';
COMMENT ON COLUMN nex.authorresponse.research_results IS 'Research results submitted by the author.';
COMMENT ON COLUMN nex.authorresponse.dataset_description IS 'Description of the dataset submitted by the author.';
COMMENT ON COLUMN nex.authorresponse.source_id IS 'FK to SOURCE.SOURCE_ID.';
COMMENT ON COLUMN nex.authorresponse.curator_checked_datasets IS 'Whether a curator has checked the datasets in the paper.';
COMMENT ON COLUMN nex.authorresponse.colleague_id IS 'FK to COLLEAGUE.COLLEAGUE_ID.';
COMMENT ON COLUMN nex.authorresponse.other_description IS 'Any other description submitted by the author.';
COMMENT ON COLUMN nex.authorresponse.reference_id IS 'FK to REFERENCEDBENTITY.DBENTITY_ID.';
COMMENT ON COLUMN nex.authorresponse.curator_checked_genelist IS 'Whether a curator has checked the submitted gene list.';
ALTER TABLE nex.authorresponse ADD CONSTRAINT authorresponse_uk UNIQUE (reference_id);
CREATE INDEX authorresponse_coll_fk_index ON nex.authorresponse (colleague_id);
CREATE INDEX authorresponse_source_fk_index ON nex.authorresponse (source_id);

DROP TABLE IF EXISTS nex.referencetriage CASCADE;
CREATE TABLE nex.referencetriage (
	curation_id bigint NOT NULL DEFAULT nextval('curation_seq'),
	pmid bigint NOT NULL,
	citation varchar(500) NOT NULL,
	fulltext_url varchar(500),
    abstract_genes varchar(500),
	abstract text,
    json text,
	date_created timestamp NOT NULL DEFAULT LOCALTIMESTAMP,
	CONSTRAINT referencetriage_pk PRIMARY KEY (curation_id)
) ;
COMMENT ON TABLE nex.referencetriage IS 'Papers obtained via the reference triage system.';
COMMENT ON COLUMN nex.referencetriage.abstract IS 'Paper abstract.';
COMMENT ON COLUMN nex.referencetriage.fulltext_url IS 'URL to the fulltext of the paper.';
COMMENT ON COLUMN nex.referencetriage.abstract_genes IS 'Comma separated list of gene or systematic names identified in the abstract.';
COMMENT ON COLUMN nex.referencetriage.date_created IS 'Date the record was entered into the database.';
COMMENT ON COLUMN nex.referencetriage.citation IS 'Full citation of the paper.';
COMMENT ON COLUMN nex.referencetriage.curation_id IS 'Unique identifier (serial number).';
COMMENT ON COLUMN nex.referencetriage.pmid IS 'Pubmed identifier for the paper.';
COMMENT ON COLUMN nex.referencetriage.json IS 'JSON object of the reference data.';
ALTER TABLE nex.referencetriage ADD CONSTRAINT referencetriage_uk UNIQUE (pmid);

DROP TABLE IF EXISTS nex.colleaguetriage CASCADE;
CREATE TABLE nex.colleaguetriage (
	curation_id bigint NOT NULL DEFAULT nextval('curation_seq'),
	triage_type varchar(10) NOT NULL,
    colleague_id bigint,
    json text NOT NULL,
    curator_comment varchar(500),
    date_created timestamp NOT NULL DEFAULT LOCALTIMESTAMP,
	CONSTRAINT colleaguetriage_pk PRIMARY KEY (curation_id)
) ;
COMMENT ON TABLE nex.colleaguetriage IS 'New and update colleague submissions.';
COMMENT ON COLUMN nex.colleaguetriage.colleague_id IS 'FK to COLLEAGUE.COLLEAGUE_ID.';
COMMENT ON COLUMN nex.colleaguetriage.triage_type IS 'Type of colleague submission (New, Update, Stalled).';
COMMENT ON COLUMN nex.colleaguetriage.json IS 'JSON object of the colleague data.';
COMMENT ON COLUMN nex.colleaguetriage.date_created IS 'Date the record was entered into the database.';
COMMENT ON COLUMN nex.colleaguetriage.curation_id IS 'Unique identifier (serial number).';
COMMENT ON COLUMN nex.colleaguetriage.curator_comment IS 'Notes or comments about this colleague entry by the curators.';
ALTER TABLE nex.colleaguetriage ADD CONSTRAINT colleagetriage_type_ck CHECK (TRIAGE_TYPE IN ('New', 'Update', 'Stalled'));
CREATE INDEX colleaguetriage_coll_fk_index ON nex.colleaguetriage (colleague_id);

DROP TABLE IF EXISTS nex.reservednametriage CASCADE;
CREATE TABLE nex.reservednametriage (
    curation_id bigint NOT NULL DEFAULT nextval('curation_seq'),
    proposed_gene_name varchar(20) NOT NULL,
    colleague_id bigint NOT NULL,
    json text NOT NULL,
    date_created timestamp NOT NULL DEFAULT LOCALTIMESTAMP,
    CONSTRAINT reservednametriage_pk PRIMARY KEY (curation_id)
) ;
COMMENT ON TABLE nex.reservednametriage IS 'New gene name submissions.';
COMMENT ON COLUMN nex.reservednametriage.colleague_id IS 'FK to COLLEAGUE.COLLEAGUE_ID.';
COMMENT ON COLUMN nex.reservednametriage.proposed_gene_name IS 'Proposed gene name.';
COMMENT ON COLUMN nex.reservednametriage.json IS 'JSON object of the reserved name data.';
COMMENT ON COLUMN nex.reservednametriage.date_created IS 'Date the record was entered into the database.';
COMMENT ON COLUMN nex.reservednametriage.curation_id IS 'Unique identifier (serial number).';
CREATE INDEX reservednametriage_coll_fk_index ON nex.reservednametriage (colleague_id);

DROP TABLE IF EXISTS nex.curatoractivity CASCADE;
CREATE TABLE nex.curatoractivity (
    curation_id bigint NOT NULL DEFAULT nextval('curation_seq'),
    display_name varchar(500) NOT NULL,
    obj_url varchar(500) NOT NULL,
    activity_category varchar(40) NOT NULL,
    dbentity_id bigint,
    message varchar(1000) NOT NULL,
    json text NOT NULL,
    date_created timestamp NOT NULL DEFAULT LOCALTIMESTAMP,
    created_by varchar(12) NOT NULL,
    CONSTRAINT curatoractivity_pk PRIMARY KEY (curation_id)
) ;
COMMENT ON TABLE nex.curatoractivity IS 'Curator activities in the curator interfaces.';
COMMENT ON COLUMN nex.curatoractivity.curation_id IS 'Unique identifier (serial number).';
COMMENT ON COLUMN nex.curatoractivity.display_name IS 'Public display name.';
COMMENT ON COLUMN nex.curatoractivity.obj_url IS 'URL of the object (relative for local links or complete for external links).';
COMMENT ON COLUMN nex.curatoractivity.activity_category IS 'Type of curator activity.';
COMMENT ON COLUMN nex.curatoractivity.dbentity_id IS 'FK to DBENTITY.DBENTITY_ID.';
COMMENT ON COLUMN nex.curatoractivity.message IS 'Description of the curator activity.';
COMMENT ON COLUMN nex.curatoractivity.json IS 'JSON object.';
COMMENT ON COLUMN nex.curatoractivity.date_created IS 'Date the record was entered into the database.';
COMMENT ON COLUMN nex.curatoractivity.created_by IS 'Username of the person who entered the record into the database.';
CREATE INDEX curatoractivity_dbentity_fk_index ON nex.dbentity (dbentity_id);