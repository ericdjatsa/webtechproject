
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
						name = value.split("&")[0];
						image = value.split("&")[1];
						if (image)
						{ 
							return "<img height=\"60px\" src=\"" + image + "\"/> " + name;
						}
						else
						{
							return name;
						}
					},
				formatResult: function(data, value) 
					{
						return value.split("&")[0];
					}
			}
		); 
	});