import React from "react";
import PageBase from "../components/PageBase";
import FilterDrawer, { FilterObj } from "../components/filter/FilterDrawer";
import EventsTimeline from "../components/accidents-claims/analysis/EventsTimeline";
import VehicleDetails from "../components/accidents-claims/analysis/VehicleDetails";
//import axios from "axios";

class AccidentAnalysis extends React.Component {
    constructor() {
        super();
        this.state = {
            filterObj: this.defaultFilter(1, 1)
        };
    }

    defaultFilter(startOffset, endOffset) {
        let start = new Date();
        start.setDate(start.getDate() - startOffset);

        let end = new Date();
        end.setDate(end.getDate() - endOffset);

        let filterObj = new FilterObj();
        filterObj.startDate = start;
        filterObj.endDate = end;
        filterObj.vehicleList = [];
        return filterObj;
    }

    applyFilter(filterObj) {
        this.setState({ fiterObj: filterObj });
    }

    render() {
        return (
            <PageBase title="Detailed analysis of accidents" navigation="Application / Accident Analysis">
                <div>
                    <div>
                        <FilterDrawer filterObj={this.state.filterObj} applyFilter={this.applyFilter.bind(this)} />
                    </div>
                    <div>
                        <VehicleDetails />
                        <EventsTimeline />
                    </div>
                </div>
            </PageBase>
        );
    }
}

export default AccidentAnalysis;
