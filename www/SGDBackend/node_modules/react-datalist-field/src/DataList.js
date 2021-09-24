import React, { Component } from 'react';
import PropTypes from 'prop-types';
import './style.css';

class DataList extends Component {
  constructor(props) {
    super(props);
    this.handleOnBlur = this.handleOnBlur.bind(this);
    this.handleSelect = this.handleSelect.bind(this);
    this.handleMoreOptions = this.handleMoreOptions.bind(this);

    let inputFieldText = this._handleGetInputValue(this.props.selectedId) ;
    inputFieldText = inputFieldText == undefined ? '': inputFieldText[this.props.left];
    
    this.state = {
      showOptions: false,
      inputFieldText: inputFieldText,
      selectedOptionId: this.props.selectedId,
      isMoreOptionClicked:false,
      showMoreOptions: false,
      searchString:''
    };
  }

  componentDidUpdate(prevProps,prevState) {
    //state: change is internal
    if (prevState.selectedOptionId != this.state.selectedOptionId) {
      // console.log('state');
      var selected_item = this._handleGetInputValue(this.state.selectedOptionId);
      if (selected_item != undefined) {
        this.setState({ 
          selectedOptionId: selected_item[this.props.id], 
          inputFieldText: selected_item[this.props.left], 
          searchString:'' });
      }
      
      if ('onOptionChange' in this.props && typeof this.props.onOptionChange == 'function' ){
        this.props.onOptionChange();
      }
    }
    // props: change is external
    else if (prevProps.selectedId != this.props.selectedId){
      // console.log('props');
      var selected_item = this._handleGetInputValue(this.props.selectedId);
      if (selected_item != undefined) {
        this.setState({ 
          selectedOptionId: selected_item[this.props.id], 
          inputFieldText: selected_item[this.props.left], 
          searchString:'' });
      }
      else if(this.props.setNewValue == true){
        this.setState({inputFieldText: this.props.selectedId});
      }
      else{
        this.setState({ 
          selectedOptionId: '', 
          inputFieldText: '', 
          searchString:'' });
      }
    }
    else if(this.state.showOptions == false && prevState.showOptions == true){
      //Closing the dropdown
      // console.log('dropdown');
      if (this.state.searchString != ''){
        var selected_item = this._handleGetInputValue(this.state.selectedOptionId);
        if (selected_item == undefined){
          if (this.props.setNewValue == true){
            this.setState({inputFieldText:this.state.selectedOptionId,searchString:''});
          }
          else{
            this.setState({inputFieldText:'',searchString:''});
          }
        }
        else{
          this.setState({inputFieldText:selected_item[this.props.left],searchString:''});
        }
      }
    }
  }

  _handleGetSearchString(input_value){
    let searchString = [...input_value].map(char => /[()]/g.test(char) ? '\\'+char : char).join('');
    return searchString;
  }

  _handleGetInputValue(index){
    let selectedInputValue= this.props.options.filter((value) => value[this.props.id] == index)[0];
    return selectedInputValue;
  }

  handleOnBlur() {
    if (this.state.isMoreOptionClicked) {
      this.setState({ isMoreOptionClicked:false});
      this.nameInput.focus();
    }
    else {
      this.handleHideOptions();
    }
  }

  handleShowOptions() {
    this.setState({ showOptions: true });
  }

  handleHideOptions() {
    this.setState({ showOptions: false,showMoreOptions: false });
  }

  handleMoreOptions() {
    this.setState({ isMoreOptionClicked:true,showMoreOptions: true});
  }

  handleChange(e) {
    var input_value = e.target.value;  
    if (input_value != '') {
      if (/[()]/g.test(input_value)){
        let searchString = this._handleGetSearchString(input_value);
        this.setState({ inputFieldText: input_value,searchString:searchString});
      }
      else{
        this.setState({ inputFieldText: input_value,searchString:input_value});
      }
    }
    else {
      this.setState({ inputFieldText: input_value, selectedOptionId:'',searchString:'' });
    }
  }

  handleSelect(index) {
    var selected_item = this._handleGetInputValue(index);
    if (selected_item != undefined) {
      this.setState({ selectedOptionId: selected_item[this.props.id], inputFieldText: selected_item[this.props.left],searchString:'' });
      this.handleHideOptions();
    }
  }

  handleNewValue(){
    this.setState({selectedOptionId: this.state.inputFieldText });
  }

  renderOptions() {
    var options; 
    options = this.props.options
        .filter((value) => RegExp('^' + this.state.searchString + '.*', 'i').test(value[this.props.right]) || 
                           RegExp('^' + this.state.searchString + '.*', 'i').test(value[this.props.left]))
        .map((option) => {
          return <li value={option[this.props.left]} key={option[this.props.id]} className='clearfix' onMouseDown={() => this.handleSelect(option[this.props.id])}>
            <a> <span className='float-left'>{option[this.props.left]} </span><span className='float-right'>{option[this.props.right]}</span> </a>
          </li>;
        });
    if (!this.state.showMoreOptions) {
      if(options.length > 10){
        options = options.slice(0,10);
        options.push(<li key='-1' onMouseDown={() => this.handleMoreOptions()}><a>more options</a></li>);
      }
    }

    if (this.props.setNewValue && this.state.inputFieldText != '') {
      options.unshift(<li value={this.state.inputFieldText} key='0' className='clearfix' onMouseDown={() => this.handleNewValue()}>
        <a><span className='float-left'>{this.state.inputFieldText} </span></a></li>);
    }

    return (
      <div className={this.state.showOptions ? 'reactDatalist_show' : 'reactDatalist_hide'}>
        <div className='reactDatalist_options'>
          <ul className='reactDatalist_options_list'>
            {options}
          </ul>
        </div>
      </div>
    );
  }

  render() {
    let isDev = this.props.dev == true ? <p>option selected: {this.state.selectedOptionId}</p>: ''
    return (
      <div className='reactDatalist'>
          <input type='text' ref={(input) => { this.nameInput = input; }} className='reactDatalist_input' 
          onSelect={() => this.handleShowOptions()} onBlur={() => this.handleOnBlur()} 
          onChange={this.handleChange.bind(this)} value={this.state.inputFieldText} />
          {this.renderOptions()}
          <input type='hidden' name={this.props.selectedIdName} value={this.state.selectedOptionId} />
          {isDev}
      </div>
    );
  }

}

DataList.propTypes = {
  options: PropTypes.array.isRequired,
  id: PropTypes.string.isRequired,
  left: PropTypes.string.isRequired,
  right: PropTypes.string.isRequired,
  onOptionChange: PropTypes.func,
  selectedIdName: PropTypes.string.isRequired,
  selectedId:PropTypes.string.isRequired,
  setNewValue:PropTypes.bool,
  dev:PropTypes.bool
};

DataList.defaultProps = {
  setNewValue:false,
  dev:false
};

export default DataList;