# Create your views here.
from playground.sandbox.models import Message
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime
from django.shortcuts import get_object_or_404, render_to_response


def index(request):
    latest_message_list = Message.objects.all().order_by('-timestamp')[:5]
    t = loader.get_template('sandbox/index.html')
    c = Context({
        'latest_message_list': latest_message_list,
    })
    return HttpResponse(t.render(c))


def post(request):
	try:
		title = request.POST['title']
		text = request.POST['text']
		msg = Message(title = title, text = text, timestamp = datetime.now())
		msg.save()		
		return HttpResponseRedirect(reverse('playground.sandbox.views.index'))
	except (KeyError):
		t = loader.get_template('sandbox/post.html')
		c = Context()
		return HttpResponse(t.render(c))

def message(request, msg_id):
	msg = get_object_or_404(Message, pk=msg_id)
	t = loader.get_template('sandbox/message.html')
	c = Context({'message': msg,})
	return HttpResponse(t.render(c))
