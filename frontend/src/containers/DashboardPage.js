import React from "react";
import Statistics from "../components/dashboard/Statistics";
import Kpi from "../components/dashboard/KPI";
import GeoVisualization from "../components/dashboard/GeoVisualization";
import PageBase from "../components/PageBase";
import FilterDrawer, { FilterObj } from "../components/filter/FilterDrawer";

class DashboardPage extends React.Component {
    constructor() {
        super();
        this.state = { filterObj: defaultFilter() };
    }

    defaultFilter() {
        let filterObj = new FilterObj();
        let start = new Date();
        let end = new Date();
        
        //one week
        start.setDate(start.getDate() - 7);
        end.setDate(end.getDate() - 1);

        filterObj.startDate = start;
        filterObj.endDate = end;
        filterObj.vehicleList = [];
        return filterObj;
    }

    applyFilter(filterObj) {
        this.setState({ filterObj: filterObj });
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
