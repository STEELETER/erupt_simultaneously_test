
function login(flag)
{
    if(flag){
            external.LoginFromAccount($.md5('hui_yi_ip'), '111111');
        }
    else {
            if($(".sign").css('display')=='none')
            {
                var pwd = document.getElementById("textvalue");
                external.Login(pwd.value);
            }
            else
            {
                var user=document.getElementById("name");
                var pwd = document.getElementById("pass");

                external.LoginFromAccount(user.value, $.md5(pwd.value));
            }
        }

//	alert("pwd="+pwd.value);
}

function cancelLogin()
{
	external.CancelLogin();	
}

function showMin()
{
	external.ShowMin();
}

function closeWin()
{
	external.CloseWindow();
}

function showErrMsg(msg)
{
    // alert(msg)
	// var msg = external.GetPropMsg();
//	alert("errmsg="+msg);
	wingText(msg);
}

function setParam(ip, s_port, ca_ip)
{
	external.SetServerInfo(ip, s_port, ca_ip);
	
}

function getFocus(){
	external.ActiveWindow();
}

function setFocus(){
	$('#hidearea').focus();
}

function getParam(s_ip,s_port,s_caip){
	$(".setList").css('display','block');
	$(".casetList").css('display','block');

	document.getElementById("ipaddr").value=s_ip;
	document.getElementById("port").value=s_port;
	if(s_caip != null && s_caip != ''){
		$('#caipaddr').val(s_caip);
	}
}