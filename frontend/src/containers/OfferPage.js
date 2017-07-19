import React from "react";
import PageBase from "../components/PageBase";
import MonthlyDiscount from "../components/offer/MonthlyDiscount";
import MileageStats from "../components/offer/MileageStats";
import ScoringStats from "../components/offer/ScoringStats";
import { Tabs, Tab } from "material-ui/Tabs";
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';
import axios from 'axios';

const months = [
    'July 2017'
];

class OfferPage extends React.Component {
    constructor() {
        super();
        this.state = this.getDefaultState();
    }

    getDefaultState() {
        return {
            month: 'July 2017',
            allMonths: months
        };
    }

    retrieveMonths() {
        var reqObj = {
            method: "post",
            url: "/api/month",
            headers:{
				"Content-Type": "application/json",
				Authorization: "Bearer " + localStorage.getItem("access_token")            
			}
        };
        axios(reqObj)
            .then(resp => {
                this.setState({ allMonths: resp.data });
            })
            .catch(err => {
                this.setState(this.getDefaultState());
            });
    }

    componentDidMount() {
        this.retrieveMonths();
    }

    getMenuItems() {
        const { allMonths } = this.state;
        return allMonths.map((month) => 
            (<MenuItem
                key = {month}
                value = {month}
                primaryText = {month}
            />)
        );
    }

    handleMonthChange(event, index, value) {
        this.setState( {month: value} );
    }

    render() {
        const month = this.state.month;
        
        return (
            <PageBase title="Discount" navigation="Application / Offer">
                <div>
                    <SelectField 
                        value = {month}
                        onChange = {this.handleMonthChange.bind(this)}
                        floatingLabelText="Month"
                        floatingLabelFixed = {true}
                    >
                        {this.getMenuItems()}
                    </SelectField> 
                    <MonthlyDiscount month = {month}/>
                    <MileageStats month = {month}/>
                    <ScoringStats month = {month}/>
                </div>
            </PageBase>
        );
    }
}

export default OfferPage;
