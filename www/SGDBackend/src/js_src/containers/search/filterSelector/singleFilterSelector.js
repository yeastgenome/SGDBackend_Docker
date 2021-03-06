/*eslint-disable react/no-set-state */
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import Select from 'react-select';
import { push } from 'connected-react-router';
import PropTypes from 'prop-types';
import style from './style.css';
import { getQueryParamWithValueChanged,convertSearchObjectToString } from '../../../lib/searchHelpers';
import CategoryLabel from '../../../components/categoryLabel';

const DELIMITER = '@@';
const SMALL_NUM_VISIBLE = 10;
const MED_NUM_VISIBLE = 25;
const MAX_NUM_VISIBLE = 1000;
const SEARCH_PATH = '/search';

class SingleFilterSelector extends Component {
  constructor(props) {
    super(props);
    this.state = {
      numVisible: SMALL_NUM_VISIBLE,
      isSearchMode: false
    };
  }

  handleSelectChange(newValues) {
    let simpleValues = newValues.map( d => d.name );
    let newQp = getQueryParamWithValueChanged(this.props.name, simpleValues, this.props.queryParams);
    let newPath = { pathname: SEARCH_PATH, query: newQp };
    this.props.dispatch(push(newPath));
  }

  renderFilterValues() {
    let values = this.props.values.slice(0, this.state.numVisible);
    return values.map( d => {
      let classSuffix = d.isActive ? style.activeFilter : style.inactiveFilter;
      let _key = `fv.${this.props.name}.${d.name}`;
      let nameNode;
      if (this.props.name.match('species')) {
        nameNode = <i>{d.displayName}</i>;
      } else if (this.props.name === 'category') {
        nameNode = <CategoryLabel category={d.name} />;
      } else {
        nameNode = <span>{d.displayName}</span>;
      }      
      let newQueryObj = getQueryParamWithValueChanged(this.props.name, d.key, this.props.queryParams);
      var search = convertSearchObjectToString(newQueryObj);
      return (
        <div className={`${style.filter} ${classSuffix}`} key={_key}>
          <Link to={{ pathname: SEARCH_PATH, search:  search}}>
            <span className={style.aggLink}>
              <span className={style.aggLinkLabel}>{nameNode}</span><span>{d.total.toLocaleString()}</span>
            </span>
          </Link>
        </div>
      );
    });
  }

  handleControlClick(e) {
    e.preventDefault();
    this.setState({ numVisible: this.getNextNumVisible() });
  }

  handleToggleMode(e) {
    e.preventDefault();
    this.setState({ isSearchMode: !this.state.isSearchMode });
  }

  getNextNumVisible() {
    let currentNum = this.state.numVisible;
    let newNum;
    if (currentNum === SMALL_NUM_VISIBLE) {
      newNum = MED_NUM_VISIBLE;
    } else if (currentNum === MED_NUM_VISIBLE) {
      newNum = MAX_NUM_VISIBLE;
    } else {
      newNum = SMALL_NUM_VISIBLE;
    }
    return newNum;
  }

  renderSearchNode() {
    let currentValues = this.props.values.filter( d => d.isActive );
    return (
      <div className={style.selectContainer}>
        <Select
          delimiter={DELIMITER}
          labelKey='displayName'
          multi
          onChange={this.handleSelectChange.bind(this)}
          options={this.props.values}
          placeholder='Search or Select'
          value={currentValues}
          valueKey='name'
        />
      </div>
    );
  }

  renderControlNode() {
    if (this.props.values.length <= SMALL_NUM_VISIBLE) return null;
    let moreLabel = (this.state.numVisible !== MAX_NUM_VISIBLE) ? 'Show More' : `Show ${SMALL_NUM_VISIBLE}`;
    let modeLabelNode = this.state.isSearchMode ? <span>List</span> : <span><i className='fa fa-search' /></span>;
    let moreLabelNode = this.state.isSearchMode ? <span /> : <a href='#' onClick={this.handleControlClick.bind(this)}>{moreLabel}</a>;
    return (
      <p className={style.singleFacetControl}>
        <a href='#' onClick={this.handleToggleMode.bind(this)} >{modeLabelNode}</a>
        {moreLabelNode}
      </p>
    );
  }

  renderListNode() {
    return (
      <div>
        {this.renderFilterValues(this.props)}
      </div>
    );
  }

  render() {
    // don't render an empty filter
    if (this.props.values.length === 0) {
      return null;
    }
    let selectableNode = this.state.isSearchMode ? this.renderSearchNode() : this.renderListNode();
    return (
      <div className={style.aggValContainer}>
        <p className={style.filterLabel}><b>{this.props.displayName}</b></p>
        {selectableNode}
        {this.renderControlNode()}
      </div>
    );
  }
}

SingleFilterSelector.propTypes = {
  dispatch: PropTypes.func,
  displayName: PropTypes.string,
  name: PropTypes.string,
  queryParams: PropTypes.object,
  values: PropTypes.array
};

export default connect()(SingleFilterSelector);
