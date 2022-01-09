import React, { useRef, useLayoutEffect } from 'react';
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";
import {AllPollsTable} from "./allPollsTable";

am4core.useTheme(am4themes_animated);

export const PollsResultsPage = () => {

    const chart = useRef(null);
    useLayoutEffect(() => {
    let x = am4core.create("chartdiv", am4charts.XYChart);

        x.data = [{
            "country": "Lithuania",
            "litres": 501
        }, {
            "country": "Czechia",
            "litres": 301
        }, {
            "country": "Ireland",
            "litres": 201
        }, {
            "country": "Germany",
            "litres": 165
        }, {
            "country": "Australia",
            "litres": 139
        }, {
            "country": "Austria",
            "litres": 128
        }, {
            "country": "UK",
            "litres": 99
        }, {
            "country": "Belgium",
            "litres": 60
        }, {
            "country": "The Netherlands",
            "litres": 50
        }];


    let categoryAxis = x.xAxes.push(new am4charts.CategoryAxis());
    categoryAxis.dataFields.category = "country";
    categoryAxis.title.text = "Countries";

    let valueAxis = x.yAxes.push(new am4charts.ValueAxis());
    valueAxis.title.text = "Litres sold (M)";


    let series = x.series.push(new am4charts.ColumnSeries());
    series.name = "Sales";
    //series.columns.template.tooltipText = "Series: {name}\nCategory: {categoryX}\nValue: {valueY}";
    series.columns.template.fill = am4core.color("#4cd20c"); // fill
    series.dataFields.valueY = "litres";
    series.dataFields.categoryX = "country";

    chart.current = x;

    return () => {
      x.dispose();
      //
    };
  }, []);

    return(
        <>
            <AllPollsTable/>
            <div id="chartdiv" style={{width: "80%", height: "500px"}}/>
        </>
    )
}