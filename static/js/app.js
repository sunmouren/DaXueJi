$(function(){
    // 懒加载
    $("img").addClass("lazy");
    $("img.lazy").fadeIn("2000");
    
    // 提示
    $('[data-toggle="tooltip"]').tooltip();
    $(".share-weixin").click(function(){
        $('#share-wechat').modal('show');
    });
    /*关注*/
    $("a[id^='attentto']").hover(function(){
        if ($(this).hasClass("btn-default") || $(this).hasClass("following")){
    	    $(this).html('<i class="fa fa-times"></i><span> 取消关注</span>');
    	}
    },function(){
    	if ($(this).hasClass("btn-default") || $(this).hasClass("following")){
    	    $(this).html('<i class="fa fa-check"></i><span> 已关注</span>');
    	}
    });
    // /*投稿*/
    // $("a[id^='taogaoart']").hover(function(){
    //     if ($(this).hasClass("btn-default")){
    // 	    $(this).html('<i class="fa fa-times"></i><span> 取消投稿</span>');
    // 	}
    // 	tips('投稿', 'success');
    // },function(){
    // 	if ($(this).hasClass("btn-default")){
    // 	    $(this).html('<i class="fa fa-check"></i><span> 已投稿</span>');
    // 	}
    // });
});

/**
 * 页面小提示
 * @param $msg 提示信息
 * @param $type 提示类型:'info', 'success', 'warning', 'danger'
 * @param $icon 图标，例如：'fa fa-user' 或 'glyphicon glyphicon-warning-sign'
 * @param $from 'top' 或 'bottom'
 * @param $align 'left', 'right', 'center'
 * @author CaiWeiMing <314013107@qq.com>
 */
var tips = function ($msg, $type, $icon, $from, $align) {
	$type  = $type || 'info';
	$from  = $from || 'top';
	$align = $align || 'center';
	$enter = $type == 'success' ? 'animated fadeInUp' : 'animated shake';

	jQuery.notify({
		icon: $icon,
		message: $msg
	},
	{
		element: 'body',
		type: $type,
		allow_dismiss: true,
		newest_on_top: true,
		showProgressbar: false,
		placement: {
			from: $from,
			align: $align
		},
		offset: 20,
		spacing: 10,
		z_index: 10800,
		delay: 3000,
		timer: 1000,
		animate: {
			enter: $enter,
			exit: 'animated fadeOutDown'
		}
	});
};

/**
 * 页面加载等待
 * @param $mode 'show', 'hide'
 * @author yinq
 */
var pageLoader = function ($mode) {
	var $loadingEl = jQuery('#loader-wrapper');
	$mode          = $mode || 'show';
	
	if ($mode === 'show') {
		if ($loadingEl.length) {
			$loadingEl.fadeIn(250);
		} else {
			jQuery('body').prepend('<div id="loader-wrapper"><div id="loader"></div></div>');
		}
	} else if ($mode === 'hide') {
		if ($loadingEl.length) {
			$loadingEl.fadeOut(250);
		}
	}

	return false;
};


/* 关注用户 */
function attentto_user(uid) {
    // 判断是否登录，如果没有就跳转到登录界面
    var login = $("#attenttouser_"+uid).data('login');
    if(login == 'unlogin'){
        window.location.href = '/user/login/';
        return false;
    }
    var action =  $("#attenttouser_"+uid).data('action');
    $.ajax({
        cache: false,
        type: "POST",
        url: "/user/follow/user/",
        data: {'uid': uid, 'action': action},
        async: true,
        success: function(data) {
            if (data['msg'] == 'ok') {
                $("#attenttouser_"+uid).data('action', action == 'follow' ? 'unfollow' : 'follow');
                if ($("#attenttouser_"+uid).hasClass("btn-default")) {
                    $("#attenttouser_"+uid).removeClass("btn-round btn-default");
                    $("#attenttouser_"+uid).addClass("btn-teal btn-circular");

                    $("#attenttouser_"+uid).html('<i class="fa fa-plus"></i> 关注');
                } else {
                    $("#attenttouser_"+uid).removeClass("btn-teal btn-circular");
                    $("#attenttouser_"+uid).addClass("btn-round btn-default");

                    $("#attenttouser_"+uid).html('<i class="fa fa-check"></i> 已关注');
                }
            }
        },
    });
}


