$('document').ready(
	function() 
	{	 
		// enable tooltip for "download" element. use the "slide" effect 
		$(".film_thumbnail").tooltip({ 
			effect: "slide",
			position: "bottom center",
			offset: [-100, 0],
			predelay: 1000,
			delay: 1000,});  
	});
