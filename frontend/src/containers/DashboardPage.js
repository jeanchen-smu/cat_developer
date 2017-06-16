import React from 'react';
import Statistics from '../components/dashboard/Statistics';
import Kpi from '../components/dashboard/KPI';
import GeoVisualization from '../components/dashboard/GeoVisualization';

class DashboardPage extends React.Component{
  render() {
    return (
      <div>
        <Kpi />
        <Statistics />
        <GeoVisualization filterObj={[1.36716,103.80921,30]}/>
      </div>
    );
  };
};

export default DashboardPage;
