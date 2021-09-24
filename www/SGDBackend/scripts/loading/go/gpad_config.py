curator_id = {'Rama Balakrishnan'   : 'RAMA',
              'Selina Dwight'       : 'DWIGHT',
              'Rob Nash'            : 'NASH',
              'Stacia Engel'        : 'STACIA',
              'Marek Skrzypek'      : 'MAREK',
              'Maria Costanzo'      : 'MARIA',
              'Dianna Fisk'         : 'FISK',
              'Edith Wong'          : 'EDITH',
              'Paul Lloyd'          : 'PLLOYD',
              'Janos Demeter'       : 'JDEMETER',
              'Diane Inglis'        : 'DIANE',
              'Shuai Weng'          : 'SHUAI',
              'Jodi Hirschman'      : 'JODI',
              'Kara Dolinski'       : 'KARA',   
              'Chandra Theesfeld'   : 'CHANDRA',
              'Julie Park'          : 'JULIEP',
              'Karen Christie'      : 'KCHRIS',
              'Anand Sethuraman'    : 'ANAND',
              'Laurie Issel-Traver' : 'LAURIE',
              'Midori Harris'       : 'MIDORI',
              'Eurie Hong'          : 'EURIE',
              'Cynthia Krieger'     : 'CINDY',
              'Rose Oughtred'       : 'ROSE',
              'Terry Jackson'       : 'TLJ',
              'Sage Hellerstedt'    : 'SAGEH',
              'Kevin MacPherson'    : 'KMACPHER',
              'Olivia Lang'         : 'OWLANG',
              'Emily Heald'         : 'EMILYJC',
              'Suzi Aleksander'     : 'SUZIA',
              'Joanna Argasinska'   : 'JOANNA',
              'Micheal Alexander'   : 'MICHEAL',
              'Barbara Dunn'        : 'BDUNN',
              'Patrick Ng'          : 'PCNG',
              '0000-0002-2657-8762' : 'KMACPHER',
              '0000-0001-6787-2901' : 'SUZIA',
              '0000-0003-3841-4324' : 'MICHEAL',
              '0000-0003-2678-2824' : 'JOANNA',
              '0000-0002-7041-0035' : 'BDUNN',
              '0000-0001-5472-917X' : 'STACIA',
              '0000-0002-5299-5308' : 'SAGEH',
              '0000-0002-3726-7441' : 'NASH',
              '0000-0001-8208-652X' : 'PCNG',
              '0000-0001-6749-615X' : 'MAREK',
              '0000-0001-9799-5523' : 'EDITH' }

computational_created_by = 'OTTO'
email_receiver = ['sweng@stanford.edu']
email_subject = 'GPAD loading summary'

go_db_code_mapping = {
    'EC'                 : ['IUBMB', 'EC number'],
    'EMBL'               : ['GenBank/EMBL/DDBJ', 'DNA accession ID'],
    'ENSEMBL'            : ['ENSEMBL', 'Gene ID'],
    'FLYBASE'            : ['FLYBASE', 'Gene ID'],
    'GO'                 : ['GO Consortium', 'GOID'],
    'HAMAP'              : ['EXPASY', 'HAMAP'],
    'HUGO'               : ['HUGO', 'Gene ID'],
    'InterPro'           : ['EBI', 'InterPro'],
    'MGI'                : ['MGI', 'Gene ID'],
    'PANTHER'            : ['PANTHER', 'PANTHER'],
    'PDB'                : ['PDB', 'PDB ID'],
    'PomBase'            : ['PomBase', 'Gene ID'],
    'Prosite'            : ['Prosite', 'Prosite ID'],
    'RGD'                : ['RGD', 'Gene ID'],
    'SGD'                : ['SGD', 'DBID Primary'],
    'UniProtKB-KW'       : ['EBI', 'UniProtKB Keyword'],
    'UniProtKB-SubCell'  : ['EBI', 'UniProtKB Subcellular Location'],
    'TAIR'               : ['TAIR', 'Gene ID'],
    'UniProtKB'          : ['EBI', 'UniProt/Swiss-Prot ID'],
    'WB'                 : ['WB', 'Gene ID'],
    'protein_id'         : ['GenBank/EMBL/DDBJ', 'Protein version ID'],
    'UniPathway'         : ['UniPathway', 'UniPathway ID'],
    'HAMAP'              : ['HAMAP', 'HAMAP ID']
}


go_ref_mapping = {
    'GO_REF:0000002' : 'S000124036', 
    'GO_REF:0000003' : 'S000124037',
    'GO_REF:0000004' : 'S000124038',
    'GO_REF:0000015' : 'S000069584',
    'GO_REF:0000020' : 'S000181932',
    'GO_REF:0000023' : 'S000125578',
    'GO_REF:0000024' : 'S000250423',
    'GO_REF:0000033' : 'S000185201',
    'GO_REF:0000036' : 'S000147045',
    'GO_REF:0000037' : 'S000148669',
    'GO_REF:0000038' : 'S000148670',
    'GO_REF:0000039' : 'S000148671',
    'GO_REF:0000040' : 'S000148672',
    'GO_REF:0000041' : 'S000150560',
    'GO_REF:0000043' : 'S000250402',
    'GO_REF:0000044' : 'S000250403',
    'GO_REF:0000047' : 'S000250424',
    'GO_REF:0000050' : 'S000250425',
    'GO_REF:0000101' : 'S000250426',
    'GO_REF:0000104' : 'S000181514',
    'GO_REF:0000107' : 'S000204514',
    'GO_REF:0000108' : 'S000204515',
    'GO_REF:0000111' : 'S000246004',
    'GO_REF:0000114' : 'S000250427',
    'GO_REF:0000115' : 'S000246005'
}

current_go_qualifier = ['NOT', 'colocalizes_with', 'contributes_to']

    