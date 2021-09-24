from datetime import datetime
import json
import csv
import sys
sys.path.insert(0, '../../../src/')
from models import Locussummary, LocussummaryReference, Source
sys.path.insert(0, '../')
from database_session import get_dev_session as get_session
from config import CREATED_BY, EMAIL
from util import sendmail
                             
__author__ = 'sweng66'

'''
* Retrieve the summary data and put it into dictionary (memory)
* Read in the summary text for each gene from the upload file and compare the 
  text with the info in the memory.
  * The summary for this gene for the given type (eg, Regulation or Phenotype) 
    is not in the database,
       * insert the summay text into the LOCUSSUMMARY table
       * insert any associated reference(s) into LOCUSSUMMARY_REFERENCE table 
         (eg, for regulation summaries)
  * The summary for this gene for the given type is in the database.
       * if the summary text is updated, update the LOCUSSUMMARY.text/html; 
         otherwise noneed todo anything to theLOCUSSUMMARY table
       * check to see if there is any referenceupdate, if yes, updatethe 
         LOCUSSUMMARY_REFERENCE table
'''  

def load_summaries(nex_session, summary_file_reader, summary_type=None):
    
    if summary_type is None:
        summary_type = "Phenotype_Regulation"

    log_file = "loading/logs/" + summary_type + "_summary_loading.log"

    fw = open(log_file, "w")
    
    fw.write(str(datetime.now()) + "\n")
    fw.write("reading data from summary_file_reader...\n")
    
    data_for_json = []

    data = read_summary_file(nex_session, fw, summary_type, summary_file_reader, log_file, data_for_json)

    fw.write(str(datetime.now()) + "\n")
    fw.write("retriveing data from database and store the data in dictionary...\n")
    
    key_to_summary = dict([((x.locus_id, x.summary_type, x.summary_order), x) for x in nex_session.query(Locussummary).all()])
    key_to_summaryref = dict([((x.summary_id, x.reference_id, x.reference_order), x) for x in nex_session.query(LocussummaryReference).all()])
    
    source_to_id = dict([(x.display_name, x.source_id) for x in nex_session.query(Source).all()])
    source_id = source_to_id.get('SGD')

    summary_id_to_references = {}
    for x in nex_session.query(LocussummaryReference).all():
        references = []
        if x.summary_id in summary_id_to_references:
            references = summary_id_to_references[x.summary_id]
        references.append(x)
        summary_id_to_references[x.summary_id] = references

    load_summary_holder = { "summary_added": 0,
                            "summary_updated": 0,
                            "summary_reference_added": 0 }

    fw.write(str(datetime.now()) + "\n")
    fw.write("updating the database...\n")

    for x in data:
        key = (x['locus_id'], x['summary_type'], x['summary_order'])
        name = None
        dbentity = x.get('dbentity')
        if dbentity is not None:
            name = dbentity.gene_name
            if name is None:
                name = dbentity.systematic_name
        summary_id = None
        summary_updated = 0
        reference_updated = 0
        if key in key_to_summary:
            if x['text'] != key_to_summary[key].text.strip():
                fw.write("OLD:" + key_to_summary[key].text + ":\n")
                fw.write("NEW:" + x['text'] + ":\n")
                nex_session.query(Locussummary).filter_by(summary_id=key_to_summary[key].summary_id).update({'text': x['text'], 'html': x['html']})
                load_summary_holder['summary_updated'] = load_summary_holder['summary_updated'] + 1
                summary_updated = 1
            else:
                fw.write("SUMMARY is in DB\n")
            summary_id = key_to_summary[key].summary_id
            reference_updated = update_references(nex_session,
                                                  fw,
                                                  load_summary_holder,
                                                  source_id, 
                                                  summary_id, 
                                                  summary_id_to_references.get(summary_id),
                                                  x['references'])
            if name is not None:
                tag = None
                if summary_updated and reference_updated:
                    tag = "summary & references updated"
                elif summary_updated:
                    tag = "summary updated"
                elif reference_updated:
                    tag = "reference(s) updated"
                if tag is not None:
                    data_for_json.append({'category': 'locus',
                                          'name': name,
                                          'href': 'http://www.yeastgenome.org/locus/' + dbentity.sgdid,
                                          'type': x['summary_type'] + ' summary',
                                          'value': x['text'],
                                          'tag': tag})
        else:
            summary_id = insert_summary(nex_session, fw, load_summary_holder, source_id, x)
            if x.get('references'):
                for y in x['references']:
                    insert_summary_reference(nex_session, fw, load_summary_holder, source_id, summary_id, y)
            if name is not None:
                data_for_json.append({'category': 'locus',
                                      'name': name,
                                      'href': 'http://www.yeastgenome.org/locus/' + dbentity.sgdid,
                                      'type': x['summary_type'] + ' summary',
                                      'value': x['text'],
                                      'tag': "summary added"})
                    
    nex_session.commit()
    nex_session.close()
 
    fw.write(str(datetime.now()) + "\n")
    fw.write("writing summary and sending an email to curators...\n")

    write_summary_and_send_email(load_summary_holder, fw, summary_type)

    fw.close()

    return data_for_json