/* 首页关注用户 */
function attentto_user_index(uid) {
    // 判断是否登录，如果没有就跳转到登录界面
    var login = $("#attenttouser_"+uid).data('login');
    if(login == 'unlogin'){
        window.location.href = '/user/login/';
        return false;
    }
     var action =  $("#attenttouser_"+uid).data('action');
    $.ajax({
        cache: false,
        type: "POST",
        url: "/user/follow/user/",
        data: {'uid': uid, 'action': action},
        async: true,
        success: function(data) {
            if (data['msg'] == 'ok') {
                $("#attenttouser_"+uid).data('action', action == 'follow' ? 'unfollow' : 'follow');
                if ($("#attenttouser_"+uid).hasClass("following")) {
                    $("#attenttouser_"+uid).removeClass("following");
                    $("#attenttouser_"+uid).addClass(" follow");

                    $("#attenttouser_"+uid).html('<i class="fa fa-plus"></i><span> 关注</span>');
                } else {
                    $("#attenttouser_"+uid).removeClass("follow");
                    $("#attenttouser_"+uid).addClass("following");

                    $("#attenttouser_"+uid).html('<i class="fa fa-check"></i><span> 已关注</span>');
                }
            }
        },
    });
}

/* 关注专题 */
function attentto_cat(tid) {
    // 判断是否登录，如果没有就跳转到登录界面
    var login = $("#attenttocat_"+tid).data('login');
    if(login == 'unlogin'){
        window.location.href = '/user/login/';
        return false;
    }
    var action =  $("#attenttocat_"+tid).data('action');
    $.ajax({
        cache: false,
        type: "POST",
        url: "/user/follow/topic/",
        data: {'tid': tid, 'action': action},
        async: true,
        success: function(data) {
            if (data['msg'] == 'ok') {
                $("#attenttocat_"+tid).data('action', action == 'follow' ? 'unfollow' : 'follow');
                if ($("#attenttocat_"+tid).hasClass("btn-default")) {
                    $("#attenttocat_"+tid).removeClass("btn-round btn-default");
                    $("#attenttocat_"+tid).addClass("btn-teal btn-circular");

                    $("#attenttocat_"+tid).html('<i class="fa fa-plus"></i> 关注');
                } else {
                    $("#attenttocat_"+tid).removeClass("btn-teal btn-circular");
                    $("#attenttocat_"+tid).addClass("btn-round btn-default");

                    $("#attenttocat_"+tid).html('<i class="fa fa-check"></i> 已关注');
                }
            }
        },
    });
}

/* 删除文章 */
function deleteArticle(aid) {
    $.ajax({
        cache: false,
        type : "POST",
        data : {'aid': aid},
        url : "/article/delete/",
        async: true,
        beforeSend : function () {
            pageLoader('show'); // loading
        },
        //成功返回之后调用的函数
        success:function(data){
            if (data['msg'] == 'ok') {
                tips('删除成功！, 页面即将刷新~', 'success');
                setTimeout(function () {
                    window.location.href = '/';
                }, 1500);
            }else {
                tips('好气~ 删除失败!', 'danger');
            }
        },
        complete: function () {
            pageLoader('hide');
        },

        //调用出错执行的函数
        error: function(){
            tips('好气~ 提交失败!', 'danger');
        }
    });
}

/* 喜欢文章 */
function like_article(aid) {
    // 判断是否登录，如果没有就跳转到登录界面
    var login = $("#likearticletaga_"+aid).data('login');
    if(login == 'unlogin'){
        window.location.href = '/user/login/';
        return false;
    }
    var action =  $("#likearticletaga_"+aid).data('action');
    $.ajax({
        cache: false,
        type: "POST",
        data: {'aid': aid, 'action': action},
        url: "/article/like/",
        async: true,
        success: function(data) {
            if (data['msg'] == 'ok') {
                $("#likearticletaga_"+aid).data('action', action == 'like' ? 'unlike' : 'like');
                var previous_likes = parseInt($("#likeatcount_"+aid).text());

                if ($("#likearticlegroup_"+aid).hasClass("active")) {
                    $("#likearticlegroup_"+aid).removeClass("active");

                    $("#likearticletaga_"+aid).html('<i class="fa fa-heart-o"></i><span>喜欢</span>');
                    $("#likeatcount_"+aid).text(previous_likes - 1)
                } else {
                    $("#likearticlegroup_"+aid).addClass("active");

                    $("#likearticletaga_"+aid).html('<i class="fa fa-heart"></i><span>喜欢</span>');
                    $("#likeatcount_"+aid).text(previous_likes + 1)
                }
            }
        },
    });
}

