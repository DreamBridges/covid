function gettime() {
	$.ajax({
		url: "/time",
		timeout: 10000, //超时时间设置为10秒；
		success: function(data) {
			$("#time").html(data)
		},
		error: function(xhr, type, errorThrown) {

		}
	});
}

function get_c1_data() {
	$.ajax({
		url: "/c1",
		success: function(data) {
			$(".num h1").eq(0).html(data.confirm);
			$(".num h1").eq(1).html(data.confirm_now);
			$(".num h1").eq(2).html(data.heal);
			$(".num h1").eq(3).html(data.dead);
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}
function get_c2_data() {
	$.ajax({
		url:"/c2",
		success: function(data) {
			optionMap.series[0].data = data.data
			ec_center.setOption(optionMap)
		},
		error: function(xhr, type, errorThrown) {
		
		}
	})
}

function get_l1_data() {
	$.ajax({
		url:"/l1",
		success: function(data) {
			option_left2.xAxis.data = data.day
			option_left2.series[0].data = data.confirm_add
			option_left2.series[1].data = data.heal_add
			ec_left2.setOption(option_left2)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}



function get_l2_data() {
	$.ajax({
		url:"/l2",
		success: function(data) {
			var update_time = data.update_time
            var details = data.details
            var risk = data.risk
             $("#l2 .ts").html("截至时间：" + update_time)
            var s =""
            for(var i in details){
                if (risk[i] == "高风险"){
                     s += "<li><span class='high_risk'>高风险\t\t</span>"+ details[i] + "</li>"
                }else{
                     s += "<li><span class='middle_risk'>中风险\t\t</span>"+ details[i] + "</li>"
                }
            }
             $("#risk_wrapper_li1 ul").html(s)
            start_roll()
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}


function get_r1_data() {
	$.ajax({
		url:"/r1",
		success: function(data) {
			option_right1.xAxis.data = data.province_name
			option_right1.series[0].data = data.total_confirm
			ec_right1.setOption(option_right1)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}


function get_r2_data() {
	$.ajax({
		url:"/r2",
		success: function(data) {
			option_right2.series[0].data = data.kws
			ec_right2.setOption(option_right2)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}

gettime()
get_c1_data()
get_c2_data()
get_l1_data()
get_l2_data()
get_r1_data()
get_r2_data()
setInterval(gettime, 1000)
setInterval(get_c1_data, 1000*10)
setInterval(get_c2_data, 1000*10)
setInterval(get_l1_data, 1000*10)
setInterval(get_l1_data, 1000*10)
setInterval(get_r1_data, 1000*10)
setInterval(get_r1_data, 1000*10)
