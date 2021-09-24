import urllib.request, urllib.parse, urllib.error
import sys
import os
import gzip
from datetime import datetime
import logging
import importlib
importlib.reload(sys)  # Reload does the trick!
from src.models import Dbentity, Locusdbentity, LocusAlias, Source, Filedbentity, Edam
from src.helpers import upload_file
from scripts.loading.database_session import get_session

__author__ = 'sweng66'

logging.basicConfig(format='%(message)s')
log = logging.getLogger()
log.setLevel(logging.INFO)

CREATED_BY = os.environ['DEFAULT_USER']

alias_type_src_list = [("UniProtKB ID", "UniProtKB"),
                       ("UniParc ID", "UniParc"),
                       ("DNA accession ID", "GenBank/EMBL/DDBJ"),
                       ("Protein version ID", "GenBank/EMBL/DDBJ"),
                       ("TPA protein version ID", "NCBI"),
                       ("RefSeq protein version ID", "NCBI"),
                       ("RefSeq nucleotide version ID", "NCBI"),
                       ("Gene ID", "BioGRID"),
                       ("Gene ID", "DIP"),
                       ("Gene ID", "NCBI")]

# "PDB":             ("PDB ID", "PDB"),

ID_type_mapping = {"UniParc":         ("UniParc ID", "UniParc"),
                   "EMBL":            ("DNA accession ID", "GenBank/EMBL/DDBJ"),
                   "EMBL-CDS":        ("Protein version ID", "GenBank/EMBL/DDBJ"),
                   "EMBL-CDS-TPA":    ("TPA protein version ID", "NCBI"),
                   "RefSeq":          ("RefSeq protein version ID", "NCBI"),
                   "RefSeq_NT":       ("RefSeq nucleotide version ID", "NCBI"),
                   "BioGrid":         ("Gene ID", "BioGRID"),
                   "DIP":             ("Gene ID", "DIP"),
                   "GeneID":          ("Gene ID", "NCBI") }

log_file = "scripts/loading/dbxref/logs/update_dbxref.log"

ADDED = 0
DELETED = 0
UPDATED = 0

