$(function(){
	$('#save_value').click(function(){
		var val = [];
		$(':checkbox:checked').each(function(i){
			val[i] = $(this).val();
			print(val[i]);
		});
	});
});