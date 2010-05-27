function SwitchComment(obj, viewAll)
{
	objs = obj.parentNode.getElementsByTagName("var");
	if(viewAll)
	{
		objs[0].style.display = "none";
		objs[1].style.display = "block";
	}
	else
	{
		objs[0].style.display = "block";
		objs[1].style.display = "none";
	}
}

function ToggleBlock(visibleObj, hiddenObj)
{
	visibleObj.style.display = "block";
	hiddenObj.style.display = "none";
}