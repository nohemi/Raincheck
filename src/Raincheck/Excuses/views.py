from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


from Raincheck.Excuses.models import Excuse, ExcuseVote

# Create your views here.

@login_required
def vote(request, excuseID, excuse_is_liked):
	excuse = get_object_or_404(Excuse, pk=excuseID)
	try:
		vote = ExcuseVote.objects.get(user=request.user)
	except ExcuseVote.DoesNotExist:
		vote = ExcuseVote(user=request.user)
        if excuse_is_liked == "like":
                excuse.like += 1
		excuse.likedBy.add(vote)
        elif excuse_is_liked == "dislike":
                excuse.dislike += 1
		excuse.dislikedBy.add(vote)
	vote.save()
	excuse.save()
	#ExcuseVote.objects.filter(excuse__is=excuse).count()
	return render_to_response('vote.html', {'excuse': excuse, 'liked': excuse.likedBy.count(),'disliked':excuse.dislikedBy.count()}, context_instance=RequestContext(request))