def update_data(infile):

    nex_session = get_session()

    fw = open(log_file,"w")

    edam_to_id = dict([(x.format_name, x.edam_id) for x in nex_session.query(Edam).all()])
    locus_id_to_name = dict([(x.dbentity_id, x.systematic_name) for x in nex_session.query(Locusdbentity).all()])
    
    id_to_source = {}
    source_to_id = {}

    log.info(str(datetime.now()))
    log.info("Getting data from the database...")

    for x in nex_session.query(Source).all():
        id_to_source[x.source_id] = x.display_name
        source_to_id[x.display_name] = x.source_id

    sgdid2tpa = sgdid_to_tpa_mapping()
    
    locus_id_to_sgdid = {}
    sgdid_to_locus_id = {}
    
    for x in nex_session.query(Dbentity).filter_by(subclass="LOCUS").all():
        locus_id_to_sgdid[x.dbentity_id] = x.sgdid
        sgdid_to_locus_id[x.sgdid] = x.dbentity_id
    
        
    log.info("Reading data from uniprot data file...")

    [sgdid_to_uniprot_id, uniprot_id_to_sgdid_list, key_to_ids] = read_uniprot_file(infile, source_to_id)

    all_aliases = nex_session.query(LocusAlias).all()

    nex_session.close()
    nex_session = get_session()

    key_to_ids_DB = {}
    
    log.info("Updating the data in the database...")

    for x in all_aliases:

        ## ignore all NISS genes for now
        systematic_name = locus_id_to_name[x.locus_id]
        if systematic_name in ['YAR070W-A', 'YAR069W-A', 'ENA6', 'IMI1', 'KHR1', 'MPR1', 'RTM1']:
            continue

        this_key = (x.alias_type, id_to_source[x.source_id])
        if this_key not in alias_type_src_list:
            continue

        sgdid = locus_id_to_sgdid[x.locus_id]
        uniprot_id = sgdid_to_uniprot_id.get(sgdid)
        if uniprot_id is None:
            continue

        if x.alias_type == "UniProtKB ID":
            if x.display_name != uniprot_id:
                # print "NEW:", uniprot_id
                # print "OLD:", x.display_name
                update_uniprot_id(nex_session, fw, x.locus_id, 
                                  x.alias_type, uniprot_id)
            continue

        key = (sgdid, x.alias_type, x.source_id)
        id_list = []
        if key in key_to_ids_DB:
            id_list = key_to_ids_DB[key]
        id_list.append(x.display_name)
        key_to_ids_DB[key] = id_list

    for this_key in key_to_ids:
        (uniprot_id, alias_type, source_id) = this_key
        sgdid_list = uniprot_id_to_sgdid_list.get(uniprot_id)
        if sgdid_list is None:
            continue
        for sgdid in sgdid_list:
            key = (sgdid, alias_type, source_id)
            if key in key_to_ids_DB:
                update_aliases(nex_session, fw, key, key_to_ids[this_key], 
                               key_to_ids_DB[key], sgdid_to_locus_id, id_to_source,
			       sgdid2tpa)
                del key_to_ids_DB[key]
            else:
                insert_aliases(nex_session, fw, key, key_to_ids[this_key],
                               sgdid_to_locus_id, id_to_source, sgdid2tpa)

    ## delete the ones that are not in the current uniprot file
    for key in key_to_ids_DB:
        delete_aliases(nex_session, fw, key, sgdid_to_locus_id)
    
    # nex_session.rollback()
    nex_session.commit()

    # update_database_load_file_to_s3(nex_session, infile, source_to_id, edam_to_id)

    log.info("Loading summary:")
    log.info("\tAdded: " + str(ADDED))
    log.info("\tUpdated: " + str(UPDATED))
    log.info("\tDeleted: " + str(DELETED))
    log.info(str(datetime.now()))
    log.info("Done!")

def delete_aliases(nex_session, fw, key, sgdid_to_locus_id):

    (sgdid, alias_type, source_id) = key

    locus_id = sgdid_to_locus_id.get(sgdid)
    if locus_id is None:
        return
    nex_session.query(LocusAlias).filter_by(locus_id=locus_id, alias_type=alias_type, source_id=source_id).delete()
    global DELETED
    DELETED = DELETED + 1

def insert_aliases(nex_session, fw, key, ids, sgdid_to_locus_id, id_to_source, sgdid2tpa):
    
    (sgdid, alias_type, source_id) = key
    
    locus_id = sgdid_to_locus_id.get(sgdid)
    if locus_id is None:
        return
    for ID in ids:
        if alias_type == 'TPA protein version ID' and sgdid in sgdid2tpa and sgdid2tpa[sgdid] != ID:
            continue
            # ID = sgdid2tpa[sgdid]
        insert_alias(nex_session, fw, locus_id, alias_type, id_to_source[source_id], source_id, ID)
        global ADDED
        ADDED = ADDED + 1

def update_aliases(nex_session, fw, key, ids_new, ids_DB, sgdid_to_locus_id, id_to_source, sgdid2tpa):

    (sgdid, alias_type, source_id) = key
    ids = []
    for id in ids_new:
        if alias_type == 'TPA protein version ID' and sgdid in sgdid2tpa and id != sgdid2tpa[sgdid]:
            continue
        ids.append(id)
    if set(ids_DB) == set(ids):
        return
    
    locus_id = sgdid_to_locus_id.get(sgdid)
    if locus_id is None:
        return
    for ID in ids:
        # if alias_type == 'TPA protein version ID' and sgdid in sgdid2tpa and sgdid2tpa[sgdid] != ID:
        #    continue
        if ID in ids_DB:
            ids_DB.remove(ID)
            continue
        insert_alias(nex_session, fw, locus_id, alias_type, 
                     id_to_source[source_id], source_id, ID)
        global ADDED
        ADDED = ADDED + 1

    for ID in ids_DB:
        delete_alias(nex_session, fw, locus_id, alias_type, ID)
        global DELETED
        DELETED = DELETED + 1

