$(function(){
	//拿取对应标签元素的引用
	var $li = $('.slide_pics li');
	var len = $li.length;
	var $prev = $('.prev');
	var $next = $('.next');

	//记录将要运动过来的li的下标
	var nowli = 0;

	//记录当前要离开的li的下标
	var prevli = 0;

	var timer = null;

	//进来时将除了第一张图片外，其他的图片放到右边
	$li.not(':first').css({left:460});
	//有多少张图片就生成多少个索引点
	$li.each(function(index){

		var $sli = $('<li>');

		if(index==0)  //让第一个索引点高亮
		{
			$sli.addClass('active');
		}
		//将点添加到对应的元素标签下
		$sli.appendTo('.points')

	})
	//获取索引点的引用
	$points = $('.points li');

	$points.click(function(){
		nowli = $(this).index();  //获取点击点的索引
		if(nowli==prevli){  //点击的和当前的是同一个索引点
			return;
		}
		move();   //不是同一个点就进行图片的变换
		$(this).addClass('active').siblings().removeClass('active'); //设置索引点高亮
	});

	//点击上一个模块的事件
	$prev.click(function(){
		nowli--;
		move();
		$points.eq(nowli).addClass('active').siblings().removeClass('active');
	})
	//点击下一个模块的事件
	$next.click(function(){
		nowli++;
		move();
		$points.eq(nowli).addClass('active').siblings().removeClass('active');
	})
	//当鼠标进入图片，则停止图片的运动
	$('.slide').mouseenter(function() {
		clearInterval(timer);
	});
	//当鼠标离开图片，则开始图片的运动，每4秒运动一次
	$('.slide').mouseleave(function() {
		timer = setInterval(autoplay,4000);
	});
	//定时器
	timer = setInterval(autoplay,4000);
	//没有任何操作的时候，就让图片自动播放
	function autoplay(){
		nowli++;
		move();
		$points.eq(nowli).addClass('active').siblings().removeClass('active');
	}
	//图片变换的操作
	function move(){
		if(nowli<0)
		{
			nowli = len-1;
			prevli = 0;
			$li.eq(nowli).css({left:-460});
			$li.eq(prevli).stop().animate({left:460});
			$li.eq(nowli).stop().animate({left:0});
			prevli=nowli;
			return;
		}
		if(nowli>len-1)
		{
			nowli = 0;
			prevli = len-1;
			$li.eq(nowli).css({left:460});
			$li.eq(prevli).stop().animate({left:-460});
			$li.eq(nowli).stop().animate({left:0});
			prevli=nowli;
			return;
		}
		if(nowli>prevli){

			$li.eq(nowli).css({left:460});
			$li.eq(prevli).stop().animate({left:-460});
		}
		else
		{
			$li.eq(nowli).css({left:-460});
			$li.eq(prevli).stop().animate({left:460});
		}
		$li.eq(nowli).stop().animate({left:0});
		prevli=nowli;
	}
})