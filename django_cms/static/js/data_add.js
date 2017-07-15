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
					"data_get?id=" + get_menu_param("id") + "&random=" + Math.random(),
					function(data) {
						$("#title").html("修改数据");
						
						$("#name").val(data.res_data.name);
						$("#dataclass").val(data.res_data.dataclass.id);
						$("#sort").val(data.res_data.sort);
												
						$("#content").val(data.res_data.content);
						// $('#content').ckeditor();
						
						$("#btn_submit").val("更新");
					}
				);
			}
			//else
			//	$('#content').ckeditor();
		}
	);
	
	$("#btn_submit").click(function() {
		
		var name = $("#name").val();
		var sort = $("#sort").val();
		var dataclass = $("#dataclass").val();
		var content = $("#content").val();
		
		var msg = "";
		if(name == "")
			msg += "名称不能为空\n";
		if(dataclass == "0")
			msg += "没有选择分类\n";
		if(msg != "")
			alert(msg);
		else {
			
			var type = get_menu_param("type");
			
			var obj = null;
			if(get_menu_param("id")) {
				var id = get_menu_param("id");
				obj = { id: id, name: name, sort: sort, dataclass_id: dataclass, content: content, type: type, random: Math.random() };
			}
			else
				obj = { name: name, sort: sort, dataclass_id: dataclass, content: content, type: type, random: Math.random() };
		
			$.post(
				"data_add",
				obj,
				function(data) {
					
					if(!get_menu_param("id"))
						$("#menu_param").val("type:" + get_menu_param("type"));
					else {
						var page = 1;
						if(get_menu_param("page"))
							page = get_menu_param("page");
						$("#menu_param").val("type:" + get_menu_param("type") + ",page:" + page);
					}
					
					$("#center-column").load("../../static/templates/data_manager/data_list.html?random=" + Math.random());
				},
				"json"
			);
		}
		
	});
	
});