def delete_alias(nex_session, fw, locus_id, alias_type, ID):
    
    nex_session.query(LocusAlias).filter_by(locus_id=locus_id, alias_type=alias_type, display_name=ID).delete()
    
    fw.write("Delete "+alias_type+" "+ID+"\n")
    
def insert_alias(nex_session, fw, locus_id, alias_type, source, source_id, ID):
    
    obj_url = get_url(alias_type, ID, source)

    x = LocusAlias(display_name = ID,
                   obj_url = obj_url,
                   source_id = source_id,
                   locus_id = locus_id,
                   has_external_id_section = "1",
                   alias_type = alias_type,
                   created_by = CREATED_BY)
    nex_session.add(x)

    fw.write("Insert a new "+alias_type+": "+ID+"\n")
    
def update_uniprot_id(nex_session, fw, locus_id, alias_type, ID):

    nex_session.query(LocusAlias).filter_by(locus_id=locus_id, alias_type=alias_type).update({"display_name": ID, "obj_url": "http://www.uniprot.org/uniprot/"+ID})
        
    fw.write("Update "+alias_type+" to "+ID+" for locus_id="+str(locus_id)+"\n")
    global UPDATED
    UPDATED = UPDATED + 1

def get_url(alias_type, ID, source):
    
    if source == "DIP" and alias_type == "Gene ID":
        return "http://dip.doe-mbi.ucla.edu/dip/Browse.cgi?PK="+ID+"&D=1"
    if source == "NCBI" and alias_type == "Gene ID":
        return "http://www.ncbi.nlm.nih.gov/gene/"+ID
    if source == "BioGRID" and alias_type == "Gene ID":
        return "https://thebiogrid.org/"+ID+"/summary/saccharomyces-cerevisiae"
    # if source == "PDB" and alias_type == "PDB ID":
    #    return "http://www.rcsb.org/pdb/explore/explore.do?structureId="+ID
    if source == "NCBI" and alias_type == "RefSeq protein version ID":
        return "https://www.ncbi.nlm.nih.gov/protein/"+ID
    if source == "NCBI" and alias_type == "RefSeq nucleotide version ID":
        return "https://www.ncbi.nlm.nih.gov/nuccore/" + ID
    if source == "NCBI" and alias_type == "TPA protein version ID":
        return "https://www.ncbi.nlm.nih.gov/protein/" + ID
    if source == "GenBank/EMBL/DDBJ" and alias_type == "Protein version ID":
        return "https://www.ncbi.nlm.nih.gov/protein/" + ID
    if source == "GenBank/EMBL/DDBJ" and alias_type == "DNA accession ID":
        return "https://www.ncbi.nlm.nih.gov/nuccore/" + ID
    if source == "UniParc" and alias_type == "UniParc ID":
        return "http://www.uniprot.org/uniparc/"+ID
    
    print("Unknown source & alias_type:", source, alias_type)    
    return ""


def update_database_load_file_to_s3(nex_session, data_file, source_to_id, edam_to_id):

    local_file = open(data_file, mode='rb')

    import hashlib
    dx_md5sum = hashlib.md5(data_file.encode()).hexdigest()
    dx_row = nex_session.query(Filedbentity).filter_by(md5sum = dx_md5sum).one_or_none()

    if dx_row is not None:
        return

    log.info("Uploading the file to S3...")

    nex_session.query(Dbentity).filter_by(display_name=data_file, dbentity_status='Active').update({"dbentity_status": 'Archived'})
    nex_session.commit()

    data_id = edam_to_id.get('EDAM:2872')   ## data:2872 ID list 
    topic_id = edam_to_id.get('EDAM:3345')  ## topic:3345 Data identity and mapping
    format_id = edam_to_id.get('EDAM:3475') ## format:3475 TSV

    from sqlalchemy import create_engine
    from src.models import DBSession
    engine = create_engine(os.environ['NEX2_URI'], pool_recycle=3600)
    DBSession.configure(bind=engine)

    upload_file(CREATED_BY, local_file,
                filename=data_file,
                file_extension='gz',
                description='UniProt ID mapping file',
                display_name=data_file,
                data_id=data_id,
                format_id=format_id,
                topic_id=topic_id,
                status='Active',
                is_public='0',
                is_in_spell='0',
                is_in_browser='0',
                file_date=datetime.now(),
                source_id=source_to_id['SGD'],
                md5sum=dx_md5sum)

    
