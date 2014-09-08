$(function(){
	var ru = window.location.href;
	var isReload = true; //ÊÇ·ñË¢ÐÂÒ³Ãæ
	//login
	FCLogin.initilize({   
		appId:"1017",   
		secretKey:"8e2ad6ed333f378a83de9afbe19cec65",   
		ru:ru,    
		sc:function(ret){
			$(".uname a").html(ret.uniqname);
			$(".login_before").hide();
			$(".login_after").show();
			$.getScript('/common/modules/passport/js/login_success.php?from=fpp', function(){
				if(isReload){
					window.location.reload();
				}
			});
		},    
		fc:function(){
			
		}
	}); 
	
	//ÔØÈëÊ±ÅÐ¶ÏµÇÂ¼×´Ì¬ 
	FCLogin.checkUserStatus(function(ret){  
		//console.log(ret);
		if(ret){
			$(".uname a").html(ret.nickName);
			$(".login_before").hide();
			$(".login_after").show();
		}else{        
			//logOutCallBack();  
		} 
	}); 
	
	//logout
	$(".logout").click(function(){
		FCLogin.logout();
		$(".login_after").hide();
		$(".login_before").show();
	});
	
	$(".login_before .input_c").click(function(){
		FCLogin.open();
	});	
})