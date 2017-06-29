import React from "react";
import PageBase from "../components/PageBase";
import FilterDrawer, { FilterObj } from "../components/filter/FilterDrawer";
import RankTable from "../components/ranking/RankTable";
import axios from "axios";

class RankPage extends React.Component {
	constructor() {
		super();
		this.state = {
			sortAscending: true,
			filterObj: this.defaultFilter(1,1),
			rankingData: []
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

	componentDidMount() {
		this.refreshRankingData();
	}

	getRankingReqObj(){
		return {
            method: "post",
            url: "/api/rank",
			headers:{
				"Content-Type": "application/json",
				Authorization: "Bearer " + localStorage.getItem("access_token")            
			}, 
			data: {
				startDate: this.state.filterObj.startDate,
				endDate: this.state.filterObj.endDate
			}	
        };
	}

	refreshRankingData() {
		var reqObj = this.getRankingReqObj();
		axios(reqObj)
			.then(resp => {
				this.setState({ rankingData: resp.data });
			})
			.catch(err => {
				this.setState({ rankingData: [] });
			});
	}

	applyFilter(filterObj) {
		this.setState({ fiterObj: filterObj });
		this.refreshRankingData();
	}

	render() {
		return (
			<PageBase
				title="Ranking of Vehicles"
				navigation="Application / Ranking"
			>
				<div>
					<div>
						<FilterDrawer
							filterObj={this.state.filterObj}
							applyFilter={this.applyFilter.bind(this)}
						/>
					</div>
					<div>
						<RankTable rankingData={this.state.rankingData} />
					</div>
				</div>
			</PageBase>
		);
	}
}

export default RankPage;
