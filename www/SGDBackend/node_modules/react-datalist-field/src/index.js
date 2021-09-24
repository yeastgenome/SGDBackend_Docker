import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import DataList from './DataList';

var cars = [
  { id: 1, model: "(CRV", company: "Honda" },
  { id: 2, model: "Accord", company: "Honda" },
  { id: 3, model: "800", company: "Maruti" },
  { id: 4, model: "Civic", company: "Honda" },
  { id: 5, model: "Model S", company: "Tesla" },
  { id: 6, model: "Model 3", company: "Tesla" },
  { id: 7, model: "Model X", company: "Tesla" },
  { id: 8, model: "Corolla", company: "Toyota" },
  { id: 9, model: "Rav4", company: "Toyota" },
  { id: 10, model: "Camry", company: "Toyota" },
  { id: 11, model: "Innova", company: "Toyota" },
  { id: 12, model: "Ya(ris", company: "Toyota" },
  { id: 13, model: "Pri(us", company: "Toyota" },
  { id: 14, model: "High(lander", company: "Toyota" },
  { id: 15, model: "Grand Cherokee", company: "Jeep" },
  { id: 16, model: "Wrangler", company: "Jeep" },
  { id: 17, model: "Comanche", company: "Jeep" }
];

class DataListExampleDev {
  constructor(options) {
    if (typeof options === "undefined") options = {};
    options.el = options.el || document.getElementById('example');

    ReactDOM.render(React.createElement(DataList, {
      options: cars,
      id: 'id',
      left: 'model',
      right: 'company',
      selectedIdName: 'selectedCar',
      selectedId: '',
      onOptionChange: this.handleSelection,
      dev:true,
      setNewValue:true
    }), options.el);
  }

  handleSelection() {
    let selection = document.getElementsByName('selectedCar')[0];
    if (document.getElementById('demo') == null) {
      let p = document.createElement("h3");
      p.id = 'demo';
      if (selection.value !== null && selection.value !== '') {
        p.innerHTML = 'Selected value = ' + selection.value.toString();
        document.body.appendChild(p);
      }
    }
    else {
      let p = document.getElementById('demo');
      if (selection !== null) {
        p.innerHTML = 'Selected value = ' + selection.value.toString();
      }
    }
  };
}

class DataListExample extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedValue: ''
      ,count:0
    }
    this.handleChange = this.handleChange.bind(this);
    this.handleClick = this.handleClick.bind(this);
  }

  handleChange() {
    var element = document.getElementsByName('selectedCar')[0];
    this.setState({ selectedValue: element.value });
  }

  handleClick(){
    var count = this.state.count;
    this.setState({count:count+1});
  }

  render() {
    
    return (
      <div>
        <DataList
          options={cars}
          id='id'
          left='model'
          right='company'
          selectedIdName='selectedCar'
          selectedId=''
          onOptionChange={this.handleChange}
        />
        {/* <button onClick={this.handleClick}>Click Me</button>
        <h3>{this.state.count}</h3> */}
        <p>You have selected option: {this.state.selectedValue}</p>
      </div>
    )
  }
}

export { DataListExampleDev, DataListExample, DataList };