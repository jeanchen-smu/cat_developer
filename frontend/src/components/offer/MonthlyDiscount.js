import React, {PropTypes} from "react";
import {
    cyan600,
    pink600,
    purple600,
    orange600,
    red600,
    blue600
} from "material-ui/styles/colors";
import { Card, CardHeader, CardText } from "material-ui/Card";
import Assignment from "material-ui/svg-icons/action/assignment";
import SwapCalls from "material-ui/svg-icons/communication/swap-calls";
import Equalizer from "material-ui/svg-icons/av/equalizer";
import SwapHoriz from "material-ui/svg-icons/action/swap-horiz";
import AssignmentTurnedIn from "material-ui/svg-icons/action/assignment-turned-in";
import MonetizationOn from "material-ui/svg-icons/editor/monetization-on";
import InfoBox from "../dashboard/InfoBox";
import axios from "axios";

class MonthlyDiscount extends React.Component {
    constructor(props) {
        super(props);
        this.state = this.getDefaultState();
    }

    getDefaultState() {
        return {
            claims: 0,
            mileage: 0,
            score: 0,
            crossSell: false,
            pilotProgram: false,
            rebate: 0
        };
    }

    getMonthlyDiscount() {
        var reqObj = {
            method: "post",
            url: "/api/monthly_discount",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + localStorage.getItem("access_token")
            },
            data: {
                month: this.props.month
            }
        };
        axios(reqObj)
            .then(resp => {
                console.log(resp.data)
                this.setState({
                    claims: resp.data.claims,
                    mileage: resp.data.mileage,
                    score: resp.data.score,
                    crossSell: resp.data.crossSell,
                    pilotProgram: resp.data.pilotProgram,
                    rebate: resp.data.rebate
                });
            })
            .catch(err => {
                this.setState(this.getDefaultState());
            });
    }

    componentDidMount() {
        this.getMonthlyDiscount();
    }

    componentWillReceiveProps(nextProps){
        this.getMonthlyDiscount();
    }

    render() {
        return (
            <Card>
                <CardHeader
                    title="Monthly Rebate"
                    actAsExpander={true}
                    showExpandableButton={true}
                />
                <CardText expandable={false}>
                    <div className="row">
                        <div className="col-xs-12 col-sm-6 col-md-4 col-lg-4 m-b-15 ">
                            <InfoBox
                                Icon={Assignment}
                                color={orange600}
                                title="Claims"
                                value={this.state.claims.toString()}
                            />
                        </div>

                        <div className="col-xs-12 col-sm-6 col-md-4 col-lg-4 m-b-15 ">
                            <InfoBox
                                Icon={SwapCalls}
                                color={pink600}
                                title="Average Mileage"
                                value={this.state.mileage.toFixed(2) + " km"}
                            />
                        </div>

                        <div className="col-xs-12 col-sm-6 col-md-4 col-lg-4 m-b-15 ">
                            <InfoBox
                                Icon={Equalizer}
                                color={purple600}
                                title="Driver Score"
                                value={(this.state.score.toFixed(2)*100).toString()}
                            />
                        </div>

                        <div className="col-xs-12 col-sm-6 col-md-4 col-lg-4 m-b-15 ">
                            <InfoBox
                                Icon={SwapHoriz}
                                color={red600}
                                title="Cross-sell"
                                value={this.state.crossSell?"Yes":"No"}
                            />
                        </div>

                        <div className="col-xs-12 col-sm-6 col-md-4 col-lg-4 m-b-15 ">
                            <InfoBox
                                Icon={AssignmentTurnedIn}
                                color={cyan600}
                                title="Pilot Program"
                                value={this.state.pilotProgram?"Yes":"No"}
                            />
                        </div>

                        <div className="col-xs-12 col-sm-6 col-md-4 col-lg-4 m-b-15 ">
                            <InfoBox
                                Icon={MonetizationOn}
                                color={blue600}
                                title="Rebates"
                                value={"$ " + this.state.rebate.toString()}
                            />
                        </div>
                    </div>

                </CardText>
            </Card>
        );
    }
}

MonthlyDiscount.propTypes = {
	month: PropTypes.string
};

export default MonthlyDiscount;