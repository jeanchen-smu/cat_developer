import React from "react";
import PageBase from "../components/PageBase";
import FilterDrawer, { FilterObj } from "../components/filter/FilterDrawer";
import ClaimsUploader from "../components/accidents-claims/accidents/ClaimsUploader";

class AccidentsPage extends React.Component {
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
            <PageBase title="Accidents and claims" navigation="Application / Accidents">
                <div>
                    <div>
                        <FilterDrawer filterObj={this.state.filterObj} applyFilter={this.applyFilter.bind(this)} />
                    </div>
                    <div>
                        <ClaimsUploader/>
                    </div>
                </div>
            </PageBase>
        );
    }
}

export default AccidentsPage;
