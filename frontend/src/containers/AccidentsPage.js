import React from "react";
import PageBase from "../components/PageBase";
import Divider from 'material-ui/Divider';
import FilterDrawer, { FilterObj } from "../components/filter/FilterDrawer";
import ClaimsUploader from "../components/accidents-claims/accidents/ClaimsUploader";
import AccidentClaimListing from "../components/accidents-claims/accidents/AccidentClaimListing";

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
                        <AccidentClaimListing/>
                    </div>
                </div>
            </PageBase>
        );
    }
}

export default AccidentsPage;
