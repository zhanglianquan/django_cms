/**
 * Created by Administrator on 2017/7/2.
 */
$(document).ready(function() {
        // 点击验证码,刷新
        $("#get_code_img").click(function() {
            $(".getcode").attr("src", "get_code?rand=" + Math.random());
            return true;

	    });

        // 点击登录
        $("#main_form").submit(function() {
            var username = $(".username").val();
            var password = $(".password").val();
            var verify_code = $(".verify_code").val();
            $.ajax({
                type:"get",
                url:"login?username=" +username+ "&password="+ hex_md5(password) + "&verify_code="+verify_code,
                dataType:"json",
                beforeSend:function(xhr){
                    $(".submit_button").attr("disabled", true);
                },
                success:function(data){
                    console.log(data);
                    if(data.res_type == 1){
                        // 登录成功
                        location.href = "admin";
                    }else{
                        alert(data.res_desc);
                        //刷新验证码
					    $(".getcode").attr("src", "get_code?rand=" + Math.random());
                    }
                },
                complete: function() {
				    $(".submit_button").removeAttr("disabled");
			    }
            });
            return false;
        });

});