


$('foodName').on('click', function(){
var selected = [];
$('.data input:checked').each(function() {
     selected.push($(this).val());
});



  alert(selected);
});
