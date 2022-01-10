/**
 * Created
 */

var ec_right1 = echarts.init(document.getElementById('r1'),"dark");
var ec_right1_option = {
	//标题样式
	title : {
	    text : "高风险地区排名TOP5",
	    textStyle : {
	        color : 'white'
	    },
	    left : 'left'
	},
	  color: ['#3398DB'],
	    tooltip: {
	        trigger: 'axis',
	        axisPointer: {            // 坐标轴指示器，坐标轴触发有效
	            type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
	        }
	    },

    xAxis: {
        type: 'category',
		 //设置轴线的属性
          //           axisLine:{
          //               lineStyle:{
          //                   color:'#fff'
          //                 //  width:8//这里是为了突出显示加上的
          //               }
          //           },
        data: [
"长沙",
"岳阳",
"株洲",
"邵阳",
"常德"
]
    },
    yAxis: {
        type: 'value',
		//设置轴线的属性
                     axisLine:{
                        lineStyle:{
                            color:'#fff'
							// type:'solid'
                           // width:8//这里是为了突出显示加上的
                        }
                    }
    },
    series: [{
        // data: [],
		 data: [],
        type: 'bar',
		barMaxWidth:"50%"
    }]
};


ec_right1.setOption(ec_right1_option);

