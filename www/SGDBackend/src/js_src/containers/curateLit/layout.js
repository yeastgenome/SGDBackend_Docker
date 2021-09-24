  /* eslint-disable*/
import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import style from './style.css';
import { SMALL_COL_CLASS, LARGE_COL_CLASS } from '../../constants';
import fetchData from '../../lib/fetchData';
import LoadingPage from '../../components/loadingPage';
// import AuthorResponseDrawer from './authorResponseDrawer';
import CategoryLabel from '../../components/categoryLabel';
import updateTitle from '../../lib/updateTitle';
import { selectActiveLitEntry } from '../../selectors/litSelectors';
import { updateActiveEntry } from './litActions';
import { setNotReady, finishPending } from '../../actions/metaActions';
import { PREVIEW_URL } from '../../constants.js';
import {Switch,Route} from 'react-router-dom';
import CurateLitBasic from '../curateLit/basic';
import CurateLitPhenotype from '../curateLit/phenotype';
import {requireAuthentication} from '../authenticateComponent';
import Referencesetting from './referencesettings';

const BASE_CURATE_URL = '/curate/reference';
const SECTIONS = [
  'tags',
  'Settings'
];

class CurateLitLayout extends Component {
  componentDidMount() {
    this.props.dispatch(setNotReady());
    this.fetchData();
    this._isMounted = true;
  }

  componentWillUnmount() {
    this._isMounted = false;
    updateTitle('');
  }

  fetchData() {
    let id = this.props.match.params.id;
    let url = `/reference/${id}`;
    fetchData(url).then( (data) => {
      if (this._isMounted) {
        updateTitle(data.citation);
        this.props.dispatch(updateActiveEntry(data));
        this.props.dispatch(finishPending());
      }
    });
  }

  renderHeader() {
    let d = this.props.activeEntry;
    let previewUrl = `${PREVIEW_URL}/reference/${this.props.match.params.id}`;
    let urls = d.urls || [];
    let linkNodes = urls.map( (d, i) => {
      return <span key={`refL${i}`} style={{ marginRight: '1rem' }}><a href={d.link} target='_new'>{d.display_name}</a> </span>;
    });
    if (d.pubmed_id) {
      linkNodes.unshift(<span key='refLp' style={{ marginRight: '1rem' }}>PMID: {d.pubmed_id} </span>);
    }
    return (
      <div>
        <h3 style={{ display: 'inline-block', marginRight: '0.5rem' }}><CategoryLabel category='reference' hideLabel isPageTitle /> {d.citation}</h3>
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <span style={{ display: 'inline-block' }}><a href={previewUrl} target='_new'><i className='fa fa-file-image-o' aria-hidden='true'></i> preview</a></span>
          <span>{linkNodes}</span>
        </div>
        <hr style={{ margin: '1rem 0' }} />
      </div>
    );
  }

  renderSectionsNav() {
    let baseUrl = `${BASE_CURATE_URL}/${this.props.match.params.id}`;
    let current = this.props.pathname.replace(baseUrl, '');

    let temp = SECTIONS.map( (d) => {
      let relative;
      if (d === 'tags') {
        relative = '';
      } else {
        relative = `/${d}`;
      }
      let isActive = (current === relative);
      let url = `${baseUrl}${relative}`;
      let _className = isActive ? style.activeNavLink : style.navLink;
      return <li key={`lit${d}`}><Link className={_className} to={url}>{d}</Link></li>;
    });
    return temp;
  }

  render() {
    if (!this.props.isReady) return <LoadingPage />;
    return (
      <div>
        {this.renderHeader()}
        <div className='row'>
          <div className={SMALL_COL_CLASS}>
            <ul className='vertical menu'>
              {this.renderSectionsNav()}
            </ul>
          </div>
          <div className={LARGE_COL_CLASS}>
            <div>
              <Switch>
                <Route component={Referencesetting} path='/curate/reference/:id/settings'/>
                <Route component={CurateLitBasic} exact/>
                {/* TODO: Navigate to phenotypes */}
                {/* <Route component={CurateLitPhenotype} path='/curate/reference/:id/phenotypes' exact/> */}
              </Switch>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

CurateLitLayout.propTypes = {
  activeEntry: PropTypes.object,
  children: PropTypes.node,
  dispatch: PropTypes.func,
  params: PropTypes.object,
  pathname: PropTypes.string,
  isReady: PropTypes.bool
};

function mapStateToProps(state) {
  return {
    activeEntry: selectActiveLitEntry(state),
    pathname: state.router.location.pathname,
    isReady: state.meta.get('isReady')
  };
}

export { CurateLitLayout as CurateLitLayout };
export default connect(mapStateToProps)(CurateLitLayout);
