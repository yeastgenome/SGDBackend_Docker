const JOIN_HIGHLIGHT_BY = '...';
const FILTER_ORDER = ['gene_type', 'species'];

import { makeFieldDisplayName } from '../lib/searchHelpers';
import { NON_HIGHLIGHTED_FIELDS } from '../constants';

// takes the fields in responseObj.highlights and replaces the shallow values in responseObj
// also return highlight values as strings like '<em>val</em>...<em>val2</em>' instead of array
export function injectHighlightIntoResponse(responseObj) {
  let high = responseObj.highlights || {};
  let highKeys = Object.keys(high);
  let simpleHighObj = {};
  highKeys.forEach( key => {
    let highArr = high[key];
    let highStr = highArr.reduce( (prev, current, i) => {
      let suffix = (i === highArr.length - 1) ? '' : JOIN_HIGHLIGHT_BY;
      return prev + current + suffix;
    }, '');
    simpleHighObj[key] = highStr;
    // don't highlight some fields
    if (NON_HIGHLIGHTED_FIELDS.indexOf(key) < 0) {
      responseObj[key] = highStr;
    }
  });
  responseObj.highlights = simpleHighObj;
  return responseObj;
}

export function parseResults(results) {
  return results.map( d => {
    switch (d.category) {
    case 'gene':
      return parseGeneResult(d);
    case 'go':
      return parseGoResult(d);
    case 'disease':
      return parseDiseaseResult(d);
    case 'homology_group':
      return parseHomologyGroupResult(d);
    default:
      return parseDefaultResult(d);
    }
  });
}

export function parseAggs(rawAggs, queryObject) {
  // first sort them
  rawAggs = rawAggs.sort( (a, b) => (FILTER_ORDER.indexOf(a.key) < FILTER_ORDER.indexOf(b.key)) );
  return rawAggs.map( d => {
    let _values = d.values.map( _d => {
      let currentValue = queryObject[d.key];
      let _isActive;
      // look at array fields differently
      if (typeof currentValue === 'object') {
        _isActive = (currentValue.indexOf(_d.key) >= 0);
      } else {
        _isActive = _d.key === currentValue;
      }
      return {
        name: _d.key,
        displayName: makeFieldDisplayName(_d.key),
        key: _d.key,
        total: _d.total,
        isActive: _isActive
      };
    });
    return {
      name: d.key,
      displayName: makeFieldDisplayName(d.key),
      key: d.key,
      values: _values
    };
  });
}

function parseCoordinates(d) {
  // make sure there is a chromosome identifiers
  let chrom = d.gene_chromosomes || [];
  chrom = chrom.filter( d => d );
  if (chrom.length !== 1) {
    return null;
  }
  chrom = chrom[0];
  // make sure there are coordinates
  let numFields = ['gene_chromosome_starts', 'gene_chromosome_ends'];
  for (var i = numFields.length - 1; i >= 0; i--) {
    let field = numFields[i];
    let type = typeof d[field];
    if (type !== 'string' && type !== 'number') {
      return null;
    }
  }
  // only render what you can
  return `chr${chrom}:${d.gene_chromosome_starts}-${d.gene_chromosome_ends}`;
}

// search result individual entry parsers
function parseGeneResult(_d) {
  let d = injectHighlightIntoResponse(_d);
  return {
    symbol: d.gene_symbol || '(no symbol)',
    category: d.category || 'gene',
    display_name: d.gene_symbol,
    href: d.href,
    name: d.name,
    id: d.id || '(no ID)',
    sourceHref: d.href,
    synonyms: d.gene_synonyms,
    gene_type: makeFieldDisplayName(d.gene_type),
    species: d.species,
    highlight: d.highlights,
    homologs: parseLogs(d.homologs),
    paralogs: parseLogs(d.paralogs),
    genomic_coordinates: parseCoordinates(_d)
  };
}

function parseLogs(logs) {
  if (!logs) return null;
  return logs.map( d => {
    let famId = d.panther_family;
    d.evidence_name = famId;
    d.evidence_href = `http://pantherdb.org/panther/family.do?clsAccession=${famId}`;
    return d;
  });
}

function parseGoResult(_d) {
  let d = injectHighlightIntoResponse(_d);
  return {
    category: d.category,
    display_name: d.name,
    go_branch: makeFieldDisplayName(d.go_type),
    highlight: d.highlights,
    href: d.href,
    name: d.name,
    synonyms: d.go_synonyms
  };
}

function parseDiseaseResult(_d) {
  let d = injectHighlightIntoResponse(_d);
  return {
    associated_genes: d.associated_genes,
    category: d.category,
    display_name: d.name,
    go_branch: d.go_branch,
    highlight: d.highlights,
    href: d.href,
    name: d.name,
    omim_id: d.id,
    synonyms: d.disease_synonyms
  };
}

function parseHomologyGroupResult(_d) {
  let d = injectHighlightIntoResponse(_d);
  return {
    associated_genes: d.associated_genes,
    category: d.category || 'gene',
    display_name: d.name,
    highlight: d.highlights,
    href: d.href,
    name: d.name,
    synonyms: d.synonym,
    member_genes: _d.member_genes
  };
}

function parseDefaultResult(_d) {
  let d = injectHighlightIntoResponse(_d);
  if(d.category == 'download'){
    return {
      associated_genes: d.associated_genes,
      category: d.category,
      display_name: d.name,
      highlight: d.highlights,
      href: d.href,
      name: d.name,
      synonyms: d.synonym,
      file_size: d.file_size,
      readme_url: d.readme_url,
      status: d.status
    };

  }
  else{
    return {
      associated_genes: d.associated_genes,
      category: d.category || 'gene',
      display_name: d.name,
      highlight: d.highlights,
      href: d.href,
      name: d.name,
      synonyms: d.synonym
    };
  }
}
