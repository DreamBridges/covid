//初始化echarts实例
var ec_center = echarts.init(document.getElementById("c2"),"white");
var mydata = []
var optionMap = {
		title: {
			text: '',
			subtext: '',
			x: 'left'
		},
		tooltip: {
			trigger: 'item'
		},
		//左侧小导航图标
		visualMap: {
			show: true,
			x: 'left',
			y: 'bottom',
			textStyle: {
				fontSize: 8,
				color: "#ffffff"
			},
			splitList: [{
					start: 1,
					end: 9
				},
				{
					start: 10,
					end: 99
				},
				{
					start: 100,
					end: 499
				},
				{
					start: 500,
					end: 999
				},
				{
					start: 1000,
					end: 4999
				},
				{
					start: 5000
				}
			],
			color: ['#af000b','#f60000','#ff3636','#fc6d76','#fab6bb','#feeeed']
		},

			//配置属性
			series: [{
				name: '累积确诊人数',
				type: 'map',
				mapType: 'china',
				roam: false,
				itemStyle: {
					normal: {
						borderWidth: .5,
						borderColor: '#009fe8',
						areaColor: '#ffefd5'
					},
					emphasis: {
						borderWidth: .5,
						borderColor: '#4b0082',
						areaColor: '#fff'
					}
				},
				label: {
					normal: {
						show: true, //省份名称
						fontSize: 8
					},
					emphasis: {
						show: true,
						fontSize: 8
					}
				},
				data: mydata //数据
			}]
		};

		//使用制定的配置项和数据显示图表
		ec_center.setOption(optionMap);
