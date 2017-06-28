import React from 'react';
import Statistics from '../components/dashboard/Statistics';
import Kpi from '../components/dashboard/KPI';
import GeoVisualization from '../components/dashboard/GeoVisualization';
import PageBase from '../components/PageBase';
import FilterDrawer, {FilterObj} from "../components/filter/FilterDrawer";

class DashboardPage extends React.Component{
  constructor() {
    super();

    let filterObj = new FilterObj();
    filterObj.startDate = new Date();
    filterObj.endDate = new Date();
    filterObj.vehicleList = [];

    this.state = { filterObj: filterObj };
  }

  applyFilter(filterObj) {
    this.setState({ filterObj: filterObj });
  }

  render() {
    return (
      <PageBase title = "Overview" navigation = "Application / Overview">
        <div>
          <Kpi />
          <Statistics />
          <GeoVisualization filterObj={this.state.filterObj}/>
        </div>
        <FilterDrawer 
          filterObj = {this.state.filterObj} 
          applyFilter = {this.applyFilter.bind(this)}
        />
      </PageBase>
    );
  }
}

export default DashboardPage;
