var ec_right1 = echarts.init(document.getElementById("r1"),"white");

option_right1 = {
	title: {
		text: '确诊省份/地区TOP5',
		textStyle: {
			color: 'white'
		},
		left: 'left'
	},
	grid: {
		left: '3%',
		right: '4%',
		bottom: '3%',
		containLabel: true
	  },
	color: ['#3398DB'],
	tooltip: {
		trigger: 'axis',
		axisPointer: {
			type: 'shadow'
		}
	},
	//全局字体样式
	// textStyle: {
	// 	fontFamily: 'PingFangSC-Medium',
	// 	fontSize: 12,
	// 	color: '#858E96',
	// 	lineHeight: 12
	// },
	xAxis: {
		type: 'category',
		//                              scale:true,
		data: [],
		axisLine: {
			lineStyle: {
				// 设置x轴颜色
				color: '#ffffff'
			}
		},
	},
	yAxis: {
		type: 'value',
		axisLine: {
			lineStyle: {
				// 设置x轴颜色
				color: '#ffffff'
				}
			},
		},
	series: [{
		type: 'bar',
		data: [],
		barMaxWidth: "50%"
	}]
};
ec_right1.setOption(option_right1)
