		var isAutoLogin = false;
		var firstclick = true;
		function dragDisabled(){
			var textp = document.getElementsByTagName('body')[0];
			textp.ondragenter = function(ev){
			ev.stopPropagation();  
			ev.preventDefault();  
		}  
		textp.ondrop = function(ev){  
			ev.stopPropagation();  
			ev.preventDefault();  
		}  
		textp.ondragover = function(ev){  
			ev.stopPropagation();  
			ev.preventDefault();  
		}  
		textp.ondragleave = function(ev){ 
			ev.stopPropagation();  
			ev.preventDefault(); 
		}
	}
    $(function(){
		
    	dragDisabled();
   		if(isAutoLogin){
            login(isAutoLogin);
			$("#loginform2").hide();
			$("#loginform1").hide();
			$("#logintext").addClass("inputloading");
			$("#textvaluehide").html('   登录中...');
			$("#textvaluehide").css('color','#fff');
			$("#btnimg").hide();
			$("#btn3img").hide();
			$("#btn2img").show();
			$("#loginform3").show();
			$("#btn2img").on({
				"mouseover" : function() {
					$(this).attr("src","image/login/stopovr.png");
				},
				"mouseout" : function() {
					$(this).attr("src","image/login/stopstd.png");
				}, 
				"click" : function() {
					$("#logintext").removeClass("inputloading");
					$("#textvaluehide").html('登陆被取消！');
					$("#textvaluehide").css('color','#E97E23');
					$("#loginform1").hide();
					$("#loginform3").show();
					$("#btn2img").hide();
					$("#btnimg").show();
					firstclick = true;
				}
			});
			$("#btnimg").on({
				"mouseover" : function() {
					$(this).attr("src","image/login/loginover.png");
				},
				"mouseout" : function() {
					$(this).attr("src","image/login/loginstd.png");
				}, 
				"click" : function() {
					login();
					$("#loginform2").hide();
					$("#loginform1").hide();
					$("#logintext").addClass("inputloading");
					$("#textvaluehide").html('   登录中...');
					$("#textvaluehide").css('color','#fff');
					$("#btnimg").hide();
					$("#btn3img").hide();
					$("#btn2img").show();
					$("#loginform3").show();
				}
			});
			
		}else{

					$("#textvalue").val('');
			    $("#name").val('');
			    $("#pass").val('');
				if($("#loginform3").css('display')=='none'){
					if($('.sign').css('display')=='block'){
						$('.sign').css('display','none');
						$('#loginform2').css('display','none');
						$('#loginform1').css('display','block');
						$("#textvalue").focus();
					}else{
						$('.sign').css('display','block');
						$('#loginform1').css('display','none');
						$('#loginform2').css('display','block');
						$("#name").focus();
					}
				} 
				 	
       $("#textvalue").focus();
       $("#btnimg").on({
			"mouseover" : function() {
			   $(this).attr("src","image/login/loginover.png");
			},
			"mouseout" : function() {
			   $(this).attr("src","image/login/loginstd.png");
			}, 
			"click" : function() {
				btn1Onclick($(this));
			}
		});
		$("#btn2img").on({
			"mouseover" : function() {
			   $(this).attr("src","image/login/stopovr.png");
			},
			"mouseout" : function() {
			   $(this).attr("src","image/login/stopstd.png");
			}, 
			"click" : function() {
				cancelLogin();
			   $(this).attr("src","image/login/stopclk.png");
			   $(this).hide();
			   $("#btnimg").show();
			   if($('.sign').css('display')=='block'){
			   		$("#loginform2").show();
			   		$("#name").focus();
			   }else{
			   		$("#loginform1").show();
			   		$("#textvalue").focus();
			   }
			   $("#textvalue").val('');
			   $("#name").val('');
			   $("#pass").val('');
			   $("#loginform3").hide();
			   $("#logintext").removeClass("inputloading");
			   $("#textvalue").focus();
			   firstclick = true;
			}
		});
		$("#btn3img").on({
			"mouseover" : function() {
			   $(this).attr("src","image/login/backover.png");
			},
			"mouseout" : function() {
			   $(this).attr("src","image/login/backstd.png");
			}, 
			"click" : function() {
			   $(this).attr("src","image/login/backclk.png");
			   $(this).hide();
			   $("#btnimg").show();
			   if($('.sign').css('display')=='block'){
			   		$("#loginform2").show();
			   		$("#name").focus();
			   }else{
			   		$("#loginform1").show();
			   		$("#textvalue").focus();
			   }
			   $("#textvalue").val('');
			   $("#name").val('');
			   $("#pass").val('');
			   $("#loginform3").hide();
			   $("#textvalue").focus();
			   firstclick = true;
			}
		});
		$(".chooseBox").on({
			"click":function(){
				$("#textvalue").val('');
			    $("#name").val('');
			    $("#pass").val('');
				if($("#loginform3").css('display')=='none'){
					if($('.sign').css('display')=='block'){
						$('.sign').css('display','none');
						$('#loginform2').css('display','none');
						$('#loginform1').css('display','block');
						$("#textvalue").focus();
					}else{
						$('.sign').css('display','block');
						$('#loginform1').css('display','none');
						$('#loginform2').css('display','block');
						$("#name").focus();
					}
				}
			}
		})
		$(".chooseInfo").on({
			"click":function(){
				$("#textvalue").val('');
			    $("#name").val('');
			    $("#pass").val('');
				if($("#loginform3").css('display')=='none'){
					if($('.sign').css('display')=='block'){
						$('.sign').css('display','none');
						$('#loginform2').css('display','none');
						$('#loginform1').css('display','block');
						$("#textvalue").focus();
					}else{
						$('.sign').css('display','block');
						$('#loginform1').css('display','none');
						$('#loginform2').css('display','block');
						$("#name").focus();
					}
				}
			}
		})
		// $(".img4").on({
		// 	"click":function(){
		// 		getParam();
		// 		$(".setList").css('display','block');
		// 		$(".casetList").css('display','block');
		// 	}
		// })
		$(".img5").on({
			"click":function(){
				var ipaddr = $(this).parent().parent().find('#ipaddr');
				var port = $(this).parent().parent().find('#port');
				if(ipaddr.val() && port.val()){
					port.next().removeClass('glyphicon-remove');
					port.next().css('display','none');
					ipaddr.next().removeClass('glyphicon-remove');
					ipaddr.next().css('display','none');
					if(checkIpFun(ipaddr.val())){
						// alert('ip yes ')
						ipaddr.next().removeClass('glyphicon-remove');
						ipaddr.next().css('display','block');
						if(checkIsPort(port.val())){
							// alert('p yes ')
//							alert('设置成功');
							setParam(ipaddr.val(), port.val(), '');
							port.next().removeClass('glyphicon-remove');
							port.next().css('display','block');
							$(".setList").css('display','none');
						}else{
							alert('端口格式不正确！')
//							$('#port').next().addClass('glyphicon-remove');
							port.next().css('display','block');
							port.val('');
						}
					}else{
						alert('服务器地址格式不正确！')
						ipaddr.next().addClass('glyphicon-remove');
						ipaddr.next().css('display','block');
						ipaddr.val('');
					}
				}else{
					alert('服务器地址或端口为空！')
					port.next().addClass('glyphicon-remove');
					port.next().css('display','block');
					ipaddr.next().addClass('glyphicon-remove');
					ipaddr.next().css('display','block');
				}
				
			}
		})
		$(".img6").on({
			"click":function(){
				$(".setList").css('display','none');
			}
		})
		
		$(".img7").on({
			"click":function(){
				var caipaddr = $(this).parent().parent().find('#caipaddr');
				var ipaddr = $(this).parent().parent().find('#ipaddr');
				var port = $(this).parent().parent().find('#port');
				if(caipaddr.val() && ipaddr.val() && port.val()){
					caipaddr.next().removeClass('glyphicon-remove');
					caipaddr.next().css('display','none');
					ipaddr.next().removeClass('glyphicon-remove');
					ipaddr.next().css('display','none');
					port.next().removeClass('glyphicon-remove');
					port.next().css('display','none');
					if(checkIpFun(caipaddr.val())){
						caipaddr.next().removeClass('glyphicon-remove');
						caipaddr.next().css('display','block');
						if(checkIpFun(ipaddr.val())){
//							alert('ip yes ')
							ipaddr.next().removeClass('glyphicon-remove');
							ipaddr.next().css('display','block');
							if(checkIsPort(port.val())){
//								alert('p yes ')
//								alert('设置成功');
								setParam(ipaddr.val(), port.val(), caipaddr.val());
								port.next().removeClass('glyphicon-remove');
								port.next().css('display','block');
								$(".casetList").css('display','none');
							}else{
//								$('#port').next().addClass('glyphicon-remove');
								port.next().css('display','block');
								port.val('');
							}
						}else{
//							alert('ip no ')
							ipaddr.next().addClass('glyphicon-remove');
							ipaddr.next().css('display','block');
							ipaddr.val('');
						}
					} else {
						caipaddr.next().addClass('glyphicon-remove');
						caipaddr.next().css('display','block');
						caipaddr.val('');
					}
				}else{
//					alert('kong');
					caipaddr.next().addClass('glyphicon-remove');
					caipaddr.next().css('display','block');
					port.next().addClass('glyphicon-remove');
					port.next().css('display','block');
					ipaddr.next().addClass('glyphicon-remove');
					ipaddr.next().css('display','block');
				}
				
			}
		})
		
		$(".img8").on({
			"click":function(){
				$(".casetList").css('display','none');
			}
		})
		
		$("#caipaddr").on({
			"click":function(){
				$(this).next().removeClass('glyphicon-remove');
				$(this).next().css('display','none');
			}
		})
		$("#ipaddr").on({
			"click":function(){
				$(this).next().removeClass('glyphicon-remove');
				$(this).next().css('display','none');
			}
		})
		$("#port").on({
			"click":function(){
				$(this).next().removeClass('glyphicon-remove');
				$(this).next().css('display','none');
			}
		})
		
	}
    });
    function btn1Onclick(o){
    	if($('.sign').css('display')=='none'){
////			if(!$('#textvalue').val()){
////				o.attr("src","qrc:/login/login/image/login/loginclk.png");
////			    o.hide();
////				$("#textvaluehide").val('PIN码不能为空');
////				$("#textvaluehide").css('color','#E97E23');
////				$("#loginform1").hide();
////				$("#loginform3").show();
////				$("#btn3img").show();
////			}else{
				login();
				o.attr("src","image/login/loginclk.png");
			    o.hide();
			    $("#loginform2").hide();
			    $("#loginform1").hide();
			    $("#logintext").addClass("inputloading");
			    $("#textvaluehide").html('   登录中...');
			    $("#textvaluehide").css('color','#fff');
			    $("#btn2img").show();
			    $("#loginform3").show();
////			}
		}else{
			if(!$('#name').val()){
				o.attr("src","image/login/loginclk.png");
			    o.hide();
				$("#textvaluehide").html('用户名不能为空');
				$("#textvaluehide").css('color','#E97E23');
				$("#loginform2").hide();
				$("#loginform3").show();
				$("#btn3img").show();
			}else{
				if(!$('#pass').val()){
					o.attr("src","image/login/loginclk.png");
			    	o.hide();
					$("#textvaluehide").html('密码不能为空');
					$("#textvaluehide").css('color','#E97E23');
					$("#loginform2").hide();
					$("#loginform3").show();
					$("#btn3img").show();
				}else{
					o.attr("src","image/login/loginclk.png");
				    o.hide();
				    $("#btn2img").show();
				    $("#loginform2").hide();
				    $("#loginform1").hide();
				    $("#logintext").addClass("inputloading");
				    $("#textvaluehide").html('   登录中...');
				    $("#textvaluehide").css('color','#fff');
				    $("#loginform3").show();
					login();
				}
			}
		}
    }
    function clear(){
        $("#logintext").removeClass("inputloading");
    }
    function wingText(a){
		if(!isAutoLogin){
			clear();
			$("#textvaluehide").html(a);
			$("#textvaluehide").css("color",'#E97E23');
			$("#btn2img").hide();
			$("#btn3img").show();
			$("#btn1img").hide();
		}else{    	
        clear();
        $("#textvaluehide").html(a);
        $("#textvaluehide").css("color",'#E97E23');
				$("#btnimg").show();
				$("#btn2img").hide();
				$("#btn3img").hide();
    }
  }
    function checkIpFun(nasip){
	    var exp=/^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
		var reg = nasip.match(exp);
		if(reg==null){
			return false;
		}else{
			return true;
		}
	}
    function checkIsPort(){
    	var port = $("#port").val();
    	if(isNumber(port)&&port<65536){
    		return true;
    	}else{
    		return false;
    	}
	}
	function isNumber(s){
		var regu = "^[0-9]+$";
		var re = new RegExp(regu);
		if (s.search(re) != -1) {
			return true;
		} else {
			return false;
		}
	}
	function enterkey() 
	{ 
		e = event.keyCode; 
		if (e==13 && firstclick){
			firstclick = false;
//		alert(e);
			btn1Onclick($('#btnimg'));
			$('#pass').val('');
			event.returnValue= false; // 取消此事件的默认操作 
		} 
	}