def insert_summary_reference(nex_session, fw, load_summary_holder, source_id, summary_id, y):
    
    x = LocussummaryReference(summary_id = summary_id, 
                              reference_id = y['reference_id'], 
                              reference_order = y['reference_order'], 
                              source_id = source_id, 
                              created_by = CREATED_BY)
    nex_session.add(x)
    
    load_summary_holder['summary_reference_added'] = load_summary_holder['summary_reference_added'] + 1

    fw.write("insert new summary reference:" + str(summary_id) + ", " + str(y['reference_id']) + ", " + str(y['reference_order']))

def insert_summary(nex_session, fw, load_summary_holder, source_id, y):
    x = Locussummary(locus_id = y['locus_id'], 
                     summary_type = y['summary_type'], 
                     summary_order = y['summary_order'], 
                     text = y['text'], 
                     html = y['html'], 
                     source_id = source_id, 
                     created_by = CREATED_BY)
    nex_session.add(x)
    nex_session.commit()

    load_summary_holder['summary_added'] = load_summary_holder['summary_added'] + 1

    fw.write("insert summary:" + str(y['locus_id']) + ", " + y['summary_type'] + ", " + str(y['summary_order']) + ", " + y['text'] + ", " + y['html'])
    
    return x.summary_id

    
def update_references(nex_session, fw, load_summary_holder, source_id, summary_id, old_references, new_references):
    if old_references is None and new_references is None:
        return
    
    reference_updated = 0

    if old_references is None:
        for y in new_references:
            insert_summary_reference(nex_session, fw, load_summary_holder, source_id, summary_id, y)
        reference_updated = 1
    elif new_references is None:
        for y in old_references:
            nex_session.delete(y)
        reference_updated = 1
    else:
        ref_old = {}
        for x in old_references:
            ref_old[x.reference_id] = x

        ref_new = {}
        for y in new_references:
            if y['reference_id'] in ref_old:
                x = ref_old[y['reference_id']]
                if y['reference_order'] == x.reference_order:
                    continue
                else:
                    nex_session.query(LocussummaryReference).filter_by(summary_id=summary_id,reference_id=y['reference_id']).update({'reference_order': y['reference_order']})
                    reference_updated = 1
            else:
                insert_summary_reference(nex_session, fw, load_summary_holder, source_id, summary_id, y)
                reference_updated = 1
            ref_new[y['reference_id']] = 1

        ## clean up old refs
        # for x in old_references:
        #    if x.reference_id in ref_new:
        #        print "The REFERENCE is in the file"
        #        continue
        #    # nex_session.delete(x)
        #    # print "The LOCUSSUMMARY_REFERENCE row for summary_id=", summary_id, " and reference_id=", x.reference_id, " has been deleted from the database."

    return reference_updated

            
