import React from "react";
import Statistics from "../components/dashboard/Statistics";
import Kpi from "../components/dashboard/KPI";
import GeoVisualization from "../components/dashboard/GeoVisualization";
import PageBase from "../components/PageBase";
import FilterDrawer, { FilterObj } from "../components/filter/FilterDrawer";

class DashboardPage extends React.Component {
    constructor() {
        super();

        let filterObj = new FilterObj(), start = new Date(), end = new Date();
        filterObj.startDate = start;
        filterObj.endDate = end;
        filterObj.vehicleList = [];

        this.state = { filterObj: filterObj };
    }

    applyFilter(filterObj) {
        this.setState({ filterObj: filterObj });
        //alert('filter callback');
    }

    render() {
        return (
            <PageBase title="Overview" navigation="Application / Overview">
                <div>
                    <div>
                        <Kpi filterObj={this.state.filterObj} />
                        <Statistics filterObj={this.state.filterObj} />
                        <GeoVisualization filterObj={this.state.filterObj} />
                    </div>
                    <div>
                        <FilterDrawer
                            filterObj={this.state.filterObj}
                            applyFilter={this.applyFilter.bind(this)}
                        />
                    </div>
                </div>
            </PageBase>
        );
    }
}

export default DashboardPage;
