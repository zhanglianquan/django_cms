﻿
$(function() {
	
	//获取分类数据
	$.getJSON(
		"dataclass_list?type=" + get_menu_param("type") + "&random=" + Math.random(),
		function(data) {
			show_data(data.res_data);
			if(get_menu_param("id")) {
				//编辑状态
				$.getJSON(
					"dataclass_get?id=" + get_menu_param("id") + "&random=" + Math.random(),
					function(data) {
						$("#title").html("修改分类");
						
						$("#name").val(data.res_data.name);
						$("#dataclass").val(data.res_data.parent_id);
						$("#sort").val(data.res_data.sort);
						
						$("#btn_submit").val("更新");
					}
				);
			}
		}
	);
	
	//提交按钮
	$("#btn_submit").click(function() {
		
		var msg = "";
		if($("#name").val() == "")
			msg += "名称不能为空\n";
		
		if(msg != "")
			alert(msg);
		else {
			var url = null;
			if(get_menu_param("id"))
				url = "dataclass_add?id=" + get_menu_param("id") + "&name=" + encodeURIComponent($("#name").val()) + "&parent_id=" + $("#dataclass").val() + "&sort=" + $("#sort").val() + "&type=" + get_menu_param("type") + "&random=" + Math.random();
			else
				url = "dataclass_add?name=" + encodeURIComponent($("#name").val()) + "&parent_id=" + $("#dataclass").val() + "&sort=" + $("#sort").val() + "&type=" + get_menu_param("type") + "&random=" + Math.random();
			
			$.getJSON(
				url,
				function(data) {
					
					if(data.code == 0)
						alert(data.res_desc);
					else {
						//重置参数
						$("#menu_param").val("type:" + get_menu_param("type"));
						$("#center-column").load("../../static/templates/data_manager/dataclass_list.html?random=" + Math.random());
					}
						
				}
			);
		}	
		
		return false;
	});	
});
