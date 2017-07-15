
var id;

$(function() {
		
	//获取参数
	id = get_menu_param("id");
	
	$.getJSON(
		"art_single_get?id=" + id + "&random=" + Math.random(),
		function(data) {
			$("#content").val(data.res_data.content);
			$('#content').ckeditor();
			
			$("#art_name").html(data.res_data.name);
			
			$("#btn_submit").click(function() {
				$.post(
					"art_single_update",
					{ id: id, content: $("#content").val(), random: Math.random() },
					function(data) {
						alert(data.desc);
					},
					"json"
				);
			});
		}
	);
	
});