def read_uniprot_file(infile, source_to_id):
    
    f = gzip.open(infile, mode='rt')    
    sgdid_to_uniprot_id = {}
    uniprot_id_to_sgdid_list = {}
    key_to_ids = {}
    for line in f:
        pieces = line.strip().split("\t")
        uniprot_id = pieces[0].strip()
        type = pieces[1].strip()
        ID = pieces[2].strip()
        if ID == '-' or ID == '_' or ID == None:
            continue
        if type.startswith('EMBL') and ID.startswith('BK'):
            continue
        if "-" in uniprot_id and len(uniprot_id) > 6:
            uniprot_id = uniprot_id[0:6]
        if type == "SGD":
            sgdid_to_uniprot_id[ID] = uniprot_id
            sgdid_list = []
            if uniprot_id in uniprot_id_to_sgdid_list:
                sgdid_list = uniprot_id_to_sgdid_list[uniprot_id]
            sgdid_list.append(ID)
            uniprot_id_to_sgdid_list[uniprot_id] = sgdid_list
            # print uniprot_id, ID
        if type == 'DIP':
            ## example ID = "DIP-310N"
            ID = ID.replace("DIP-", "").replace("N", "")
        if type == "EMBL-CDS" and ID.startswith("DAA"):
            type = "EMBL-CDS-TPA"
        if type in ID_type_mapping:
            (db_type, src) = ID_type_mapping[type]
            key = (uniprot_id, db_type, source_to_id.get(src)) 
            id_list = []
            if key in key_to_ids:
                id_list = key_to_ids[key] 
            if ID not in id_list:
                id_list.append(ID)
            key_to_ids[key] = id_list        
    f.close()

    ### adding TPA protein ID for YPR099C (its UniProt ID: O13548
    key = ('O13548', 'TPA protein version ID', source_to_id.get('NCBI'))
    if key not in key_to_ids:
        key_to_ids[key] = ['DAC85312.1']
        
    return [sgdid_to_uniprot_id, uniprot_id_to_sgdid_list, key_to_ids] 


def sgdid_to_tpa_mapping():

    return { 'S000000214' : 'DAA07131.1', # HHT1          
             'S000004976' : 'DAA10514.1', # HHT2          
             'S000000213' : 'DAA07130.1', # HHF1          
             'S000004975' : 'DAA10515.1', # HHF2          
             'S000000322' : 'DAA07236.1', # TEF2          
             'S000006284' : 'DAA11498.1', # TEF1          
             'S000003674' : 'DAA08662.1', # TIF2          
             'S000001767' : 'DAA09210.1', # TIF1          
             'S000002793' : 'DAA12229.1', # EFT2          
             'S000005659' : 'DAA10907.1', # EFT1
             'S000001535' : 'DAA09105.1', # ASK1 ; it has a TPA_exp
             'S000004205' : 'DAA06809.1', # CDC123 ; it has a TPA_exp
             'S000001157' : 'DAA06809.1', # DMA1 ; it has a TPA_exp
             'S000005060' : 'DAA10432.1',
             'S000004205' : 'DAA09532.1' }

if __name__ == '__main__':

    url_path = 'ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/idmapping/by_organism/'
    uniprot_file = 'YEAST_559292_idmapping.dat.gz'
    urllib.request.urlretrieve(url_path + uniprot_file, uniprot_file)

    update_data(uniprot_file)