/* 喜欢评论 */
function like_comment(cid) {
    // 判断是否登录，如果没有就跳转到登录界面
    var login = $("#likecomment_"+cid).data('login');
    if(login == 'unlogin'){
        window.location.href = '/user/login/';
        return false;
    }
    var action =  $("#likecomment_"+cid).data('action');
    $.ajax({
        cache: false,
        type: "POST",
        url: "/comment/like/",
        data: {'cid': cid, 'action': action},
        async: true,
        success: function(data) {
            if (data['msg'] == 'ok') {
                $("#likecomment_"+cid).data('action', action == 'like' ? 'unlike' : 'like');
                var previous_likes = parseInt($("#likectcount_"+cid).text());
                if ($("#likecomment_"+cid).hasClass("btn-default")) {
                    $("#likecomment_"+cid).removeClass("btn-default");
                    $("#likecomment_"+cid).addClass("btn-danger");

                    $("#likectcount_"+cid).text(previous_likes + 1);
                } else {
                    $("#likecomment_"+cid).removeClass("btn-danger");
                    $("#likecomment_"+cid).addClass("btn-default");

                    $("#likectcount_"+cid).text(previous_likes - 1)
                }
            }
        },
    });
}

 /*  发表评论 */
function submitComment(aid, pid){
     // 判断是否登录，如果没有就跳转到登录界面
    var login = $("#commentarea_"+pid).data('login');
    if(login == 'unlogin'){
        window.location.href = '/user/login/';
        return false;
    }
    var comment_text = $.trim($("#commentarea_"+pid).val());

    if (comment_text == '') {
        tips('评论不能为空！', 'danger');
        return false;
    }
    $.ajax({
        cache: false,
        type: "POST",
        data: {'aid': aid, 'pid': parseInt(pid), 'content': comment_text},
        url: "/comment/submit/",
        async: true,
        beforeSend : function () {
            pageLoader('show'); // loading
        },
        //成功返回之后调用的函数
        success:function(data){
            if (data['msg'] == 'ok') {
                tips('评论提交成功，页面即将刷新~', 'success');
                $("#commentarea_"+pid).val("");
                setTimeout(function () {
                    location.reload();
                    window.location.href= location.href + '#recentcomments';
                }, 1500);
                return true;
            } else {
                tips('评论出错啦！Ps: 目前不支持有emoji表情符号！对方或已删除评论！', 'danger');
                return false;
            }
        },
        complete: function () {
            pageLoader('hide');
        },

        //调用出错执行的函数
        error: function(){
            tips('好气啊 提交失败啦 Ps: 目前不支持有emoji表情符号！对方或已删除评论！', 'danger');
            return false;
        }
    });
}

 // 加载回复表单
function addCommentReplyForm(pid){
     // 判断是否登录，如果没有就跳转到登录界面
    var login = $("#replyatag_"+pid).data('login');
    if(login == 'unlogin'){
        window.location.href = '/user/login/';
        return false;
    }
    $(".replyform_"+pid).fadeToggle();
    $("#commentarea_"+pid).focus();
}
// 取消回复
function cancleReply(pid) {
    $("#commentarea_"+pid).val("");
    $(".replyform_"+pid).fadeOut();
}

// 删除评论
function deleteComment(cid) {
    $.ajax({
        cache: false,
        type : "POST",
        data : {'cid': parseInt(cid)},
        url : "/comment/delete/",
        async: true,
        beforeSend : function () {
            pageLoader('show'); // loading
        },
        //成功返回之后调用的函数
        success:function(data){
            if (data['msg'] == 'ok') {
                tips('删除成功~', 'success');
                setTimeout(function () {
                    $('#comment-'+cid).remove();
                }, 1000);

            }else {
                tips('好气~ 删除失败!', 'danger');
            }
        },
        complete: function () {
            pageLoader('hide');
        },

        //调用出错执行的函数
        error: function(){
            tips('好气~ 提交失败!', 'danger');
        }
    });
}

// 全选
function selectAll(obj, name)
{
	$("input[name='"+name+"']").prop('checked', obj.checked);
}