def read_summary_file(nex_session, fw, summary_type, summary_file_reader, log_file, data_for_json):

    from util import link_gene_names
    from models import Locusdbentity, Referencedbentity

    name_to_dbentity = dict([(x.systematic_name, x) for x in nex_session.query(Locusdbentity).all()])
    sgdid_to_dbentity_id = dict([(x.sgdid, x.dbentity_id) for x in nex_session.query(Locusdbentity).all()])
    pmid_to_reference_id = dict([(x.pmid, x.dbentity_id) for x in nex_session.query(Referencedbentity).all()]) 
    
    data = []
        
    if summary_type == 'Phenotype_Regulation':
        for pieces in summary_file_reader:

            summary_type = pieces[1]
            if summary_type in ['Phenotype', 'phenotype', 'PHENOTYPE']:
                summary_type = 'Phenotype'
            elif summary_type in ['Regulation', 'regulation', 'REGULATION']:
                summary_type = 'Regulation'

            dbentity = name_to_dbentity.get(pieces[0])

            if dbentity is None:
                data_for_json.append({'category': 'locus',
                                      'name': pieces[0],
                                      'type': x['summary_type'] + ' summary',
                                      'value': x['text'],
                                      'tag': "unknown gene name"})
                continue

            references = []
            if len(pieces) > 3:
                pmid_list = pieces[3].replace(' ', '')
                pmids = pmid_list.split('|')
                order = 0

                for pmid in pmids:
                    reference_id = pmid_to_reference_id.get(int(pmid))
                    if reference_id is None:
                        print("PMID=", pmid, " is not in the database")
                        continue
                    order = order + 1
                    references.append({'reference_id': reference_id, 'reference_order': order})

            data.append({'locus_id': dbentity.dbentity_id,
                         'text': pieces[2],
                         'html': link_gene_names(pieces[2], {dbentity.display_name, dbentity.format_name, dbentity.display_name + 'P', dbentity.format_name + 'P'}, nex_session),
                         'summary_type': summary_type,
                         'summary_order': 1,
                         'references': references,
                         'dbentity': dbentity})

    elif summary_type == 'Function':
        for pieces in summary_file_reader:
            if len(pieces) >= 8:
                sgdid = pieces[8]
                if sgdid.startswith('SGD:'):
                    dbentity_id = sgdid_to_dbentity_id.get(sgdid[4:])
                    if dbentity_id is None:
                        continue
                    functionSummary = [x[22:].strip() for x in pieces[9].split('|') if x.startswith('go_annotation_summary')]
                    if len(functionSummary) == 1:
                        data.append({'locus_id': dbentity_id,
                                     'text': functionSummary[0],
                                     'html': functionSummary[0],
                                     'summary_type': summary_type,
                                     'summary_order': 1})
    else:
        fw.write("Unknown summary_type: " + summary_type+ "\n")
        exit()
    
    return data


def write_summary_and_send_email(load_summary_holder, fw, summary_type):

    summary = ''
    summary = summary + "In total " + str(load_summary_holder['summary_added']) + " " + summary_type + " summaries added.\n"
    summary = summary + "In total " + str(load_summary_holder['summary_updated']) + " " + summary_type + " summaries updated.\n"
    summary = summary + "In total " + str(load_summary_holder['summary_reference_added']) + " " + summary_type + " summary references addedd.\n\n"
    
    fw.write(summary)

    
    # email_subject = summary_type + " Summaries Loading"
    # send email here                                                                               
    # sendmail(email_subject, summary, EMAIL)

    print(summary)


if __name__ == "__main__":
        
    summary_file = ""
    summary_type = ""
    if len(sys.argv) >= 3:
        summary_file = sys.argv[1]
        summary_type = sys.argv[2]
    elif len(sys.argv) >= 2:
        summary_file = sys.argv[1]
    else:
        print("Usage: load_summaries.py summary_file_name_with_path summary_type[Phenotype_Regulation|Function]")
        print("Example: load_summaries.py summary_test.txt Phenotype_Regulation")
        print("Example: load_summaries.py gp_information.559292_sgd Function")
        exit()

    f = open(summary_file, 'r')

    summary_file_reader = csv.reader(f, delimiter='\t')

    nex_session = get_dev_session

    data_to_return = load_summaries(nex_session, summary_file_reader, summary_type)

    print(json.dumps(data_to_return, sort_keys=True, indent=4))
    
