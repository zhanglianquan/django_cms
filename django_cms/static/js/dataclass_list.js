﻿
$(function() {
	//获取分类数据
	$.getJSON(
		"dataclass_list?type=" + get_menu_param("type") + "&random=" + Math.random(),
		function(data) {
			show_data(data.res_data);
		}
	);
	
	//编辑
	$("#btn_edit").click(function() {
		
		if($("#dataclass").val() != "0") {
			$("#menu_param").val("type:" + get_menu_param("type") + ",id:" + $("#dataclass").val());
			$("#center-column").load("../../static/templates/data_manager/dataclass_add.html?random=" + Math.random());
		}
		else
			alert("请选择分类");
		
		return false;
	});
	
	//删除
	$("#btn_delete").click(function() {
		
		if(confirm("确认删除吗？")) {
			if($("#dataclass").val() != "0") {
				$.getJSON(
					"dataclass_del?id=" + $("#dataclass").val() + "&random=" + Math.random(),
					function(data) {
						alert(data.res_desc);
						$("#dataclass").empty();
						$("#dataclass").append('<option value="0">请选择分类</option>');
						
						//重新获取分类数据
						$.getJSON(
							"dataclass_list?type=" + get_menu_param("type") + "&random=" + Math.random(),
							function(data) {
								show_data(data.res_data);
							}
						);
					}
				);
			}
			else
				alert("请选择分类");
		}
		
		return false;
	});
	
	//添加按钮
	$("#add_btn").click(function() {
		$("#center-column").load("../../static/templates/data_manager/dataclass_add.html?random=" + Math.random());
		return false;
	});	
});
