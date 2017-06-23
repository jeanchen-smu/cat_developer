import React from "react";
import PageBase from "../components/PageBase";
import FilterDrawer, { FilterObj } from "../components/filter/FilterDrawer";
import RankTable from "../components/ranking/RankTable";
import axios from "axios";

class RankPage extends React.Component {
	constructor() {
		super();
		//alert('constructor');
		let filterObj = new FilterObj();
		filterObj.startDate = new Date();
		filterObj.endDate = new Date();

		this.state = {
			sortAscending: true,
			filterObj: filterObj,
			rankingData: []
		};
	}

	componentDidMount() {
		this.refreshRankingData();
	}

	getRankingReqObj(){
		return {
            method: "get",
            url: "/api/rank",
			headers:{
				Authorization: "Bearer " + localStorage.getItem("access_token")            
			}, 
			params: {
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
				alert("Fetch error : " + err);
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
