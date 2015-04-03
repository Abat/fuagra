$(document).ready(function() {
	$('.likes').click(function() {
		var id;
		id = $(this).attr("data-news_id");
		newsid = id.toString();
		// print "AJAX!"
		$.get('/like_news/', { news_id: id }, function(data){
			data = data + ' likes'
			$("strong.like_count[news_id='" + id.toString() + "'").html(data);
		})
	});
});