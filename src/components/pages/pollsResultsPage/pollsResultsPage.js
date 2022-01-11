import React, {useRef, useLayoutEffect, useState} from 'react';
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";
import {AllPollsTable} from "./allPollsTable";
import { AppContext } from "../../../lib/contextLib";
am4core.useTheme(am4themes_animated);

export const PollsResultsPage = () => {

    const [pollData,setPollData] = useState(null);

    const chart = useRef(null);
    useLayoutEffect(() => {

        if (pollData != null) {
            let x = am4core.create("chartdiv", am4charts.XYChart);

            let answers = pollData.answers;
            let answers_counter = pollData.answers_counter;
            //console.log(pollData);
            //console.log(answers);
            //console.log(answers_counter);

            let categoryAxis = x.xAxes.push(new am4charts.CategoryAxis());
            categoryAxis.dataFields.category = "answer";
            categoryAxis.title.text = "Answers";

            let valueAxis = x.yAxes.push(new am4charts.ValueAxis());
            valueAxis.title.text = "Votes";


            let series = x.series.push(new am4charts.ColumnSeries());
            series.name = "votes";
            //series.columns.template.tooltipText = "Series: {name}\nCategory: {categoryX}\nValue: {valueY}";
            series.columns.template.fill = am4core.color("#4cd20c"); // fill
            series.dataFields.valueY = "votes";
            series.dataFields.categoryX = "answer";

            let count = Object.keys(answers).length;
            let lst = [];
            for (let i = 0; i < count; i++){
                    lst.push({
                        "answer": answers[i],
                        "votes": answers_counter[i]
                    });
                }

            x.data = lst;
            console.log(x.data);

            chart.current = x;

            return () => {
                x.dispose();
                //
            };
        }
  }, [pollData]);

    return(
        <>
            <AppContext.Provider value={{pollData, setPollData}}>
                <AllPollsTable/>
                {pollData != null ? (<h1> data!!</h1>)
            : (<h1> no data...</h1>)}
                <div id="chartdiv" style={{width: "80%", height: "500px"}}/>
            </AppContext.Provider>
        </>
    )
}