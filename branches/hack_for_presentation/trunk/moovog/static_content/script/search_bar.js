
var show_error_message = function(msg)
{
	$('div#errorbox').html((new Date()).getTime() + " Error: " + msg);
};

var search_data = [];


$('document').ready(
	function()
	{
		$('input#search-string').autocomplete(
			'/frontend/search/json/', 
			{ 
				selectFirst: false,
				extraParams: { type: function() {return $('select#search-type').val();}},
				formatItem: function(data, i, n, value) 
					{
						return "<img height=\"60px\" src=\"" + value.split("&")[1] + "\"/> " + value.split("&")[0];
					},
				formatResult: function(data, value) 
					{
						return value.split("&")[0];
					}
			}
		); 
	});