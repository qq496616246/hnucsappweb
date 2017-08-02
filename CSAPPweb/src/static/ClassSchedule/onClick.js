// JavaScript Document

$(function(){
	
	//界面切换效果
	
	$('#b0').click(function(){
		$('#menu1').fadeOut(250,"swing",function(){
			$('#menu2').fadeIn(250,"swing");
		});
	});
		
	$('#alterb0').click(function(){
		$('#menu2').fadeOut(250,"swing",function(){
			$('#menu1').fadeIn(250,"swing");
		});
	});
	
	//关闭查询和发布信息界面
	
	$('#gray-canvas').click(function(){
		$('#dialog').fadeOut(50,"linear",function(){
			$('#gray-canvas').fadeOut(50,"linear",function(){
				$('#class-info').hide();
				$('#class-info li').remove();
				$('#class-setting').hide();
				$('#class-setting option').remove();
				$('#messages').val("");
				$('#class-setting li').remove();
			});
		});
	});
	
	$('#messages').click(function(){
		if ($(this).attr("class")=="text-cur")
		  {
		    $(this).attr("class","text-nocur");
		    $('#setting-frame').height(60);
		  }
		  else
		  {
		    $(this).attr("class","text-cur");
		    $('#setting-frame').height(170);
		  }

	})
	
	//弹出查询和发布信息界面。1—查询；2—发布
	
	function displaydialog(type, title){
		if(type==1){
			$('#class-info h1').html(title);
			$('#class-info ul').append($('<li>阿贾克斯很累了，阿贾克斯龟速加载中。。。</li>'))
			$('#class-info').show();
		}
		else if(type==2){
			$('#class-setting h1').html(title);
			$('#class-setting ul').append($('<li>阿贾克斯很累了，阿贾克斯龟速加载中。。。</li>'))
			$('#class-setting').show();
		}
		
		$('#gray-canvas').fadeIn(100,"linear",function(){
			$('#dialog').fadeIn(100,"linear");
		});
	}
	
	//ajax查询
	
	function ajaxQuery(choice){
		$.get("/ClassSchedule/ajaxQuery",{opt : choice},function(data){
			$('#class-info li').remove();
			if(data.opt=='s'){
				$.each(data,function(key,value){
					if(key!='opt'){
						$('#class-info ul').append($('<li>'+value+'</li>'));
					}
				});
			}
			else if(data.opt=='t'){
				$.each(data,function(key,value){
					if(key!='opt'){
						$('#class-info ul').append($('<li>'+key+'：</li>'));
						$.each(value,function(key1,value1){
							$('#class-info ul').append($('<li>'+value1+'</li>'));
						});
					}		
				});
			}		
		});
	}
	
	//ajax查询（用于发布菜单）
	function ajaxQuery2(choice){
		$.get("/ClassSchedule/ajaxQuery2",{opt : choice},function(data){
			$.each(data,function(key,value){
				if(key=="class_name"){
					$.each(value,function(key1,value1){
						$('#class-setting select').append($('<option>'+value1+'</option>'));
					});
				}
				else if(key=="message"){
					$('#class-setting li').remove();
					$.each(value,function(key2,value2){
						$('#class-setting ul').append($('<li>'+value2+'<span class="btn btn-radius-del del" style="float:right">X</span></li>'));
					});
				}
			});
			
		});
	}
	
	//课程信息查询按键监听
	
	$('#b1').click(function(){
		displaydialog(1,"课程通知：");
		ajaxQuery('1');
	});
	
	$('#b2').click(function(){
		displaydialog(1,"讨论课安排：");
		ajaxQuery('2');
	});
	
	$('#b3').click(function(){
		displaydialog(1,"实验课安排：");
		ajaxQuery('3');
	});
	
	$('#b4').click(function(){
		displaydialog(1,"大班课安排：");
		ajaxQuery('4');
	});
	
	//课程信息发布按键监听	

	$('#alterb1').click(function(){
		displaydialog(2,"课程通知：");
		ajaxQuery2('1');
	});
	
	$('#alterb2').click(function(){
		displaydialog(2,"讨论课安排：");
		ajaxQuery2('2');
	});
	
	$('#alterb3').click(function(){
		displaydialog(2,"实验课安排：");
		ajaxQuery2('3');
	});
	
	$('#alterb4').click(function(){
		displaydialog(2,"大班课安排：");
		ajaxQuery2('4');
	});

});