/**
 * Created 蓝羽教学 on 2020/5/3.
 */
var ec_left1 = echarts.init(document.getElementById('l1'), "dark");
var ec_left1_Option = {
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
		data: ['累计确诊', '现有疑似', "累计治愈", "累计死亡"],
		left: "right",
        textStyle: {
			color: '#fff'
		}

	},
	//标题样式
	title: {
		text: "全国累计趋势",
		textStyle: {
			color: '#fff'
		},
		left: 'left'    //控制标题样式 居左
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
		//
                    /*改变x轴颜色*/
         axisLine: {
                        lineStyle: {
                            color: '#fff',
                            width: 1 //这里是为了突出显示加上的
                        }
                    },
		data: []

	}],
	yAxis: [{
		type: 'value',
		//y轴字体设置
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
		//y轴线设置显示
		axisLine: {
			show: true,
            // 改变X轴颜色
            lineStyle: {
                            color: '#fff',
                            width: 1  //这里是为了突出显示加上的
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
		name: "累计确诊",
		type: 'line',
		smooth: true,
		data: [260,404,555]
	}, {
		name: "现有疑似",
		type: 'line',
		smooth: true,
		data: [54,33,4234]}
	, {
		name: "累计治愈",
		type: 'line',
		smooth: true,
		data: [5,4,8]
	}, {
		name: "累计死亡",
		type: 'line',
		smooth: true,
		data: [45,55,33]
	}]
};

ec_left1.setOption(ec_left1_Option)
