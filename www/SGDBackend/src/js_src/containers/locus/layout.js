/*eslint-disable */
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import style from './style.css';
import CategoryLabel from '../../components/categoryLabel';
import DetailList from '../../components/detailList';
import fetchData from '../../lib/fetchData';
// import Loader from '../../components/loader';
import updateTitle from '../../lib/updateTitle';
import { updateData, clearPending} from './locusActions';
import { PREVIEW_URL } from '../../constants.js';
import {Switch,Route} from 'react-router-dom';
import LocusBasic from '../locus/basic';
import LocusSummaries from '../locus/summaries';
const BASE_CURATE_URL = '/curate/locus';
const SECTIONS = [
  'basic',
  // 'gene_name',
  'summaries'
];

class LocusLayout extends Component {
  componentDidMount() {
    this.fetchData();
  }

  fetchData() {
    let id = this.props.match.params.id;
    let url = `/locus/${id}/curate`;
    this.props.dispatch(updateData(null));
    fetchData(url).then( (data) => {
      updateTitle(data.name);
      this.props.dispatch(clearPending());
      this.props.dispatch(updateData(data));
    }); 
  }

  renderNav() {
    let baseUrl = `${BASE_CURATE_URL}/${this.props.match.params.id}`;
    let current = this.props.pathname.replace(baseUrl, '');
    let nodes = SECTIONS.map( (d) => {
      let relative = d ? `/${d}` : '';
      current = !current? relative : current; 
      let isActive = (current === relative);
      let url = `${baseUrl}${relative}`;
      let _className = isActive ? style.activeNavLink : style.navLink;
      return <li key={`lit${d}`}><Link className={_className} to={url}>{d.replace('_', ' ')}</Link></li>;
    });
    return <ul className={`vertical menu ${style.menu}`}>{nodes}</ul>;
  }

  renderHeader() {
    let data = this.props.data;
    let previewUrl = `${PREVIEW_URL}/locus/${this.props.match.params.id}`;
    if (!data) return null;
    return (
      <div>
        <h3 style={{ display: 'inline-block', marginRight: '0.5rem' }}><CategoryLabel category='locus' hideLabel isPageTitle /> {data.name}</h3>
        <span><a href={previewUrl} target='_new'><i className='fa fa-file-image-o' aria-hidden='true'></i> preview</a></span>
        <DetailList data={data} fields={['sgdid', 'systematic_name']} />
        <hr style={{ margin: '1rem 0 0 0' }} />
      </div>
    );
  }

  render() {    
    return (
      <div>
        {this.renderHeader()}
        <div className='row'>
          <div className='columns small-2'>
            {this.renderNav()}
          </div>
          <div className='columns small-10'>
            <Switch>
              <Route component={LocusBasic} path='/curate/locus/:id/basic'/>
              <Route component={LocusSummaries} path='/curate/locus/:id/summaries'/>
              <Route component={LocusBasic} />
            </Switch>
          </div>  
        </div>
        
      </div>
    );
  }
}

LocusLayout.propTypes = {
  children: PropTypes.node,
  data: PropTypes.object,
  dispatch: PropTypes.func,
  pathname: PropTypes.string,
  params: PropTypes.object
};

function mapStateToProps(state) {
  let _data = state.locus.get('data') ? state.locus.get('data').toJS() : null;
  return {
    data: _data,
    pathname: state.router.location.pathname
  };
}

export { LocusLayout as LocusLayout };
export default connect(mapStateToProps)(LocusLayout);
