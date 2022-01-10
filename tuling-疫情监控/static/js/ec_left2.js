/**
 * Created 夏洛教学.
 */
var ec_left2 = echarts.init(document.getElementById('l2'), "dark");
var ec_left2_Option = {
	tooltip: {
		trigger: 'axis',
		//指示器
		axisPointer: {
			type: 'line',
			lineStyle: {
				color: '#7171C6'
			}
		}
	},

	legend: {
		data: ['新增确诊', '新增疑似'],
		left: "right",
		 textStyle: {
			color: '#fff'
		}
	},
	//标题样式
	title: {
		text: "全国新增趋势",
		textStyle: {
			color: '#fff',
		},
		left: 'left'
	},
	//图形位置
	grid: {
		left: '4%',
		right: '6%',
		bottom: '4%',
		top: 50,
		containLabel: true
	},
	xAxis: [{
		type: 'category',
		//x轴坐标点开始与结束点位置都不在最边缘
		// boundaryGap : true,
           /*改变x轴颜色*/
		axisLine: {
                        lineStyle: {
                            color: '#fff',
                            width: 1 //这里是为了突出显示加上的
                        }
                    },
		data: ['01-20','01-21','01-22']
	}],

	yAxis: [{
		type: 'value',
		//y轴字体设置

		//y轴线设置显示
		axisLine: {
			show: true,
			 lineStyle: {
				color: '#fff',
				width: 1 //这里是为了突出显示加上的
			}
		},
		axisLabel: {
			show: true,
			color: '#fff',
			fontSize: 12,
			formatter: function(value) {
				if (value >= 1000) {
					value = value / 1000 + 'k';
				}
				return value;
			}
		},
		//与x轴平行的线样式
		splitLine: {
			show: true,
			lineStyle: {
				color: '#17273B',
				width: 1,
				type: 'solid',
			}
		}
	}],

	series: [{
		name: "新增确诊",
		type: 'line',
		smooth: true,
		data: [111,222,333]
	}, {
		name: "新增疑似",
		type: 'line',
		smooth: true,
		data: [444,555,666]
	}]
};

ec_left2.setOption(ec_left2_Option);

